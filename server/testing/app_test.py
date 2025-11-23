import pytest

# --- GET /episodes ---
def test_get_episodes(client):
    response = client.get('/episodes')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) >= 2
    
    first_episode = data[0]
    assert 'id' in first_episode
    assert 'date' in first_episode
    assert 'number' in first_episode
    assert 'appearances' not in first_episode

# --- GET /episodes/<int:id> ---
def test_get_episode_by_id_success(client, episode_model, guest_model):
    episode = episode_model.query.filter_by(number=1).first()
    response = client.get(f'/episodes/{episode.id}')
    assert response.status_code == 200
    data = response.get_json()

    assert data['id'] == episode.id
    assert data['number'] == 1
    assert 'appearances' in data
    assert len(data['appearances']) == 2
    appearance = data['appearances'][0]
    assert 'rating' in appearance
    assert 'guest' in appearance
    assert 'id' in appearance['guest']
    assert 'name' in appearance['guest']

def test_get_episode_by_id_not_found(client):
    response = client.get('/episodes/999')
    assert response.status_code == 404
    assert response.get_json() == {"error": "Episode not found"}

# --- DELETE /episodes/<int:id> ---
def test_delete_episode_success(client, episode_model, appearance_model, database):
    ep_to_delete = episode_model(date="temp", number=99)
    database.session.add(ep_to_delete)
    database.session.commit()

    delete_id = ep_to_delete.id
    initial_appearances = appearance_model.query.count()

    response = client.delete(f'/episodes/{delete_id}')
    assert response.status_code == 204
    assert response.data == b''

    assert episode_model.query.get(delete_id) is None
    assert appearance_model.query.filter_by(episode_id=delete_id).count() == 0
    assert appearance_model.query.count() == initial_appearances

def test_delete_episode_not_found(client):
    response = client.delete('/episodes/998')
    assert response.status_code == 404
    assert response.get_json() == {"error": "Episode not found"}

# --- GET /guests ---
def test_get_guests(client):
    response = client.get('/guests')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) >= 2

    first_guest = data[0]
    assert 'id' in first_guest
    assert 'name' in first_guest
    assert 'occupation' in first_guest
    assert 'appearances' not in first_guest

# --- POST /appearances ---
def test_post_appearance_success(client, episode_model, guest_model, appearance_model):
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

    assert data['rating'] == 5
    assert data['episode_id'] == e_id
    assert 'episode' in data
    assert 'guest' in data
    assert data['episode']['number'] == 2
    assert data['guest']['name'] == "Madonna"

    assert appearance_model.query.count() == initial_count + 1
