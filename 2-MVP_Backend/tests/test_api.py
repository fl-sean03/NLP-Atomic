import pytest
from flask import json
from app import app
import time
from unittest.mock import patch

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@patch('app.generate_commands')
def test_commands_valid_prompt(mock_generate_commands, client):
    """Test the /api/commands endpoint with a valid prompt."""
    mock_generate_commands.return_value = [
        {"command": "buildStructure", "params": {"element": "Al", "lattice": "fcc", "nx": 1, "ny": 1, "nz": 1, "format": "pdb"}}
    ]
    response = client.post('/api/commands', json={'prompt': 'create a simple cube'})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) > 0
    mock_generate_commands.assert_called_once_with('create a simple cube')

def test_commands_invalid_prompt(client):
    """Test the /api/commands endpoint with an invalid prompt (e.g., missing prompt)."""
    response = client.post('/api/commands', json={})
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
    assert data['error'] == 'No prompt provided'

@patch('app.generate_commands')
def test_commands_response_time(mock_generate_commands, client):
    """Test that the /api/commands endpoint responds within 3 seconds."""
    mock_generate_commands.return_value = [
        {"command": "buildStructure", "params": {"element": "Al", "lattice": "fcc", "nx": 1, "ny": 1, "nz": 1, "format": "pdb"}}
    ]
    start_time = time.time()
    response = client.post('/api/commands', json={'prompt': 'create a simple cube'})
    end_time = time.time()
    duration = end_time - start_time
    assert response.status_code == 200
    assert duration < 3.0, f"Response time was {duration:.2f} seconds, which is not under 3 seconds."
    mock_generate_commands.assert_called_once_with('create a simple cube')

@patch('app.generate_commands')
def test_commands_llm_error(mock_generate_commands, client):
    """Test the /api/commands endpoint when the LLM returns an error."""
    mock_generate_commands.side_effect = Exception("Simulated LLM error")
    response = client.post('/api/commands', json={'prompt': 'simulate llm error'})
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
    assert 'Error generating commands from NLP: Simulated LLM error' in data['error']
    mock_generate_commands.assert_called_once_with('simulate llm error')