from aiogram import Router, types
from aiogram.filters import Command
from aiogram import F
from database import update_quiz_index, get_quiz_index
from keyboards import start_keyboard
from quiz_data import quiz_data
from callbacks import get_question

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Добро пожаловать в квиз!",
        reply_markup=start_keyboard()
    )

async def new_quiz(message):
    user_id = message.from_user.id
    await update_quiz_index(user_id, 0)
    await get_question(message, user_id)

@router.message(F.text == "Начать игру")
@router.message(Command("quiz"))
async def cmd_quiz(message: types.Message):
    await message.answer("Давайте начнем квиз!")
    await new_quiz(message)