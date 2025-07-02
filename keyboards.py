from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

def start_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="Начать игру"))
    return builder.as_markup(resize_keyboard=True)

def generate_options_keyboard(options):
    builder = InlineKeyboardBuilder()
    
    for idx, option in enumerate(options):
        # Используем префикс answer_ и индекс варианта
        builder.add(InlineKeyboardButton(
            text=option,
            callback_data=f"answer_{idx}"  # Сохраняем индекс выбранного варианта
        ))
    
    builder.adjust(1)
    return builder.as_markup()