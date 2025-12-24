from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from database.requests import add_favorite, get_favorites, delete_favorite
import keyboards as kb

router = Router()


@router.callback_query(F.data.startswith("add_fav:"))
async def callback_add_fav(callback: types.CallbackQuery, state: FSMContext):
    flight_number = callback.data.split(":")[1]

    data = await state.get_data()
    search_results = data.get('search_results', {})
    ticket = search_results.get(flight_number)

    if ticket:
        success = await add_favorite(callback.from_user.id, ticket)
        if success:
            await callback.answer("Билет добавлен в избранное! ")
        else:
            await callback.answer("Этот билет уже в избранном ️")
    else:
        await callback.answer("Данные устарели, повторите поиск ")


@router.message(F.text == "Избранное")
async def show_favorites(message: types.Message):
    favorites = await get_favorites(message.from_user.id)

    if not favorites:
        await message.answer("У вас пока нет избранных билетов.")
        return

    await message.answer(f"Ваши сохраненные билеты ({len(favorites)}):")

    for fav in favorites:
        text = (
            f" <b>{fav.airline} {fav.flight_number}</b>\n"
            f" {fav.date} | {fav.origin} -> {fav.destination}\n"
            f" {fav.price} {fav.currency}"
        )
        del_kb = kb.get_delete_fav_kb(fav.id)
        await message.answer(text, parse_mode="HTML", reply_markup=del_kb)


@router.callback_query(F.data.startswith("del_fav:"))
async def callback_del_fav(callback: types.CallbackQuery):
    ticket_id = callback.data.split(":")[1]
    await delete_favorite(callback.from_user.id, ticket_id)

    await callback.message.delete()
    await callback.answer("Удалено")
