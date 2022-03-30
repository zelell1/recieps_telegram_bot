from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import json
import flag
import emoji

from aiogram.utils.callback_data import CallbackData
from aiogram.utils.markdown import code

from country_recipes_parser import get_country_recipes
from type_recipes_parser import get_type_recipes
from dishes_recipes_parser import get_dishes_recipes

from aiogram.types import ReplyKeyboardRemove, CallbackQuery
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

type_recipes_callback = CallbackData("Recipes", "recipe_type")
show_type_recipes_callback = CallbackData("Type_recipes", "group_name")


@dp.message_handler(commands=['help'])
async def helping(message: types.Message):
    await message.answer("это бот кулинар")


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text=f"""Рецепты от создателей
{emoji.emojize(':floppy_disk:', language='alias')} {emoji.emojize(':iphone:', language='alias')}
{emoji.emojize(':fax:', language='alias')} {emoji.emojize(':computer:', language='alias')}
{emoji.emojize(':cd:', language='alias')}""", callback_data="creators_recipes"))
    keyboard.add(types.InlineKeyboardButton(
        text=f"""Выбор национального рецепта {flag.flag('RU')} {flag.flag('GB')} {flag.flag('FR')} {flag.flag('JP')}
{flag.flag('DE')}""", callback_data="national_recipes"))
    keyboard.add(types.InlineKeyboardButton(
        text=f"""Выбор рецепта по продуктам {emoji.emojize(':green_apple:', language='alias')}
{emoji.emojize(':grapes:', language='alias')} {emoji.emojize(':cherries:', language='alias')}
{emoji.emojize(':pear:', language='alias')} {emoji.emojize(':tangerine:', language='alias')}""",
        callback_data="food_recipes"))
    keyboard.add(types.InlineKeyboardButton(text=f"""Выбор рецепта по видам блюд 
{emoji.emojize(':meat_on_bone:', language='alias')} {emoji.emojize(':pizza:', language='alias')} 
{emoji.emojize(':rice:', language='alias')} {emoji.emojize(':hamburger:', language='alias')}
{emoji.emojize(':icecream:', language='alias')}""", callback_data="type_recipes"))
    await message.answer(f"Нажмите на кнопку, представленную ниже {emoji.emojize(':arrow_down:', language='alias')}",
                         reply_markup=keyboard)


@dp.callback_query_handler(text="back")
async def back(call: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text=f"""Рецепты от создателей
{emoji.emojize(':floppy_disk:', language='alias')} {emoji.emojize(':iphone:', language='alias')}
{emoji.emojize(':fax:', language='alias')} {emoji.emojize(':computer:', language='alias')}
{emoji.emojize(':cd:', language='alias')}""", callback_data="creators_recipes"))
    keyboard.add(types.InlineKeyboardButton(
        text=f"""Выбор национального рецепта {flag.flag('RU')} {flag.flag('GB')} {flag.flag('FR')} {flag.flag('JP')}
{flag.flag('DE')}""", callback_data="national_recipes"))
    keyboard.add(types.InlineKeyboardButton(
        text=f"""Выбор рецепта по продуктам {emoji.emojize(':green_apple:', language='alias')}
{emoji.emojize(':grapes:', language='alias')} {emoji.emojize(':cherries:', language='alias')}
{emoji.emojize(':pear:', language='alias')} {emoji.emojize(':tangerine:', language='alias')}""",
        callback_data="food_recipes"))
    keyboard.add(types.InlineKeyboardButton(text=f"""Выбор рецепта по видам блюд 
{emoji.emojize(':meat_on_bone:', language='alias')} {emoji.emojize(':pizza:', language='alias')} 
{emoji.emojize(':rice:', language='alias')} {emoji.emojize(':hamburger:', language='alias')}
{emoji.emojize(':icecream:', language='alias')}""", callback_data="type_recipes"))
    await call.message.answer(f"""Вы вернулись на главную панель выбора 
Нажмите на кнопку, представленную ниже {emoji.emojize(':arrow_down:', language='alias')}""", reply_markup=keyboard)


@dp.callback_query_handler(text="creators_recipes")
async def creators_recipes(call: types.CallbackQuery):
    await call.message.answer('Q')


