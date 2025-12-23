import pytest
from final_project.iata import get_iata_code, get_city_info

def test_get_iata_code_valid():
    assert get_iata_code("москва") == "SVO"
    assert get_iata_code("Москва") == "SVO"
    assert get_iata_code("moscow") == "SVO"
    assert get_iata_code("шереметьево") == "SVO"
    assert get_iata_code("санкт-петербург") == "LED"
    assert get_iata_code("сочи") == "AER"
    assert get_iata_code("нью-йорк") == "JFK"
    assert get_iata_code("лондон") == "LHR"
    assert get_iata_code("париж") == "CDG"
    assert get_iata_code("дубай") == "DXB"

def test_get_iata_code_invalid():
    assert get_iata_code("") is None
    assert get_iata_code("   ") is None
    assert get_iata_code("несуществующий город") is None
    assert get_iata_code("random city") is None
    assert get_iata_code("12345") is None

def test_get_iata_code_case_insensitive():
    assert get_iata_code("МОСКВА") == "SVO"
    assert get_iata_code("moscow") == "SVO"
    assert get_iata_code("MOSCOW") == "SVO"

def test_get_iata_code_spaces():
    assert get_iata_code("  москва  ") == "SVO"
    assert get_iata_code(" санкт-петербург ") == "LED"

def test_get_city_info():
    result = get_city_info("москва")
    assert result is not None
    assert result['iata'] == 'SVO'
    assert get_city_info("несуществующий") is None