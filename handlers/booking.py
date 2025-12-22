from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from final_project.states import CheckBooking
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


router = Router()

AIRLINES = [
    {"code": "SU", "name": "Аэрофлот", "url": "https://www.aeroflot.ru/sb/pnr/app/ru-ru#/search"},
    {"code": "S7", "name": "S7 Airlines", "url": "https://myb.s7.ru/myb/find-order"},
    {"code": "U6", "name": "Уральские авиалинии", "url": "https://www.uralairlines.ru/order_check"},
    {"code": "DP", "name": "Победа", "url": "https://www.flypobeda.ru/services/booking-management"},
    {"code": "FV", "name": "Россия", "url": "https://www.rossiya-airlines.com/"},
]


@router.message(F.text == "📖 Проверить бронь")
async def start_booking_check(message: types.Message, state: FSMContext):
    await message.answer(
        "Введите номер бронирования (PNR).\n"
        "Например: SU12345 (обычно начинается с кода авиакомпании)."
    )
    await state.set_state(CheckBooking.booking_code)


@router.message(CheckBooking.booking_code)
async def process_booking_code(message: types.Message, state: FSMContext):
    code = message.text.strip().upper()

    found_airline = None
    # Ищем по первым двум буквам
    if len(code) >= 2:
        prefix = code[:2]
        for airline in AIRLINES:
            if airline["code"] == prefix:
                found_airline = airline
                break

    if found_airline:
        text = (
            f"Похоже, это <b>{found_airline['name']}</b>.\n"
            f"Перейдите на сайт для проверки:"
        )
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Проверить на сайте", url=found_airline['url'])]
        ])
        await message.answer(text, parse_mode="HTML", reply_markup=kb)
    else:
        await message.answer(
            "Не удалось определить авиакомпанию автоматически.\n"
            "Попробуйте проверить на сайте перевозчика вручную."
        )

    await state.clear()