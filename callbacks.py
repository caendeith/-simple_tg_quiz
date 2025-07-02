from aiogram import Router, types
from aiogram import F
from database import update_quiz_index, get_quiz_index
from quiz_data import quiz_data
from keyboards import generate_options_keyboard

router = Router()

@router.callback_query(F.data == "right_answer")
async def right_answer(callback: types.CallbackQuery):
    await handle_answer(callback, is_correct=True)

@router.callback_query(F.data == "wrong_answer")
async def wrong_answer(callback: types.CallbackQuery):
    await handle_answer(callback, is_correct=False)

async def handle_answer(callback: types.CallbackQuery, is_correct: bool):
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )
    
    user_id = callback.from_user.id
    current_index = await get_quiz_index(user_id)
    
    if is_correct:
        await callback.message.answer("Верно!")
    else:
        correct_option = quiz_data[current_index]['correct_option']
        await callback.message.answer(
            f"Неправильно. Правильный ответ: {quiz_data[current_index]['options'][correct_option]}"
        )
    
    current_index += 1
    await update_quiz_index(user_id, current_index)
    
    if current_index < len(quiz_data):
        await get_question(callback.message, user_id)
    else:
        await callback.message.answer("Это был последний вопрос. Квиз завершен!")

async def get_question(message: types.Message, user_id: int):
    current_index = await get_quiz_index(user_id)
    question = quiz_data[current_index]
    await message.answer(
        question['question'],
        reply_markup=generate_options_keyboard(
            question['options'], 
            question['correct_option']
        )
    )