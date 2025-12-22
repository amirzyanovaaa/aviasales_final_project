import json
import os
from datetime import datetime
import random


class SimpleDatabase:
    def __init__(self):
        self.data_folder = "data"
        self.data_dir = "data"
        if not os.path.exists(self.data_folder):
            os.makedirs(self.data_folder)
        self._init_airlines()

    def _init_airlines(self):
        self.airlines = [
            {
                "code": "SU",
                "name": "Аэрофлот",
                "website": "https://www.aeroflot.ru/ru-ru",
                "booking_check_url": "https://www.aeroflot.ru/sb/pnr/app/ru-ru#/search"
            },
            {
                "code": "S7",
                "name": "S7 Airlines",
                "website": "https://www.s7.ru/",
                "booking_check_url": "https://myb.s7.ru/myb/find-order"
            },
            {
                "code": "U6",
                "name": "Уральские авиалинии",
                "website": "https://www.uralairlines.ru/",
                "booking_check_url": "https://www.uralairlines.ru/order_check"
            },
            {
                "code": "DP",
                "name": "Победа",
                "website": "https://www.pobeda.aero/ru/",
                "booking_check_url": "https://www.flypobeda.ru/services/booking-management"
            },
            {
                "code": "FV",
                "name": "Россия",
                "website": "https://www.rossiya-airlines.com/",
                "booking_check_url": "https://www.rossiya-airlines.com/"
            },
            {
                "code": "6R",
                "name": "Алроса",
                "website": "https://www.alrosa.aero/",
                "booking_check_url": "https://aero.alrosa.ru/ru/booking/#/find"
            },
            {
                "code": "N4",
                "name": "Nordwind Airlines",
                "website": "https://www.nordwindairlines.ru/",
                "booking_check_url": "https://nordwindairlines.ru/ru/account/booking/find"
            },
            {
                "code": "EO",
                "name": "ЮВТ Аэро",
                "website": "https://uvtaero.ru/",
                "booking_check_url": "https://uvtaero.ru/"
            }
        ]

    def _get_file_path(self, filename):
        return os.path.join(self.data_folder, filename)

    def add_user(self, user_id, username, first_name):
        try:
            users = self.get_all_users()
            new_user = {
                "user_id": user_id,
                "username": username,
                "first_name": first_name,
                "created_at": datetime.now().isoformat(),
                "last_seen": datetime.now().isoformat()
            }
            users[str(user_id)] = new_user
            self._save_to_file("users.json", users)
            print(f"Пользователь {first_name} добавлен")
            return True
        except Exception as e:
            print(f"Ошибка при добавлении пользователя: {e}")
            return False

    def save_search(self, user_id, search_data):
        try:
            searches = self._load_from_file("searches.json", {})
            search_id = len(searches.get("searches", [])) + 1
            search_record = {
                "search_id": search_id,
                "user_id": user_id,
                "data": search_data,
                "created_at": datetime.now().isoformat()
            }
            if "searches" not in searches:
                searches["searches"] = []
            searches["searches"].append(search_record)
            self._save_to_file("searches.json", searches)
            print(f"Поиск сохранен для пользователя {user_id}")
            return True
        except Exception as e:
            print(f"Ошибка при сохранении поиска: {e}")
            return False

    def get_all_users(self):
        return self._load_from_file("users.json", {})

    def _load_from_file(self, filename, default=None):
        filepath = self._get_file_path(filename)
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return default if default is not None else {}
        return default if default is not None else {}

    def _save_to_file(self, filename, data):
        filepath = self._get_file_path(filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def get_user(self, user_id):
        users = self.get_all_users()
        return users.get(str(user_id))

    def update_user_last_seen(self, user_id):
        try:
            users = self.get_all_users()
            if str(user_id) in users:
                users[str(user_id)]["last_seen"] = datetime.now().isoformat()
                self._save_to_file("users.json", users)
                return True
        except Exception as e:
            print(f"Ошибка при обновлении last_seen: {e}")
        return False

    def add_to_favorites(self, user_id, ticket_data):
        try:
            favorites = self._load_from_file("favorites.json", {})
            user_key = str(user_id)
            if user_key not in favorites:
                favorites[user_key] = []
            if "ticket_id" not in ticket_data:
                ticket_data["ticket_id"] = f"TKT-{random.randint(10000, 99999)}-{datetime.now().strftime('%Y%m%d')}"
            ticket_data["saved_at"] = datetime.now().isoformat()
            ticket_exists = False
            for existing in favorites[user_key]:
                if (existing.get("flight_number") == ticket_data.get("flight_number") and
                        existing.get("departure_date") == ticket_data.get("departure_date") and
                        existing.get("airline_code") == ticket_data.get("airline_code")):
                    ticket_exists = True
                    break
            if not ticket_exists:
                favorites[user_key].append(ticket_data)
                self._save_to_file("favorites.json", favorites)
                print(f"Билет добавлен в избранное")
                return {"success": True, "ticket_id": ticket_data["ticket_id"]}
            else:
                print(f"Билет уже в избранном")
                return {"success": False, "reason": "already_exists"}
        except Exception as e:
            print(f"Ошибка при добавлении в избранное: {e}")
            return {"success": False, "reason": "error"}

    def get_favorites(self, user_id):
        try:
            favorites = self._load_from_file("favorites.json", {})
            return favorites.get(str(user_id), [])
        except Exception as e:
            print(f"Ошибка при получении избранного: {e}")
            return []

    def remove_from_favorites(self, user_id, ticket_id):
        try:
            favorites = self._load_from_file("favorites.json", {})
            user_key = str(user_id)

            if user_key in favorites:
                new_favorites = [
                    ticket for ticket in favorites[user_key]
                    if ticket.get("ticket_id") != ticket_id
                ]
                favorites[user_key] = new_favorites
                self._save_to_file("favorites.json", favorites)
                print(f"Билет {ticket_id} удален из избранного пользователя {user_id}")
                return True
            return False
        except Exception as e:
            print(f"Ошибка при удалении из избранного: {e}")
            return False

    def get_airline_by_code(self, airline_code):
        for airline in self.airlines:
            if airline["code"] == airline_code:
                return airline
        return None

    def get_all_airlines(self):
        return self.airlines

    def search_booking_links(self, booking_code=None, last_name=None):
        result = {
            "airlines": self.airlines,
            "instructions":
                "Перейдите на сайт авиакомпании и введите данные"
        }
        if booking_code and len(booking_code) >= 2:
            possible_prefix = booking_code[:2].upper()
            for airline in self.airlines:
                if airline["code"] == possible_prefix:
                    result["suggested_airline"] = airline
                    result["message"] = f"Вероятно, это {airline['name']}:"
                    break
        return result
db = SimpleDatabase()