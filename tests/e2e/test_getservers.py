"""Integration testing for GET /servers method."""
import os
import requests


def test_get_server_method():
    """Test /servers method returns 200."""
    response = requests.get(
        'https://' + os.getenv('API_DOMAIN_NAME') + '/servers',
        headers={
            'x-api-key': os.getenv('API_KEY')
        }
    )
    assert response.status_code == 200
    assert isinstance(response.json().get('servers'), list)
