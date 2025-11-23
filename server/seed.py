# server/seed.py

from app import app
from models import db, Episode, Guest, Appearance

with app.app_context():
    
    print("Clearing database tables...")
    # Clear data from tables in reverse order of dependency
    Appearance.query.delete()
    Episode.query.delete()
    Guest.query.delete()
    
    # --- Episodes ---
    print("Creating episodes...")
    e1 = Episode(date="1/11/99", number=1)
    e2 = Episode(date="1/12/99", number=2)
    e3 = Episode(date="1/13/99", number=3)

    db.session.add_all([e1, e2, e3])
    
    # --- Guests ---
    print("Creating guests...")
    g1 = Guest(name="Michael J. Fox", occupation="actor")
    g2 = Guest(name="Sandra Bernhard", occupation="Comedian")
    g3 = Guest(name="Tracey Ullman", occupation="television actress")
    g4 = Guest(name="Will Smith", occupation="rapper and actor")

    db.session.add_all([g1, g2, g3, g4])
    
    db.session.commit() # Commit to get IDs before creating Appearances

    # --- Appearances ---
    print("Creating appearances...")
    a1 = Appearance(rating=4, episode=e1, guest=g1) # Michael J. Fox on Ep 1
    a2 = Appearance(rating=5, episode=e1, guest=g2) # Sandra Bernhard on Ep 1
    a3 = Appearance(rating=3, episode=e2, guest=g3) # Tracey Ullman on Ep 2
    a4 = Appearance(rating=5, episode=e2, guest=g4) # Will Smith on Ep 2
    a5 = Appearance(rating=1, episode=e3, guest=g1) # Michael J. Fox on Ep 3
    a6 = Appearance(rating=4, episode=e3, guest=g3) # Tracey Ullman on Ep 3

    db.session.add_all([a1, a2, a3, a4, a5, a6])
    
    db.session.commit()
    
    print("Seeding complete! 🌱")