from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import json

from aiogram.utils.callback_data import CallbackData
from aiogram.utils.markdown import code

from country_recipes_parser import get_country_recipes
from type_recipes_parser import get_type_recipes
from aiogram.types import ReplyKeyboardRemove, CallbackQuery
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

type_recipes_callback = CallbackData("Recipes", "recipe_type")


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.answer("это бот кулинар")


@dp.message_handler(commands=["start"])
async def cmd_random(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Рецепты от создателей", callback_data="creators_recipes"))
    keyboard.add(types.InlineKeyboardButton(text="Выбор национального рецепта", callback_data="national_recipes"))
    keyboard.add(types.InlineKeyboardButton(text="Выбор рецепта по продуктам", callback_data="food_recipes"))
    keyboard.add(types.InlineKeyboardButton(text="Выбор рецепта по видам блюд", callback_data="type_recipes"))
    await message.answer("Нажмите на кнопку, представленную ниже", reply_markup=keyboard)


@dp.callback_query_handler(text="back")
async def start_callback(call: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Рецепты от создателей", callback_data="creators_recipes"))
    keyboard.add(types.InlineKeyboardButton(text="Выбор национального рецепта", callback_data="national_recipes"))
    keyboard.add(types.InlineKeyboardButton(text="Выбор рецепта по продуктам", callback_data="food_recipes"))
    keyboard.add(types.InlineKeyboardButton(text="Выбор рецепта по видам блюд", callback_data="type_recipes"))
    await call.message.answer("Вы вернулись на главную панель выбора\n"
                              "Нажмите на кнопку, представленную ниже", reply_markup=keyboard)


@dp.callback_query_handler(text="creators_recipes")
async def send_answer(call: types.CallbackQuery):
    await call.message.answer('Q')


@dp.callback_query_handler(text="national_recipes")
async def send_answer(call: types.CallbackQuery):
    nat_keyboard = types.InlineKeyboardMarkup()
    with open(get_country_recipes("https://www.russianfood.com/recipes/")) as country_json:
        data = json.load(country_json)
    for elem in data:
        for country in elem['all_recipes']:
            nat_keyboard.add(types.InlineKeyboardButton(text=f"{country['name']}", callback_data="creators_recipes"))
    nat_keyboard.add(types.InlineKeyboardButton(text="BACK", callback_data="back"))
    await call.message.answer("Выберете страну из списка:", reply_markup=nat_keyboard)


@dp.callback_query_handler(text="food_recipes")
async def send_answer(call: types.CallbackQuery):
    await call.message.answer('E')


@dp.callback_query_handler(type_recipes_callback.filter())
async def fruit_page_handler(query: CallbackQuery, callback_data: dict):
    rec_type_keyboard = types.InlineKeyboardMarkup()
    with open(get_type_recipes("https://www.russianfood.com/recipes/")) as type_json:
        data = json.load(type_json)
    for elem in data:
        if elem['group_recipes'] == callback_data.get("recipe_type"):
            for recipe in elem['all_recipes']:
                rec_type_keyboard.add(types.InlineKeyboardButton(text=f"{recipe['name']}", callback_data='ДАНИЛ_ЛОХ'))
    await query.message.answer(f"{callback_data.get('recipe_type')}", reply_markup=rec_type_keyboard)


@dp.callback_query_handler(text="type_recipes")
async def send_answer(call: types.CallbackQuery):
    type_keyboard = types.InlineKeyboardMarkup()
    with open(get_type_recipes("https://www.russianfood.com/recipes/")) as type_json:
        data = json.load(type_json)
    for elem in data:
        type_keyboard.add(types.InlineKeyboardButton(text=f"{elem['group_recipes']}",
                                                     callback_data=type_recipes_callback.new(
                                                         recipe_type=f"{elem['group_recipes']}")))
    type_keyboard.add(types.InlineKeyboardButton(text="BACK", callback_data="back"))
    await call.message.answer("Выберете категорию блюда из списка", reply_markup=type_keyboard)


if __name__ == '__main__':
    executor.start_polling(dp)
