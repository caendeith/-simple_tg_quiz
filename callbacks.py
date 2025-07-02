from aiogram import Router, types
from aiogram import F
from database import update_quiz_index, get_quiz_index, save_quiz_result
from quiz_data import quiz_data
from keyboards import generate_options_keyboard

router = Router()

@router.callback_query(F.data.startswith("answer_"))
async def answer_handler(callback: types.CallbackQuery):
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )
    
    user_id = callback.from_user.id
    current_index = await get_quiz_index(user_id)
    
    # Получаем текущий счет
    current_state = await get_quiz_state(user_id)
    current_score = current_state['score'] if current_state else 0
    
    # Извлекаем выбранный индекс ответа
    selected_index = int(callback.data.split("_")[1])
    selected_option = quiz_data[current_index]['options'][selected_index]
    
    # Получаем правильный ответ
    correct_index = quiz_data[current_index]['correct_option']
    correct_option = quiz_data[current_index]['options'][correct_index]
    
    # Проверяем ответ и обновляем счет
    is_correct = selected_index == correct_index
    if is_correct:
        current_score += 1
        await update_quiz_state(user_id, {'score': current_score})
        response_text = (
            f"✅ Вы выбрали: <b>{selected_option}</b>\n"
            "Это <u>правильный</u> ответ!"
        )
    else:
        response_text = (
            f"❌ Вы выбрали: <b>{selected_option}</b>\n"
            f"Правильный ответ: <b>{correct_option}</b>"
        )
    
    await callback.message.answer(response_text, parse_mode="HTML")
    
    # Переход к следующему вопросу
    current_index += 1
    await update_quiz_index(user_id, current_index)
    
    if current_index < len(quiz_data):
        await get_question(callback.message, user_id)
    else:
        # Сохраняем результаты при завершении квиза
        username = callback.from_user.username
        full_name = callback.from_user.full_name
        await save_quiz_result(
            user_id, 
            f"@{username}" if username else "N/A", 
            full_name, 
            current_score, 
            len(quiz_data)
        )
        
        # Форматируем результаты
        result_text = (
            f"🏆 Квиз завершен!\n"
            f"══════════════════\n"
            f"Правильных ответов: <b>{current_score}/{len(quiz_data)}</b>\n"
            f"Успешность: <b>{(current_score/len(quiz_data)*100):.1f}%</b>\n\n"
            f"Для просмотра статистики используйте /stats"
        )
        await callback.message.answer(result_text, parse_mode="HTML")

async def get_question(message: types.Message, user_id: int):
    current_index = await get_quiz_index(user_id)
    question = quiz_data[current_index]
    
    # Получаем текущий счет
    current_state = await get_quiz_state(user_id)
    current_score = current_state['score'] if current_state else 0
    
    question_text = (
        f"Вопрос {current_index + 1}/{len(quiz_data)}\n"
        f"Текущий счет: {current_score}\n"
        f"────────────────\n"
        f"{question['question']}"
    )
    
    await message.answer(
        question_text,
        reply_markup=generate_options_keyboard(question['options'])
    )

# Временное хранилище состояния (можно заменить на Redis для продакшена)
user_states = {}

async def get_quiz_state(user_id):
    return user_states.get(user_id)

async def update_quiz_state(user_id, state):
    user_states[user_id] = state

async def reset_quiz_state(user_id):
    if user_id in user_states:
        del user_states[user_id]