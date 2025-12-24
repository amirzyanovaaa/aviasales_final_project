import re
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from final_project.states import SearchFlight
from final_project.loader import amadeus_client
from final_project import keyboards as kb
from final_project.iata import find_airports_by_query, get_airport_info_by_iata


router = Router()


@router.message(F.text == "Поиск билетов")
async def start_search(message: types.Message, state: FSMContext):
    await message.answer("Введите название города вылета:")
    await state.set_state(SearchFlight.origin)


@router.message(SearchFlight.origin)
async def process_origin(message: types.Message, state: FSMContext):
    user_input = message.text.strip()
    founded_airports = find_airports_by_query(user_input)
    if not founded_airports:
        await message.answer("Город отправления не поддерживается. Выберите другой город:")
        return
    if len(founded_airports) == 1:
        iata_code = founded_airports[0]['iata']
        await state.update_data(origin=iata_code)
        await message.answer(f"Найден аэропорт: {founded_airports[0]['name_ru']} ({iata_code})")
        await message.answer("Введите название города прибытия:")
        await state.set_state(SearchFlight.destination)
    else:
        await state.update_data(matched_airports=founded_airports)
        keyboard = kb.get_airports_chosen(founded_airports)
        await message.answer(
            f"Найдено несколько аэропортов. Выберите нужный:",
            reply_markup=keyboard
        )
        await state.set_state(SearchFlight.select_airport)


@router.callback_query(SearchFlight.select_airport, F.data.startswith("airport_"))
async def process_airport_selection(callback: types.CallbackQuery, state: FSMContext):
    iata_code = callback.data.replace("airport_", "")
    data = await state.get_data()
    matched_airports = data.get('matched_airports', [])
    selected_airport = next(
        (airport for airport in matched_airports if airport['iata'] == iata_code),
        None
    )
    if selected_airport:
        await state.update_data(origin=iata_code)
        await callback.message.answer(
            f"Выбран аэропорт: {selected_airport['name_ru']} ({iata_code})"
        )
        await callback.message.answer("Введите название города прибытия:")
        await state.set_state(SearchFlight.destination)
    await callback.answer()

@router.message(SearchFlight.destination)
async def process_destination(message: types.Message, state: FSMContext):
    user_input = message.text.strip()
    founded_airports = find_airports_by_query(user_input)
    if not founded_airports:
        await message.answer("Город назначения не найден. Попробуйте еще раз:")
        return
    if len(founded_airports) == 1:
        iata_code = founded_airports[0]['iata']
        await state.update_data(destination=iata_code)
        await message.answer(f"Найден аэропорт: {founded_airports[0]['name_ru']}")
        await message.answer("Введите дату отправления (ГГГГ-ММ-ДД):")
        await state.set_state(SearchFlight.date)
    else:
        await state.update_data(matched_dest_airports=founded_airports)
        keyboard = kb.get_airports_chosen(founded_airports, destination=True)
        await message.answer(
            f"Найдено несколько аэропортов. Выберите нужный:",
            reply_markup=keyboard
        )
        await state.set_state(SearchFlight.select_destination_airport)


@router.callback_query(SearchFlight.select_destination_airport, F.data.startswith("dest_airport_"))
async def process_destination_airport_selection(callback: types.CallbackQuery, state: FSMContext):
    iata_code = callback.data.replace("dest_airport_", "")
    data = await state.get_data()
    matched_airports = data.get('matched_dest_airports', [])

    selected_airport = next(
        (airport for airport in matched_airports if airport['iata'] == iata_code),
        None
    )

    if selected_airport:
        await state.update_data(destination=iata_code)
        await callback.message.answer(
            f"Выбран аэропорт: {selected_airport['name_ru']}"
        )
        await callback.message.answer("Введите дату отправления (ГГГГ-ММ-ДД):")
        await state.set_state(SearchFlight.date)
    await callback.answer()

@router.message(SearchFlight.date)
async def process_date(message: types.Message, state: FSMContext):
    date_text = message.text.strip()
    if not re.match(r"\d{4}-\d{2}-\d{2}", date_text):
        await message.answer("Неверный формат даты")
        return
    from datetime import datetime
    try:
        flight_date = datetime.strptime(date_text, "%Y-%m-%d").date()
        today = datetime.now().date()
        if flight_date < today:
            await message.answer("Дата не может быть в прошлом. Введите корректную дату:")
            return
    except ValueError:
        await message.answer("Неверная дата. Используйте формат ГГГГ-ММ-ДД:")
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
                f"{ticket['price']} {ticket['currency']}\n"
                f"Количество пересадок: {ticket['transfers']}\n"

            )
            await message.answer(
                text,
                parse_mode="HTML",
                reply_markup=kb.get_ticket_fav_kb(ticket['flight_number'])
            )
        await message.answer("Поиск завершен.", reply_markup=kb.get_main_menu())

    await state.set_state(None)


@router.callback_query(F.data == "cancel_search")
async def cancel_search(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer("Поиск отменен.", reply_markup=kb.get_main_menu())
    await callback.answer()


@router.callback_query(F.data.startswith("cancel_selection"))
async def cancel_selection(callback: types.CallbackQuery, state: FSMContext):
    current_state = await state.get_state()

    if current_state == SearchFlight.select_airport.state:
        await callback.message.answer("Выбор аэропорта отправления отменен. Введите город вылета:")
        await state.set_state(SearchFlight.origin)
    elif current_state == SearchFlight.select_destination_airport.state:
        await callback.message.answer("Выбор аэропорта назначения отменен. Введите город прибытия:")
        await state.set_state(SearchFlight.destination)
    else:
        await state.clear()
        await callback.message.answer("Действие отменено.", reply_markup=kb.get_main_menu())

    await callback.answer()

