import pytest
from fastapi.testclient import TestClient
from main import app
from database.models import User, Session
from database.kidinteraction import KidInteraction
from unittest.mock import patch, MagicMock
import json

@pytest.fixture
def client():
    return TestClient(app, base_url="http://localhost:8000")

# Mock database operations
@pytest.fixture
def mock_db():
    with patch('database.models.User') as mock_user, \
         patch('database.models.Session') as mock_session, \
         patch('database.kidinteraction.KidInteraction') as mock_kid_interaction, \
         patch('database.email.send_otp') as mock_send_otp:
        yield {
            'user': mock_user,
            'session': mock_session,
            'kid_interaction': mock_kid_interaction,
            'send_otp': mock_send_otp
        }

# Auth Tests
def test_login_success(client, mock_db):
    # Mock user verification
    mock_user = MagicMock()
    mock_user.verify_password.return_value = True
    mock_user.email = 'test@example.com'
    mock_db['user'].get.return_value = mock_user
    
    # Mock session creation
    mock_session = MagicMock()
    mock_session.id = 'test_session_id'
    mock_db['session'].create.return_value = mock_session

    response = client.post('/auth/login', params={'username': 'testuser', 'password': 'password123'})
    assert response.status_code == 200
    assert 'session_id' in response.json()

def test_login_failure(client, mock_db):
    mock_db['user'].get.return_value = None
    response = client.post('/auth/login', params={'username': 'wronguser', 'password': 'wrongpass'})
    assert response.status_code == 200
    assert response.json()['error'] == 'Invalid username or password'

def test_signup_success(client, mock_db):
    mock_db['user'].exists.return_value = False
    mock_user = MagicMock()
    mock_user.email = 'test@example.com'
    mock_db['user'].create.return_value = mock_user
    
    mock_session = MagicMock()
    mock_session.id = 'new_session_id'
    mock_db['session'].create.return_value = mock_session

    response = client.post('/auth/signup', params={
        'username': 'newuser',
        'email': 'test@example.com',
        'password': 'password123'
    })
    assert response.status_code == 200
    assert response.json()['message'] == 'User created'
    assert 'session_id' in response.json()

# Scenario Tests
def test_get_all_questions(client):
    with patch('endpoints.scenario.load_scenarios') as mock_load:
        mock_load.return_value = {
            'q1': {'question': 'Test Q1', 'options': {}},
            'q2': {'question': 'Test Q2', 'options': {}}
        }
        response = client.get('/scenario/questions')
        assert response.status_code == 200
        assert len(response.json()) == 2

def test_get_specific_question(client):
    with patch('endpoints.scenario.load_scenarios') as mock_load:
        mock_load.return_value = {
            'q1': {'question': 'Test Q1', 'options': {'a': {'id': '1a', 'text': 'Option A', 'correct': True}}}
        }
        response = client.get('/scenario/question/1')
        assert response.status_code == 200
        assert response.json()['question'] == 'Test Q1'

def test_submit_answer(client, mock_db):
    # Mock scenarios
    with patch('endpoints.scenario.load_scenarios') as mock_load:
        mock_load.return_value = {
            'q1': {
                'options': {
                    'a': {'id': '1a', 'text': 'Option A', 'correct': True}
                }
            }
        }
        
        # Set kid_id cookie
        client.cookies.set('kid_id', '123')
        
        response = client.post('/scenario/answer/1', params={'option_id': '1a'})
        assert response.status_code == 200
        assert response.json()['correct'] == True
        
        # Verify interaction was logged
        mock_db['kid_interaction'].create_interaction.assert_called_once()

def test_get_progress(client, mock_db):
    # Mock interactions
    mock_db['kid_interaction'].get_interactions_by_kid.return_value = [
        {'question_id': 1, 'is_correct': True},
        {'question_id': 2, 'is_correct': False}
    ]
    mock_db['kid_interaction'].get_interactions_by_kid_and_correctness.return_value = [
        {'question_id': 1, 'is_correct': True}
    ]
    
    response = client.get('/scenario/progress/123')
    assert response.status_code == 200
    assert response.json()['total_questions_attempted'] == 2
    assert response.json()['correct_answers'] == 1