@dp.callback_query_handler(text="national_recipes")
async def national_recipes(call: types.CallbackQuery):
    nat_keyboard = types.InlineKeyboardMarkup()
    with open(get_country_recipes("https://www.russianfood.com/recipes/")) as country_json:
        data = json.load(country_json)
    for elem in data:
        for country in elem['all_recipes']:
            nat_keyboard.add(types.InlineKeyboardButton(text=f"{country['name']}", callback_data="creators_recipes"))
    nat_keyboard.add(types.InlineKeyboardButton(text="BACK", callback_data="back"))
    await call.message.answer("Выберете страну из списка:", reply_markup=nat_keyboard)


@dp.callback_query_handler(text="food_recipes")
async def food_recipes(call: types.CallbackQuery):
    food_keyboard = types.InlineKeyboardMarkup()
    with open(get_dishes_recipes("https://www.russianfood.com/recipes/")) as food_json:
        data = json.load(food_json)
    for elem in data:
        food_keyboard.add(types.InlineKeyboardButton(text=f"{elem['type_recipes']}",
                                                     callback_data="creators_recipes"))
    food_keyboard.add(types.InlineKeyboardButton(text="BACK", callback_data="back"))
    await call.message.answer("Выберете продукт, из которого вы хотите приготовить блюдо", reply_markup=food_keyboard)


@dp.callback_query_handler(type_recipes_callback.filter())
async def send_answer(query: CallbackQuery, callback_data: dict):
    rec_type_keyboard = types.InlineKeyboardMarkup()
    with open(get_type_recipes("https://www.russianfood.com/recipes/")) as type_json:
        data = json.load(type_json)
    for elem in data:
        if elem['group_recipes'] == callback_data.get("recipe_type"):
            for recipe in elem['all_recipes']:
                rec_type_keyboard.add(types.InlineKeyboardButton(text=f"{recipe['name']}",
                                                                 callback_data=show_type_recipes_callback.new(
                                                                     group_name=str(recipe['href'].split('?')[1]))))
    rec_type_keyboard.add(types.InlineKeyboardButton(text="BACK", callback_data="back"))
    await query.message.answer(f"{callback_data.get('recipe_type')}", reply_markup=rec_type_keyboard)


@dp.callback_query_handler(show_type_recipes_callback.filter())
async def send_answer(query: CallbackQuery, callback_data: dict):
    button_markup = InlineKeyboardMarkup().add(
        InlineKeyboardButton(f"{emoji.emojize(':arrow_left:', language='alias')}",
                             callback_data=f"previous:0:{callback_data.get('group_name')}"),
        InlineKeyboardButton("1", callback_data="null"),
        InlineKeyboardButton(f"{emoji.emojize(':arrow_right:', language='alias')}",
                             callback_data=f"next:2:{callback_data.get('group_name')}")
    )
    await query.message.answer(f"https://www.russianfood.com/recipes/bytype/?{callback_data.get('group_name')}",
                               reply_markup=button_markup)


@dp.callback_query_handler(text_startswith="previous")
async def prev_page(query: CallbackQuery):
    await query.answer()
    data = int(query.data.split(":")[1])
    if data > 0:
        button_markup = InlineKeyboardMarkup().add(
            InlineKeyboardButton(f"{emoji.emojize(':arrow_left:', language='alias')}",
                                 callback_data=f"previous:{data - 1}:{query.data.split(':')[2]}"),
            InlineKeyboardButton(str(data), callback_data="null"),
            InlineKeyboardButton(f"{emoji.emojize(':arrow_right:', language='alias')}",
                                 callback_data=f"next:{data + 1}:{query.data.split(':')[2]}"),
        )
        await query.message.edit_text(f"https://www.russianfood.com/recipes/bytype/?{query.data.split(':')[2]}",
                                      reply_markup=button_markup)


@dp.callback_query_handler(text_startswith="next")
async def next_page(query: CallbackQuery):
    await query.answer()
    data = int(query.data.split(":")[1])

    button_markup = InlineKeyboardMarkup().add(
        InlineKeyboardButton(f"{emoji.emojize(':arrow_left:', language='alias')}",
                             callback_data=f"previous:{data - 1}:{query.data.split(':')[2]}"),
        InlineKeyboardButton(str(data), callback_data="null"),
        InlineKeyboardButton(f"{emoji.emojize(':arrow_right:', language='alias')}",
                             callback_data=f"next:{data + 1}:{query.data.split(':')[2]}"),
    )
    await query.message.edit_text(f"https://www.russianfood.com/recipes/bytype/?{query.data.split(':')[2]}",
                                  reply_markup=button_markup)


@dp.callback_query_handler(text="type_recipes")
async def type_recipes(call: types.CallbackQuery):
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
