from aiogram.fsm.state import State, StatesGroup


class SearchFlight(StatesGroup):
    origin = State()
    destination = State()
    date = State()


class CheckBooking(StatesGroup):
    booking_code = State()
