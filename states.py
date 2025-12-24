from aiogram.fsm.state import State, StatesGroup


class SearchFlight(StatesGroup):
    origin = State()
    select_airport = State()
    destination = State()
    select_destination_airport = State()
    date = State()

class CheckBooking(StatesGroup):
    booking_code = State()
