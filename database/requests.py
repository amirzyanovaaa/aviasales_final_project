from database.models import async_session, User, Favorite
from sqlalchemy import select, delete


async def add_user(tg_id, username, first_name):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if not user:
            session.add(User(tg_id=tg_id, username=username, first_name=first_name))
            await session.commit()


async def add_favorite(tg_id, data):
    async with async_session() as session:
        existing = await session.scalar(
            select(Favorite).where(
                Favorite.user_tg_id == tg_id,
                Favorite.flight_number == data['flight_number'],
                Favorite.date == data['departure_date']
            )
        )
        if existing:
            return False

        new_fav = Favorite(
            user_tg_id=tg_id,
            airline=data.get('airline', ''),
            flight_number=data.get('flight_number'),
            origin=data.get('origin'),
            destination=data.get('destination'),
            date=data.get('departure_date'),
            price=float(data.get('price', 0)),
            currency=data.get('currency', 'RUB')
        )
        session.add(new_fav)
        await session.commit()
        return True


async def get_favorites(tg_id):
    async with async_session() as session:
        result = await session.scalars(select(Favorite).where(Favorite.user_tg_id == tg_id))
        return result.all()


async def delete_favorite(tg_id, ticket_id):
    async with async_session() as session:
        await session.execute(
            delete(Favorite).where(Favorite.user_tg_id == tg_id, Favorite.id == int(ticket_id))
        )
        await session.commit()
        return True

