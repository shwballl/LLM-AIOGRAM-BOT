from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

reply_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Help")],
                                         [KeyboardButton(text="Start chat")]],
                               resize_keyboard=True,
                               input_field_placeholder="Chose menu option...")


