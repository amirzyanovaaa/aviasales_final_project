from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from states import CheckBooking
from loader import db
import keyboards as kb

router = Router()


@router.message(F.text == "Проверить бронь")
async def start_check(message: types.Message, state: FSMContext):
    await message.answer("Введите номер брони (PNR):")
    await state.set_state(CheckBooking.booking_code)


@router.message(CheckBooking.booking_code)
async def process_code(message: types.Message, state: FSMContext):
    code = message.text.strip()
    result = db.search_booking_links(booking_code=code)
    text = result["instructions"]
    keyboard = None

    if "suggested_airline" in result:
        airline = result["suggested_airline"]
        text += f"\n\nВероятно, это билет компании {airline['name']}."
        keyboard = kb.get_booking_link_kb(airline['booking_check_url'])

    await message.answer(text, reply_markup=keyboard)
    await state.clear()
