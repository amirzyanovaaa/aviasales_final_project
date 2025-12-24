import pytest
from final_project.iata import find_airports_by_query, get_airport_info_by_iata, get_city_airports


def get_iata_code_compat(search_query):
    airports = find_airports_by_query(search_query)
    return airports[0]["iata"] if airports else None


def get_city_info_compat(search_query):
    airports = find_airports_by_query(search_query)
    if airports:
        return {
            'iata': airports[0]['iata'],
            'found_by': search_query
        }
    return None


def test_get_iata_code_valid():
    assert get_iata_code_compat("москва") == "SVO"
    assert get_iata_code_compat("Москва") == "SVO"
    assert get_iata_code_compat("moscow") == "SVO"
    assert get_iata_code_compat("шереметьево") == "SVO"
    assert get_iata_code_compat("санкт-петербург") == "LED"
    assert get_iata_code_compat("сочи") == "AER"
    assert get_iata_code_compat("нью-йорк") == "JFK"
    assert get_iata_code_compat("лондон") == "LHR"
    assert get_iata_code_compat("париж") == "CDG"
    assert get_iata_code_compat("дубай") == "DXB"

def test_get_iata_code_case_insensitive():
    assert get_iata_code_compat("МОСКВА") == "SVO"
    assert get_iata_code_compat("moscow") == "SVO"
    assert get_iata_code_compat("MOSCOW") == "SVO"
    assert get_iata_code_compat("СоЧи") == "AER"
    assert get_iata_code_compat("LONDON") == "LHR"

def test_get_iata_code_spaces():
    assert get_iata_code_compat("  москва  ") == "SVO"
    assert get_iata_code_compat(" санкт-петербург ") == "LED"
    assert get_iata_code_compat("  шереметьево  ") == "SVO"

def test_get_city_info():
    result = get_city_info_compat("москва")
    assert result is not None
    assert result['iata'] == 'SVO'
    assert result['found_by'] == 'москва'

    result2 = get_city_info_compat("сочи")
    assert result2 is not None
    assert result2['iata'] == 'AER'

    assert get_city_info_compat("несуществующий") is None

def test_get_airport_info_by_iata():
    svo_info = get_airport_info_by_iata("SVO")
    assert svo_info is not None
    assert svo_info["iata"] == "SVO"
    assert svo_info["name_ru"] == "Шереметьево"
    assert svo_info["city_ru"] == "Москва"
    assert svo_info["city_code"] == "MOW"
    assert svo_info["full_name_ru"] == "Москва (Шереметьево)"

    led_info = get_airport_info_by_iata("LED")
    assert led_info is not None
    assert led_info["iata"] == "LED"
    assert led_info["name_ru"] == "Пулково"
    assert led_info["city_ru"] == "Санкт-Петербург"
    assert led_info["city_code"] == "LED"

    jfk_info = get_airport_info_by_iata("JFK")
    assert jfk_info is not None
    assert jfk_info["iata"] == "JFK"
    assert jfk_info["name_ru"] == "Джон Кеннеди"
    assert jfk_info["city_ru"] == "Нью-Йорк"
    assert jfk_info["city_code"] == "NYC"

    assert get_airport_info_by_iata("XXX") is None
    assert get_airport_info_by_iata("") is None
    assert get_airport_info_by_iata("123") is None

def test_get_city_airports():
    moscow_airports = get_city_airports("MOW")
    assert len(moscow_airports) == 4
    moscow_iata_codes = {a["iata"] for a in moscow_airports}
    assert moscow_iata_codes == {"SVO", "DME", "VKO", "ZIA"}

    spb_airports = get_city_airports("LED")
    assert len(spb_airports) == 1
    assert spb_airports[0]["iata"] == "LED"

    nyc_airports = get_city_airports("NYC")
    assert len(nyc_airports) == 3
    nyc_iata_codes = {a["iata"] for a in nyc_airports}
    assert nyc_iata_codes == {"JFK", "LGA", "EWR"}

    assert get_city_airports("XXX") == []
    assert get_city_airports("") == []

def test_city_with_multiple_airports():
    london_results = find_airports_by_query("лондон")
    assert len(london_results) == 4
    london_iata_codes = {a["iata"] for a in london_results}
    assert london_iata_codes == {"LHR", "LGW", "STN", "LTN"}

    paris_results = find_airports_by_query("париж")
    assert len(paris_results) == 3
    paris_iata_codes = {a["iata"] for a in paris_results}
    assert paris_iata_codes == {"CDG", "ORY", "BVA"}

    berlin_results = find_airports_by_query("берлин")
    assert len(berlin_results) == 3
    berlin_iata_codes = {a["iata"] for a in berlin_results}
    assert berlin_iata_codes == {"BER", "TXL", "SXF"}

def test_short_names_and_aliases():
    assert get_iata_code_compat("спб") == "LED"
    assert get_iata_code_compat("петербург") == "LED"

    assert get_iata_code_compat("st petersburg") == "LED"
    assert get_iata_code_compat("new york") == "JFK"
    assert get_iata_code_compat("los angeles") == "LAX"

    assert get_iata_code_compat("svo") == "SVO"
    assert get_iata_code_compat("LED") == "LED"
    assert get_iata_code_compat("jfk") == "JFK"

    assert get_iata_code_compat("mow") == "SVO"
    assert get_iata_code_compat("nyc") == "JFK"
    assert get_iata_code_compat("lon") == "LHR"