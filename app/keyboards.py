from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📸 Generate Photo"),
         KeyboardButton(text="🏕️ Photo Analysis",),],
        [KeyboardButton(text="📝 Generate Text"),]],
    resize_keyboard=True,
    input_field_placeholder="Select an option",
)
