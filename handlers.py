from aiogram import Router, types
from aiogram.filters import Command
from aiogram import F
from database import update_quiz_index, get_quiz_index, get_user_stats, get_leaderboard
from quiz_data import quiz_data
from callbacks import get_question, reset_quiz_state
from keyboards import start_keyboard

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "📚 Добро пожаловать в квиз по Python!\n"
        "Проверьте свои знания и сравните результаты с другими участниками.\n\n"
        "Используйте /quiz для начала новой игры\n"
        "/stats - ваша статистика\n"
        "/top - таблица лидеров",
        reply_markup=start_keyboard()
    )

async def new_quiz(message):
    user_id = message.from_user.id
    await reset_quiz_state(user_id)  # Сбрасываем состояние
    await update_quiz_index(user_id, 0)
    await get_question(message, user_id)

@router.message(F.text == "Начать игру")
@router.message(Command("quiz"))
async def cmd_quiz(message: types.Message):
    await message.answer("🚀 Начинаем новый квиз! Приготовьтесь...")
    await new_quiz(message)

@router.message(Command("stats"))
async def cmd_stats(message: types.Message):
    user_id = message.from_user.id
    stats = await get_user_stats(user_id)
    
    if not stats['last_result']:
        await message.answer("📊 Вы еще не проходили квиз. Начните игру с /quiz")
        return
    
    last_score, last_total, timestamp = stats['last_result']
    best_score = stats['best_result'][0] if stats['best_result'] else 0
    
    stats_text = (
        f"📊 <b>Ваша статистика</b>\n"
        f"══════════════════\n"
        f"• Последний результат: <b>{last_score}/{last_total}</b>\n"
        f"• Лучший результат: <b>{best_score}/{last_total}</b>\n"
        f"• Всего попыток: <b>{stats['attempts']}</b>\n\n"
        f"<i>Последняя попытка: {timestamp}</i>"
    )
    
    await message.answer(stats_text, parse_mode="HTML")

@router.message(Command("top"))
async def cmd_top(message: types.Message):
    leaderboard = await get_leaderboard()
    
    if not leaderboard:
        await message.answer("🏆 Таблица лидеров пуста. Будьте первым!")
        return
    
    leaderboard_text = "🏆 <b>Топ-10 игроков</b>\n══════════════════\n"
    
    for i, (username, full_name, score, total) in enumerate(leaderboard, 1):
        leaderboard_text += (
            f"{i}. {full_name} ({username})\n"
            f"   ⭐ <b>{score}/{total}</b> ({(score/total*100):.1f}%)\n\n"
        )
    
    await message.answer(leaderboard_text, parse_mode="HTML")