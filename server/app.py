from flask import Flask, request
from flask_restful import Api, Resource
from flask_migrate import Migrate
from server.models import db, Episode, Guest, Appearance

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)

@app.route('/')
def index():
    return "Late Show API running on port 5555"

class Episodes(Resource):
    def get(self):
        episodes = Episode.query.all()
        return [
            {"id": e.id, "date": e.date, "number": e.number}
            for e in episodes
        ], 200

class EpisodeByID(Resource):
    def get(self, id):
        episode = Episode.query.get(id)
        if not episode:
            return {"error": "Episode not found"}, 404
        return episode.to_dict(), 200

    def delete(self, id):
        episode = Episode.query.get(id)
        if not episode:
            return {"error": "Episode not found"}, 404
        
        db.session.delete(episode)
        db.session.commit()

        return "", 204

class Guests(Resource):
    def get(self):
        guests = Guest.query.all()
        return [
            {"id": g.id, "name": g.name, "occupation": g.occupation}
            for g in guests
        ], 200

class Appearances(Resource):
    def post(self):
        data = request.get_json()

        episode = Episode.query.get(data.get("episode_id"))
        guest = Guest.query.get(data.get("guest_id"))

        if not episode or not guest:
            return {"errors": ["Episode or Guest ID not found."]}, 400

        try:
            appearance = Appearance(
                rating=data.get("rating"),
                episode=episode,
                guest=guest
            )
            db.session.add(appearance)
            db.session.commit()
        except ValueError:
            return {"errors": ["Rating must be between 1 and 5."]}, 400

        return appearance.to_dict(), 201

# Register Resources
api.add_resource(Episodes, "/episodes")
api.add_resource(EpisodeByID, "/episodes/<int:id>")
api.add_resource(Guests, "/guests")
api.add_resource(Appearances, "/appearances")

if __name__ == "__main__":
    app.run(port=5555, debug=True)
