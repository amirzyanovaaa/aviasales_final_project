from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
import keyboards as kb

from database.requests import add_user

router = Router()


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    user = message.from_user

    await add_user(user.id, user.username, user.first_name)
    await message.answer(
        f"Привет, {user.first_name}! \nВыберите действие:",
        reply_markup=kb.get_main_menu()
    )

@router.message(F.text == "Назад в меню")
async def back_to_menu(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Главное меню", reply_markup=kb.get_main_menu())