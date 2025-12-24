import pytest
from unittest.mock import patch
from database.requests import add_user, add_favorite, get_favorites, delete_favorite
from database.models import User, Favorite
from sqlalchemy import select

class MockSessionContext:
    def __init__(self, session):
        self.session = session

    async def __aenter__(self):
        return self.session

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

@pytest.mark.asyncio
async def test_add_user_success(db_session):
    with patch('final_project.database.requests.async_session') as mock_maker:
        mock_maker.return_value = MockSessionContext(db_session)
        await add_user(123, "testuser", "Ivan")
        res = await db_session.execute(select(User).where(User.tg_id == 123))
        user = res.scalar_one()
        assert user.username == "testuser"
        assert user.first_name == "Ivan"

@pytest.mark.asyncio
async def test_add_favorite_logic(db_session):
    with patch('final_project.database.requests.async_session') as mock_maker:
        mock_maker.return_value = MockSessionContext(db_session)

        ticket_data = {
            'airline': 'SU',
            'flight_number': 'SU100',
            'origin': 'MOW',
            'destination': 'LED',
            'departure_date': '2024-12-31',
            'price': 5000.0,
            'currency': 'RUB'
        }

        result1 = await add_favorite(123, ticket_data)
        assert result1 is True
        result2 = await add_favorite(123, ticket_data)
        assert result2 is False

@pytest.mark.asyncio
async def test_delete_favorite(db_session):
    with patch('final_project.database.requests.async_session') as mock_maker:
        mock_maker.return_value = MockSessionContext(db_session)
        fav = Favorite(user_tg_id=999, airline="S7", flight_number="S777", origin="A", destination="B", date="2024",
                       price=100, currency="RUB")
        db_session.add(fav)
        await db_session.commit()
        assert len(await get_favorites(999)) == 1
        await delete_favorite(999, fav.id)
        assert len(await get_favorites(999)) == 0