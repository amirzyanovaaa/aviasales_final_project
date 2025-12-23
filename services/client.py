import requests
from typing import List, Dict, Any
from final_project.config import AMADEUS_API_KEY, AMADEUS_API_SECRET, AMADEUS_BASE_URL


class Client:
    def __init__(self):
        self.base_url = AMADEUS_BASE_URL
        self.api_key = AMADEUS_API_KEY
        self.api_secret = AMADEUS_API_SECRET
        self.session = requests.Session()

    def get_token(self) -> Any | None:
        token_url = f"{self.base_url}/v1/security/oauth2/token"
        data = {
            'grant_type': 'client_credentials',
            'client_id': self.api_key,
            'client_secret': self.api_secret
        }
        response = requests.post(token_url, data=data)
        if response.status_code == 200:
            token = response.json()['access_token']
            return token
        else:
            return None

    def search_flights(self,
                       origin: str,
                       destination: str,
                       departure_date: str,
                       adults: int = 1) -> List[Dict[str, Any]]:
        token = self.get_token()
        if not token:
            print("Ошибка: отсутствие токена от Amadeus")
            return []

        url = f"{self.base_url}/v2/shopping/flight-offers"
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        payload = {
            "currencyCode": "RUB",
            "originDestinations": [
                {
                    "id": "1",
                    "originLocationCode": origin.upper(),
                    "destinationLocationCode": destination.upper(),
                    "departureDateTimeRange": {
                        "date": departure_date,
                        "time": "00:00:00"
                    }
                }
            ],
            "travelers": [
                {
                    "id": "1",
                    "travelerType": "ADULT",
                    "fareOptions": ["STANDARD"]
                }
            ],
            "sources": ["GDS"],
            "searchCriteria": {
                "maxFlightOffers": 5,
            }
        }

        try:
            response = self.session.post(url, headers=headers, json=payload, timeout=15)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as e:
            return []

        flights = []
        if 'data' in data and data['data']:
            for offer in data['data']:
                flight_info = self.parser(offer, origin, destination)
                if flight_info:
                    flights.append(flight_info)
        return flights

    def parser(self, offer: dict, origin: str, destination: str) -> dict | None:
        try:
            itinerary = offer.get('itineraries', [{}])[0]
            segments = itinerary.get('segments', [])
            if not segments:
                return None

            first_segment = segments[0]
            last_segment = segments[-1]
            price_info = offer.get('price', {})

            departure_at = first_segment.get('departure', {}).get('at', '')
            arrival_at = last_segment.get('arrival', {}).get('at', '')

            return {
                'origin': origin.upper(),
                'destination': destination.upper(),
                'departure_date': departure_at[:10] if departure_at else "2024-01-15",
                'departure_time': departure_at[11:16] if departure_at else "10:00",
                'arrival_date': arrival_at[:10] if arrival_at else "2024-01-15",
                'arrival_time': arrival_at[11:16] if arrival_at else "12:00",
                'airline': first_segment.get('carrierCode', 'SU' if origin == 'SVO' else 'AY'),
                'flight_number': f"{first_segment.get('carrierCode', 'SU')}{first_segment.get('number', '1234')}",
                'price': float(price_info.get('total', 15000)),
                'currency': price_info.get('currency', 'RUB'),
                'transfers': len(segments) - 1,
            }
        except Exception:
            return None