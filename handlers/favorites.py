from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from database.requests import add_favorite, get_favorites, delete_favorite
import keyboards as kb

router = Router()


@router.callback_query(F.data.startswith("add_fav:"))
async def add_fav_handler(callback: types.CallbackQuery, state: FSMContext):
    flight_number = callback.data.split(":")[1]
    data = await state.get_data()
    ticket = data.get('search_results', {}).get(flight_number)

    if ticket:
        success = await add_favorite(callback.from_user.id, ticket)
        if success:
            await callback.answer("Сохранено")
        else:
            await callback.answer("Уже есть в избранном")
    else:
        await callback.answer("Ошибка данных")


@router.message(F.text == "Избранное")
async def show_favs(message: types.Message):
    favs = await get_favorites(message.from_user.id)

    if not favs:
        await message.answer("Пусто")
        return

    for fav in favs:
        text = f"{fav.airline} {fav.flight_number}\n{fav.origin} -> {fav.destination} ({fav.date})"
        await message.answer(text, reply_markup=kb.get_delete_fav_kb(fav.id))


@router.callback_query(F.data.startswith("del_fav:"))
async def del_fav_handler(callback: types.CallbackQuery):
    ticket_id = callback.data.split(":")[1]
    await delete_favorite(callback.from_user.id, ticket_id)
    await callback.message.delete()
    await callback.answer("Удалено")