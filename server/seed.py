from server.app import app
from server.models import db, Episode, Guest, Appearance


with app.app_context():

    print("Clearing database...")
    Appearance.query.delete()
    Episode.query.delete()
    Guest.query.delete()

    print("Seeding database...")

    e1 = Episode(date="1/11/99", number=1)
    e2 = Episode(date="1/12/99", number=2)

    g1 = Guest(name="Michael J. Fox", occupation="actor")
    g2 = Guest(name="Sandra Bernhard", occupation="Comedian")
    g3 = Guest(name="Tracey Ullman", occupation="television actress")

    db.session.add_all([e1, e2, g1, g2, g3])
    db.session.commit()

    a1 = Appearance(rating=4, episode=e1, guest=g1)
    a2 = Appearance(rating=3, episode=e1, guest=g2)
    a3 = Appearance(rating=5, episode=e2, guest=g3)

    db.session.add_all([a1, a2, a3])
    db.session.commit()

    print("✅ Database seeded successfully!")
