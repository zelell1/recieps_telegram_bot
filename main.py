from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardRemove
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.answer("это бот кулинар")


@dp.message_handler(commands="start")
async def cmd_random(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Рецепты от создателей", callback_data="creators_recipes"))
    keyboard.add(types.InlineKeyboardButton(text="Выбор национального рецепта", callback_data="national_recipes"))
    keyboard.add(types.InlineKeyboardButton(text="Выбор рецепта по продуктам", callback_data="food_recipes"))
    keyboard.add(types.InlineKeyboardButton(text="Выбор рецепта по видам блюд", callback_data="type_recipes"))
    await message.answer("Нажмите на кнопку, представленную ниже", reply_markup=keyboard)


@dp.callback_query_handler(text="creators_recipes")
async def send_answer(call: types.CallbackQuery):
    await call.message.answer('Q')


@dp.callback_query_handler(text="national_recipes")
async def send_answer(call: types.CallbackQuery):
    await call.message.answer('W')


@dp.callback_query_handler(text="food_recipes")
async def send_answer(call: types.CallbackQuery):
    await call.message.answer('E')


@dp.callback_query_handler(text="type_recipes")
async def send_answer(call: types.CallbackQuery):
    await call.message.answer('R')


if __name__ == '__main__':
    executor.start_polling(dp)
