from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


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