from states import SearchFlight, CheckBooking

def test_states():
    assert SearchFlight.origin
    assert SearchFlight.destination
    assert SearchFlight.date
    assert CheckBooking.booking_code