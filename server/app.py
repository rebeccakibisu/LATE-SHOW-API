# server/app.py

from flask import Flask, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api, Resource
from sqlalchemy.exc import IntegrityError

# Local imports
from models import db, Episode, Guest, Appearance

# 1. Configure the Flask App
app = Flask(__name__)
# Set database URI to SQLite (app.db)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database and migration
db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)

# 2. Basic Index Route
@app.route('/')
def index():
    return '<h1>🎬 Late Show API</h1>'

# --- Phase 4: Build API Endpoints ---

# Resource for all Episodes
class Episodes(Resource):
    # 1. GET /episodes
    def get(self):
        episodes = Episode.query.all()
        # Use serialization rules from the model
        episodes_dict = [episode.to_dict(rules=('-appearances',)) for episode in episodes]
        
        return make_response(episodes_dict, 200)

# Resource for single Episode (GET, DELETE)
class EpisodeByID(Resource):
    # 2. GET /episodes/<int:id>
    def get(self, id):
        episode = Episode.query.get(id)
        
        if not episode:
            return make_response({"error": "Episode not found"}, 404)
        
        # Include nested appearances with guest details (default serialization includes this)
        return make_response(episode.to_dict(), 200)

    # 3. DELETE /episodes/<int:id>
    def delete(self, id):
        episode = Episode.query.get(id)
        
        if not episode:
            return make_response({"error": "Episode not found"}, 404)

        db.session.delete(episode)
        db.session.commit()
        
        # Status 204 (No Content)
        return make_response('', 204) 

# Resource for all Guests
class Guests(Resource):
    # 4. GET /guests
    def get(self):
        guests = Guest.query.all()
        # Use serialization rules from the model
        guests_dict = [guest.to_dict(rules=('-appearances',)) for guest in guests]
        
        return make_response(guests_dict, 200)

# Resource for creating Appearances
class Appearances(Resource):
    # 5. POST /appearances
    def post(self):
        # Parse JSON data from the request body
        data = request.get_json()
        
        try:
            # Create a new Appearance instance
            new_appearance = Appearance(
                rating=data['rating'],
                episode_id=data['episode_id'],
                guest_id=data['guest_id']
            )
            
            # Add and commit to trigger the SQLAlchemy validator (models.py)
            db.session.add(new_appearance)
            db.session.commit()
            
            # If valid: Status 201, return appearance with nested episode and guest
            return make_response(new_appearance.to_dict(), 201)
        
        except ValueError as e:
            # If invalid: Status 400, return validation errors
            return make_response({"errors": [str(e)]}, 400)
        
        except IntegrityError:
            # Handle foreign key errors if episode_id or guest_id don't exist
            db.session.rollback()
            return make_response({"errors": ["Episode or Guest ID not found."]}, 400)

# Add resources to the API
api.add_resource(Episodes, '/episodes')
api.add_resource(EpisodeByID, '/episodes/<int:id>')
api.add_resource(Guests, '/guests')
api.add_resource(Appearances, '/appearances')

# Run the app on port 5555
if __name__ == '__main__':
    app.run(port=5555, debug=True)