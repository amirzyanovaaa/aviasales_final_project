import re
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from final_project.states import SearchFlight
from final_project.loader import amadeus_client
from final_project import keyboards as kb
from final_project.iata import get_iata_code

router = Router()


@router.message(F.text == "Поиск билетов")
async def start_search(message: types.Message, state: FSMContext):
    await message.answer("Введите название города вылета:")
    await state.set_state(SearchFlight.origin)


@router.message(SearchFlight.origin)
async def process_origin(message: types.Message, state: FSMContext):
    user_input = message.text.strip()
    iata_code = get_iata_code(user_input)
    if iata_code:
        await state.update_data(origin=iata_code)
        await message.answer(f"Найден аэропорт: {iata_code}")
        await message.answer("Введите название города прибытия:")
        await state.set_state(SearchFlight.destination)
        return

@router.message(SearchFlight.destination)
async def process_destination(message: types.Message, state: FSMContext):
    user_input = message.text.strip()
    iata_code = get_iata_code(user_input)
    if iata_code:
        await state.update_data(destination=iata_code)
        await message.answer(f"Найден аэропорт: {iata_code}")
        await message.answer("Введите дату отправления (ГГГГ-ММ-ДД):")
        await state.set_state(SearchFlight.date)
        return

@router.message(SearchFlight.date)
async def process_date(message: types.Message, state: FSMContext):
    date_text = message.text.strip()
    if not re.match(r"\d{4}-\d{2}-\d{2}", date_text):
        await message.answer("Неверный формат даты")
        return

    data = await state.get_data()
    await message.answer("Ищу билеты...")

    try:
        flights = amadeus_client.search_flights(data['origin'], data['destination'], date_text)
    except Exception as e:
        await message.answer(f"Ошибка API: {e}")
        return

    if not flights:
        await message.answer("Билеты не найдены.", reply_markup=kb.get_main_menu())
    else:
        flights_map = {f['flight_number']: f for f in flights}
        await state.update_data(search_results=flights_map)

        for ticket in flights:
            text = (
                f"<b>{ticket['airline']} {ticket['flight_number']}</b>\n"
                f"{ticket['origin']} - {ticket['destination']}\n"
                f"{ticket['price']} {ticket['currency']}"
            )
            await message.answer(
                text,
                parse_mode="HTML",
                reply_markup=kb.get_ticket_fav_kb(ticket['flight_number'])
            )
        await message.answer("Поиск завершен.", reply_markup=kb.get_main_menu())

    await state.set_state(None)