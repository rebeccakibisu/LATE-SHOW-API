# server/testing/app_test.py

import pytest

# --- GET /episodes ---
def test_get_episodes(client):
    response = client.get('/episodes')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) >= 2
    
    # Check response format
    first_episode = data[0]
    assert 'id' in first_episode
    assert 'date' in first_episode
    assert 'number' in first_episode
    # Should not include appearances in the list view
    assert 'appearances' not in first_episode

# --- GET /episodes/<int:id> ---
def test_get_episode_by_id_success(client, episode_model, guest_model):
    episode = episode_model.query.filter_by(number=1).first()
    response = client.get(f'/episodes/{episode.id}')
    assert response.status_code == 200
    data = response.get_json()
    
    # Check main episode data
    assert data['id'] == episode.id
    assert data['number'] == 1
    
    # Check nested appearances with guest details
    assert 'appearances' in data
    assert len(data['appearances']) == 2 # Based on conftest seed
    appearance = data['appearances'][0]
    assert 'rating' in appearance
    assert 'guest' in appearance
    assert 'id' in appearance['guest']
    assert 'name' in appearance['guest']

def test_get_episode_by_id_not_found(client):
    response = client.get('/episodes/999') # Non-existent ID
    assert response.status_code == 404
    assert response.get_json() == {"error": "Episode not found"}

# --- DELETE /episodes/<int:id> ---
def test_delete_episode_success(client, episode_model, appearance_model, database):
    # Create a new episode to delete
    with database.session.no_autoflush:
        ep_to_delete = episode_model(date="temp", number=99)
        database.session.add(ep_to_delete)
        database.session.commit()
    
    delete_id = ep_to_delete.id
    
    # Check if appearances exist for this episode (if any)
    initial_appearances = appearance_model.query.count()

    response = client.delete(f'/episodes/{delete_id}')
    assert response.status_code == 204
    assert response.data == b'' # No Content response

    # Verify episode is deleted
    assert episode_model.query.get(delete_id) is None
    
    # Verify cascade delete worked (no appearances left for this episode)
    assert appearance_model.query.filter_by(episode_id=delete_id).count() == 0
    # Total appearances should remain the same since the test episode had no appearances
    assert appearance_model.query.count() == initial_appearances
    

def test_delete_episode_not_found(client):
    response = client.delete('/episodes/998') # Non-existent ID
    assert response.status_code == 404
    assert response.get_json() == {"error": "Episode not found"}

# --- GET /guests ---
def test_get_guests(client):
    response = client.get('/guests')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) >= 2
    
    # Check response format
    first_guest = data[0]
    assert 'id' in first_guest
    assert 'name' in first_guest
    assert 'occupation' in first_guest
    # Should not include appearances in the list view
    assert 'appearances' not in first_guest

# --- POST /appearances ---
def test_post_appearance_success(client, episode_model, guest_model, appearance_model):
    # Get IDs for foreign keys
    e_id = episode_model.query.filter_by(number=2).first().id
    g_id = guest_model.query.filter_by(name="Madonna").first().id
    
    initial_count = appearance_model.query.count()

    new_appearance_data = {
        "rating": 5,
        "episode_id": e_id,
        "guest_id": g_id
    }
    
    response = client.post('/appearances', json=new_appearance_data)
    assert response.status_code == 201
    data = response.get_json()
    
    # Check response format
    assert data['rating'] == 5
    assert data['episode_id'] == e_id
    assert 'episode' in data # Check nested episode details
    assert 'guest' in data # Check nested guest details
    assert data['episode']['number'] == 2
    assert data['guest']['name'] == "Madonna"

    # Verify in the database
    assert appearance_model.query.count() == initial_count + 1

def test_post_appearance_validation_error(client, episode_model, guest_model):
    e_id = episode_model.query.filter_by(number=2).first().id
    g_id = guest_model.query.filter_by(name="Madonna").first().id
    
    # Invalid rating (6 is > 5)
    invalid_data = {
        "rating": 6, 
        "episode_id": e_id, 
        "guest_id": g_id
    }
    
    response = client.post('/appearances', json=invalid_data)
    assert response.status_code == 400
    assert response.get_json() == {"errors": ["Rating must be between 1 and 5."]}

def test_post_appearance_foreign_key_error(client):
    # Non-existent episode ID
    invalid_data = {
        "rating": 5, 
        "episode_id": 9999, 
        "guest_id": 1
    }
    
    response = client.post('/appearances', json=invalid_data)
    assert response.status_code == 400
    assert response.get_json() == {"errors": ["Episode or Guest ID not found."]}