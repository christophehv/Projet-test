import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import app
import pytest
import json
import jwt

@pytest.fixture
def client():
    app.app.config['TESTING'] = True
    with app.app.test_client() as client:
        yield client

def test_register(client):
    response = client.post('/api/register', json={
        'username': 'testuser',
        'email': 'test@test.com',
        'password': 'password123'
    })
    assert response.status_code == 201
    assert b'User registered successfully' in response.data

def test_login(client):
    # First register a user
    client.post('/api/register', json={
        'username': 'testuser2',
        'email': 'test2@test.com',
        'password': 'password123'
    })
    
    # Then try to login
    response = client.post('/api/login', json={
        'username': 'testuser2',
        'password': 'password123'
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'token' in data
    assert 'is_admin' in data

def test_get_users_unauthorized(client):
    response = client.get('/api/users')
    assert response.status_code == 401

def test_get_users_authorized(client):
    # First login to get a token
    response = client.post('/api/login', json={
        'username': 'admin',
        'password': 'admin123'
    })
    print('LOGIN ADMIN RESPONSE:', response.data)
    token = json.loads(response.data)['token']
    
    # Then try to get users with the token
    response = client.get('/api/users', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)

def test_delete_user_unauthorized(client):
    response = client.delete('/api/users/1')
    assert response.status_code == 401

def test_delete_user_not_admin(client):
    # First register and login as a normal user
    client.post('/api/register', json={
        'username': 'normaluser',
        'email': 'normal@test.com',
        'password': 'password123'
    })
    response = client.post('/api/login', json={
        'username': 'normaluser',
        'password': 'password123'
    })
    token = json.loads(response.data)['token']
    
    # Try to delete a user
    response = client.delete('/api/users/1', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 403 