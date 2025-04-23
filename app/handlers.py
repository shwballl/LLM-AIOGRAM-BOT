import logging
import aiohttp
import os


from aiogram import F, Router, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from utils.ai import generate_image, generate_text_from_image_response, generate_text_response
from .keyboards import main_keyboard

router = Router()

class FormText(StatesGroup):
    text = State()

class FormImage(StatesGroup):
    text = State()
    image = State()
    
class FormGeneratePhoto(StatesGroup):
    text = State()

@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer("Hello! I'm LLM-AIOGRAM-BOT. How can I assist you today?", reply_markup=main_keyboard)
    


# ======================== TEXT GENERATION ========================
@router.message(F.text == '📝 Generate Text')
async def generate_text(message: Message, state: FSMContext) -> None:
    await state.set_state(FormText.text)
    await message.answer("Send me a text prompt and I'll generate a response.")

@router.message(FormText.text)
async def process_text(message: Message, state: FSMContext) -> None:
    await state.update_data(text=message.text)
    text = message.text
    
    # Send typing status to indicate processing
    await message.answer("Generating response...")
    
    response = generate_text_response(text)
    await message.answer(response)
    await state.clear()
    

# ======================== PHOTO ANALYSIS ========================
@router.message(F.text == '🏕️ Photo Analysis')
async def generate_from_photo(message: Message, state: FSMContext) -> None:
    await state.set_state(FormImage.image)
    await message.answer("Send me a photo.")

@router.message(FormImage.image, F.photo)
async def process_image(message: Message, state: FSMContext, bot: Bot) -> None:
    # Get the highest quality photo (last in the list)
    photo = message.photo[-1]
    file_id = photo.file_id
    
    await state.update_data(file_id=file_id)
    await message.answer("Send me a text prompt about this image.")
    await state.set_state(FormImage.text)

@router.message(FormImage.text)
async def process_image_text(message: Message, state: FSMContext, bot: Bot) -> None:
    # Get the data from state
    data = await state.get_data()
    file_id = data.get("file_id")
    text = message.text
    
    # Notify the user that processing has started
    await message.answer("Processing your image, please wait...")
    
    try:
        # Get file info from Telegram
        file = await bot.get_file(file_id)
        file_path = file.file_path
        
        # Create a direct URL to the file on Telegram's servers
        file_url = f"https://api.telegram.org/file/bot{bot.token}/{file_path}"
        
        # Process using the URL
        response = generate_text_from_image_response(text, file_url, is_local_file=False)
        
        # Send the response
        await message.answer(response)
    except Exception as e:
        await message.answer(f"Sorry, there was an error processing your image: {str(e)}")
    finally:
        await state.clear()


# ======================== PHOTO GENERATION ========================
@router.message(F.text == '📸 Generate Photo')
async def generate_photo(message: Message, state: FSMContext) -> None:
    await state.set_state(FormGeneratePhoto.text)
    await message.answer("Send me a text prompt and I'll generate a photo.")



@router.message(FormGeneratePhoto.text)
async def process_generate_photo_from_text(message: Message, state: FSMContext) -> None:
    await state.update_data(text=message.text)
    text = message.text

    await message.answer("Generating photo...")

    try:
        image_urls = generate_image(text)
        image_url = image_urls["image_url"]["url"]
        logging.info(f"Generated image URL: {image_url}")
    except Exception as e:
        logging.error("Failed to generate image URL: " + str(e))
        await message.answer("❌ Failed to generate image URL.")
        await state.clear()
        return

    file_path = "temp_image.jpg"

    try:
        # Скачування зображення
        async with aiohttp.ClientSession() as session:
            async with session.get(image_url) as resp:
                if resp.status != 200:
                    raise Exception("Failed to fetch image.")
                with open(file_path, 'wb') as f:
                    f.write(await resp.read())

        # Відправлення зображення
        photo = FSInputFile(file_path)
        await message.answer_photo(photo=photo)

    except Exception as e:
        logging.error(f"Error sending photo: {e}")
        await message.answer("❌ Failed to download or send image.")
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

    await state.clear()
