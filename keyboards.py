from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.types import InlineKeyboardButton, KeyboardButton

def start_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="Начать игру"))
    return builder.as_markup(resize_keyboard=True)

def generate_options_keyboard(options, correct_index):
    builder = InlineKeyboardBuilder()
    
    for idx, option in enumerate(options):
        callback_data = "right_answer" if idx == correct_index else "wrong_answer"
        builder.add(InlineKeyboardButton(
            text=option,
            callback_data=callback_data
        ))
    
    builder.adjust(1)
    return builder.as_markup()