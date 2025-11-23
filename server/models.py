# server/models.py

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin

# Configure a naming convention for constraints
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

# --- Episode Model ---
class Episode(db.Model, SerializerMixin):
    __tablename__ = 'episodes'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String)
    number = db.Column(db.Integer)

    # Relationship: has many Guests through Appearances
    # back_populates links the relationships on both models
    appearances = db.relationship('Appearance', back_populates='episode', cascade='all, delete-orphan')

    # Serialization rules (to prevent infinite recursion - exclude 'appearances' in list view)
    serialize_rules = ('-appearances.episode',)
    
    def __repr__(self):
        return f'<Episode {self.id}: {self.date} - Number {self.number}>'

# --- Guest Model ---
class Guest(db.Model, SerializerMixin):
    __tablename__ = 'guests'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    occupation = db.Column(db.String)

    # Relationship: has many Episodes through Appearances
    appearances = db.relationship('Appearance', back_populates='guest', cascade='all, delete-orphan')

    # Serialization rules
    serialize_rules = ('-appearances.guest',)
    
    def __repr__(self):
        return f'<Guest {self.id}: {self.name}>'

# --- Appearance Model ---
class Appearance(db.Model, SerializerMixin):
    __tablename__ = 'appearances'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)
    
    # Foreign Keys: episode_id, guest_id
    episode_id = db.Column(db.Integer, db.ForeignKey('episodes.id'))
    guest_id = db.Column(db.Integer, db.ForeignKey('guests.id'))

    # Relationships: belongs to Episode AND Guest
    # back_populates links the relationships on both models
    episode = db.relationship('Episode', back_populates='appearances')
    guest = db.relationship('Guest', back_populates='appearances')

    # Cascade delete configuration (handled on the Episode and Guest models)

    # Serialization rules: allows Appearance to show Episode and Guest details
    # We want to show the episode details on the Appearance POST response
    serialize_rules = ('-episode.appearances', '-guest.appearances')

    # Validation: Rating must be between 1 and 5 (inclusive)
    @validates('rating')
    def validate_rating(self, key, rating):
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5.")
        return rating
    
    def __repr__(self):
        return f'<Appearance {self.id}: Rating {self.rating} - E:{self.episode_id} G:{self.guest_id}>'