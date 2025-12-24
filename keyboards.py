from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_main_menu():
    kb = [
        [KeyboardButton(text="Поиск билетов"), KeyboardButton(text="Проверить бронь")],
        [KeyboardButton(text="Избранное")]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)


def get_ticket_fav_kb(flight_number):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="В избранное", callback_data=f"add_fav:{flight_number}")]
    ])


def get_delete_fav_kb(ticket_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Удалить", callback_data=f"del_fav:{ticket_id}")]
    ])


def get_booking_link_kb(url):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Проверить на сайте", url=url)]
    ])


def get_airports_chosen(airports,  destination=False):
    builder = InlineKeyboardBuilder()

    for airport in airports:
        if 'name_ru' in airport:
            display_text = airport['name_ru']
            if 'city_ru' in airport and 'airport_name_ru' in airport:
                if airport['city_ru'] != airport['airport_name_ru']:
                    display_text = f"{airport['city_ru']} ({airport['airport_name_ru']})"
        elif 'name' in airport:
            display_text = airport['name']
        else:
            display_text = f"Аэропорт {airport['iata']}"
        if len(airports) > 1:
            display_text = f"{display_text} ({airport['iata']})"

        callback_prefix = "dest_airport_" if destination else "airport_"
        builder.button(
            text=display_text,
            callback_data=f"{callback_prefix}{airport['iata']}"
        )

    builder.button(text="Отмена", callback_data="cancel_search")
    builder.adjust(1)
    return builder.as_markup()
