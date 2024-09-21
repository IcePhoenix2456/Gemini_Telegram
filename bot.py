import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters.command import Command
from dotenv import load_dotenv
from aiogram import F
from gemini import gemini_chat
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

load_dotenv()

logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.getenv("BOT_API"))

dp = Dispatcher()

class ChatStates(StatesGroup):
    chat_history = State()


@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer("Привет напиши мне свой вопрос и я дам ответ.")
    await state.set_state(ChatStates.chat_history)


@dp.message(F.text)
async def cmd_chat(message: types.Message, state: FSMContext):
    chat_history = await state.get_data()
    chat_history = chat_history.get("history", [])
    response = gemini_chat(message.text, chat_history)
    await message.answer(response, parse_mode=ParseMode.MARKDOWN)
    chat_history.append({"role": "user", "parts": f"{message.text}, ответь на сообщение на русском и без markdown,"
                                                  f" за исключение кода. В ответе не упоминай, что я говорил тебе про"
                                                  f" markdown"})
    chat_history.append({"role": "model", "parts": f"{response}"})
    print(response)
    await state.update_data(history = chat_history)


@dp.message(Command("clear_context"))
async def clear_context(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Контекст очищен")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())