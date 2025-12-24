import pytest
import requests
from unittest.mock import MagicMock, patch
from final_project.services.client import Client

@pytest.fixture
def client():
    return Client()

def test_parser_valid_data(client):
    fake_offer = {
        'itineraries': [{
            'segments': [
                {'departure': {'at': '2024-12-31T10:30:00'}, 'carrierCode': 'SU', 'number': '1234'},
                {'arrival': {'at': '2024-12-31T14:00:00'}}
            ]
        }],
        'price': {'total': '15000.50', 'currency': 'RUB'}
    }

    result = client.parser(fake_offer, "MOW", "LED")

    assert result['airline'] == "SU"
    assert result['flight_number'] == "SU1234"
    assert result['departure_time'] == "10:30"
    assert result['price'] == 15000.5

def test_parser_broken_data(client):
    assert client.parser({}, "A", "B") is None

    bad_offer = {'itineraries': [{'segments': []}]}
    assert client.parser(bad_offer, "A", "B") is None

def test_search_flights_api_error(client):
    with patch.object(client.session, 'post', side_effect=requests.exceptions.RequestException):
        with patch.object(client, 'get_token', return_value="fake_token"):
            result = client.search_flights("A", "B", "2024")
            assert result == []

def test_search_flights_no_token(client):
    with patch.object(client, 'get_token', return_value=None):
        result = client.search_flights("A", "B", "2024")
        assert result == []