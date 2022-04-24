# импорт необходимых вещей из библиотеки aiogram
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

# импорт прочих необходимых библиотек
import json
import flag
import emoji
from math import ceil

# импорт необходимых функций из parser - ов
# from country_recipes_parser import get_country_recipes
# from type_recipes_parser import get_type_recipes
# from dishes_recipes_parser import get_dishes_recipes
from filter_parser import get_card, get_cards
from test import main, show_href

# импорт TOKEN из отдельного файла
from config import TOKEN

# создание бота и подключение TOKEN
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# создание необходимых callback - ов
type_recipes_callback = CallbackData("Recipes", "recipe_type")
show_type_recipes_callback = CallbackData("Type_recipes", "group_name")
food_recipes_callback = CallbackData("Food_recipes", "iterator")
country_recipes_callback = CallbackData("Country_recipes", "letter")
photo_recipes_callback = CallbackData("Country_recipes", "href", "page")
fav_recipes_callback = CallbackData("Fav_recipes", "href")

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36'
}


@dp.message_handler(commands=['help'])  # функция вызова сообщения с помощью
async def helping(message: types.Message):
    await message.answer(f"""{emoji.emojize(':small_blue_diamond:', language='alias')} <strong>Это бот поиска \
идеальных рецептов.</strong>
Чтобы начать им пользоваться, вам нужно набрать команду
<u>/start</u> и выбрать одну из четырех категорий. После этого
(в зависимости от категории) вам предложиться несколько
ступеней фильтрации. Затем вы сможете посмотреть интересующие вас рецепты. Также, набрав команду
<u>/creators</u>, вы сможете посмотреть разработчиков этого бота 
Приятного использования {emoji.emojize(':wink:', language='alias')} """, parse_mode="HTML")


@dp.message_handler(commands=['creators'])  # функция вызова сообщения со списком создателей
async def helping(message: types.Message):
    await message.answer(f"""Создатели этот Repi:
    
<strong>{emoji.emojize(':large_orange_diamond:', language='alias')} Арсений Артеменко</strong>

<strong>{emoji.emojize(':large_blue_diamond:', language='alias')}Даниил Лазимов</strong>""", parse_mode="HTML")


@dp.message_handler(commands=["start"])  # функция вызова стартового сообщения
async def start(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(
        text=f"""{flag.flag('RU')} {flag.flag('GB')} Выбор национального рецепта {flag.flag('FR')} {flag.flag('JP')}""",
        callback_data="national_recipes"))
    keyboard.add(types.InlineKeyboardButton(
        text=f"""{emoji.emojize(':green_apple:', language='alias')}
{emoji.emojize(':grapes:', language='alias')} Выбор рецепта по продуктам {emoji.emojize(':cherries:', language='alias')} 
{emoji.emojize(':tangerine:', language='alias')}""", callback_data="food_recipes"))
    keyboard.add(types.InlineKeyboardButton(text=f"""
{emoji.emojize(':meat_on_bone:', language='alias')} {emoji.emojize(':pizza:', language='alias')}
Выбор рецепта по видам блюд {emoji.emojize(':hamburger:', language='alias')}
{emoji.emojize(':icecream:', language='alias')}""", callback_data="type_recipes"))
    keyboard.add(types.InlineKeyboardButton(text=f"""{emoji.emojize(':heart:', language='alias')} 
{emoji.emojize(':blue_heart:', language='alias')} Понравившиеся вам блюда
{emoji.emojize(':purple_heart:', language='alias')} {emoji.emojize(':yellow_heart:', language='alias')}""",
                                            callback_data="favourite_recipes"))
    await message.answer(f"""{emoji.emojize(':small_orange_diamond:', language='alias')} \
<strong>Добро пожаловать в REPI.</strong>
Это бот-помощник, который поможет вам найти <u>идеальные рецепты блюд</u>. Вы можете воспользоваться
категориями представленными ниже для нахождения <u>конкретных блюд</u> или <u>сужения круга поисков</u>.
Нажмите на кнопку, представленную ниже {emoji.emojize(':arrow_down:', language='alias')}""",
                         reply_markup=keyboard, parse_mode="HTML")


@dp.callback_query_handler(text="back")  # функция возврата
async def back(call: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(
        text=f"""{flag.flag('RU')} {flag.flag('GB')} Выбор национального рецепта {flag.flag('FR')} {flag.flag('JP')}""",
        callback_data="national_recipes"))
    keyboard.add(types.InlineKeyboardButton(
        text=f"""{emoji.emojize(':green_apple:', language='alias')}
{emoji.emojize(':grapes:', language='alias')} Выбор рецепта по продуктам {emoji.emojize(':cherries:', language='alias')} 
{emoji.emojize(':tangerine:', language='alias')}""", callback_data="food_recipes"))
    keyboard.add(types.InlineKeyboardButton(text=f"""
{emoji.emojize(':meat_on_bone:', language='alias')} {emoji.emojize(':pizza:', language='alias')}
Выбор рецепта по видам блюд {emoji.emojize(':hamburger:', language='alias')}
{emoji.emojize(':icecream:', language='alias')}""", callback_data="type_recipes"))
    keyboard.add(types.InlineKeyboardButton(text=f"""{emoji.emojize(':heart:', language='alias')} 
{emoji.emojize(':blue_heart:', language='alias')} Понравившиеся вам блюда
{emoji.emojize(':purple_heart:', language='alias')} {emoji.emojize(':yellow_heart:', language='alias')}""",
                                            callback_data="favourite_recipes"))
    await call.message.answer(f"""Вы вернулись на главную панель выбора 
Нажмите на кнопку, представленную ниже {emoji.emojize(':arrow_down:', language='alias')}""", reply_markup=keyboard)


@dp.callback_query_handler(text="national_recipes")  # функция вывода алфавита стран
async def national_recipes(call: types.CallbackQuery):
    nat_keyboard = types.InlineKeyboardMarkup()
    with open('jsons/country_recipes.json') as country_json:
        data = json.load(country_json)
    for elem in data:
        nat_keyboard.add(types.InlineKeyboardButton(text=f"{elem['group_recipes']}",
                                                    callback_data=country_recipes_callback.new(
                                                        letter=elem['group_recipes'])))
    nat_keyboard.add(types.InlineKeyboardButton(text="BACK", callback_data="back"))
    await call.message.answer("Выберете первую букву той страны,\n рецепт которой вы хотите найти:",
                              reply_markup=nat_keyboard)


@dp.callback_query_handler(country_recipes_callback.filter())  # функция вывода стран на выбранную букву
async def send_answer(query: CallbackQuery, callback_data: dict):
    cntr_type_keyboard = types.InlineKeyboardMarkup()
    with open('jsons/country_recipes.json') as type_json:
        data = json.load(type_json)
    for elem in data:
        if elem['group_recipes'] == callback_data.get("letter"):
            for recipe in elem['all_recipes']:
                cntr_type_keyboard.add(types.InlineKeyboardButton(text=f"{recipe['name']}",
                                                                  callback_data=show_type_recipes_callback.new(
                                                                      group_name=str(recipe['href'].split('?')[1]))))
    cntr_type_keyboard.add(types.InlineKeyboardButton(text="BACK", callback_data="back"))
    await query.message.answer(f"Выберете страну из списка:", reply_markup=cntr_type_keyboard)


@dp.callback_query_handler(text="food_recipes")  # функция вывода продуктов, из которых можно что-то приготовить
async def food_recipes(call: types.CallbackQuery):
    food_keyboard = types.InlineKeyboardMarkup()
    with open('jsons/dishes_recipes.json') as food_json:
        data = json.load(food_json)
    iterator = ceil(len(data) / 10)
    for elem in data[:iterator]:
        food_keyboard.add(types.InlineKeyboardButton(text=f"{elem['type_recipes']}",
                                                     callback_data=show_type_recipes_callback.new(
                                                         group_name=str(elem['type_recipes_href'].split('?')[1]))))
    food_keyboard.add(types.InlineKeyboardButton(text="BACK", callback_data="back"))
    food_keyboard.add(
        InlineKeyboardButton(f"{emoji.emojize(':arrow_left:', language='alias')}",
                             callback_data=f"prv:0:{iterator}"),
        InlineKeyboardButton("1", callback_data="null"),
        InlineKeyboardButton(f"{emoji.emojize(':arrow_right:', language='alias')}",
                             callback_data=f"nxt:2:{iterator}")
    )
    food_keyboard.add(types.InlineKeyboardButton(text="BACK", callback_data="back"))
    await call.message.answer(
        f"Выберете продукт, из которого вы хотите приготовить блюдо{emoji.emojize(':arrow_down:', language='alias')}",
        reply_markup=food_keyboard)


@dp.callback_query_handler(text_startswith="prv")  # функция пролистывания назад страниц со списком продуктов
async def prv_page(query: CallbackQuery):
    await query.answer()
    button_markup = InlineKeyboardMarkup()
    data = int(query.data.split(":")[1])
    with open('jsons/dishes_recipes.json') as food_json:
        file = json.load(food_json)
    if data > 0:
        for elem in file[
                    int(query.data.split(':')[2]) * (int(query.data.split(":")[1]) - 1):int(
                        query.data.split(':')[2]) * int(query.data.split(":")[1])]:
            button_markup.add(types.InlineKeyboardButton(text=f"{elem['type_recipes']}",
                                                         callback_data=show_type_recipes_callback.new(
                                                             group_name=str(elem['type_recipes_href'].split('?')[1]))))
        button_markup.add(types.InlineKeyboardButton(text="BACK", callback_data="back"))
        button_markup.add(
            InlineKeyboardButton(f"{emoji.emojize(':arrow_left:', language='alias')}",
                                 callback_data=f"prv:{data - 1}:{query.data.split(':')[2]}"),
            InlineKeyboardButton(str(data), callback_data="null"),
            InlineKeyboardButton(f"{emoji.emojize(':arrow_right:', language='alias')}",
                                 callback_data=f"nxt:{data + 1}:{query.data.split(':')[2]}"),
        )
        button_markup.add(types.InlineKeyboardButton(text="BACK", callback_data="back"))
        await query.message.edit_text(
            f"Выберете продукт,\
из которого вы хотите приготовить блюдо{emoji.emojize(':arrow_down:', language='alias')}",
            reply_markup=button_markup)


@dp.callback_query_handler(text_startswith="nxt")  # функция пролистывания вперед страниц со списком продуктов
async def nxt_page(query: CallbackQuery):
    await query.answer()
    button_markup = InlineKeyboardMarkup()
    data = int(query.data.split(":")[1])
    with open('jsons/dishes_recipes.json') as food_json:
        file = json.load(food_json)
    if int(query.data.split(":")[2]) * (int(query.data.split(":")[1]) - 1) <= len(file):
        for elem in file[
                    int(query.data.split(':')[2]) * (int(query.data.split(":")[1]) - 1):int(
                        query.data.split(':')[2]) * int(query.data.split(":")[1])]:
            button_markup.add(types.InlineKeyboardButton(text=f"{elem['type_recipes']}",
                                                         callback_data=show_type_recipes_callback.new(
                                                             group_name=str(elem['type_recipes_href'].split('?')[1]))))
        button_markup.add(types.InlineKeyboardButton(text="BACK", callback_data="back"))
        button_markup.add(
            InlineKeyboardButton(f"{emoji.emojize(':arrow_left:', language='alias')}",
                                 callback_data=f"prv:{data - 1}:{query.data.split(':')[2]}"),
            InlineKeyboardButton(str(data), callback_data="null"),
            InlineKeyboardButton(f"{emoji.emojize(':arrow_right:', language='alias')}",
                                 callback_data=f"nxt:{data + 1}:{query.data.split(':')[2]}"),
        )
        button_markup.add(types.InlineKeyboardButton(text="BACK", callback_data="back"))
        await query.message.edit_text(
            f"Выберете продукт,\
из которого вы хотите приготовить блюдо{emoji.emojize(':arrow_down:', language='alias')}",
            reply_markup=button_markup)


@dp.callback_query_handler(type_recipes_callback.filter())  # функция вывода блюд выбранной категории
async def send_answer(query: CallbackQuery, callback_data: dict):
    rec_type_keyboard = types.InlineKeyboardMarkup()
    with open('jsons/type_recipes.json') as type_json:
        data = json.load(type_json)
    for elem in data:
        if elem['group_recipes'] == callback_data.get("recipe_type"):
            for recipe in elem['all_recipes']:
                rec_type_keyboard.add(types.InlineKeyboardButton(text=f"{recipe['name']}",
                                                                 callback_data=show_type_recipes_callback.new(
                                                                     group_name=str(recipe['href'].split('?')[1]))))
    rec_type_keyboard.add(types.InlineKeyboardButton(text="BACK", callback_data="back"))
    await query.message.answer(f"{callback_data.get('recipe_type')}", reply_markup=rec_type_keyboard)


# функция вывода страниц (вызывается из разных функций)
@dp.callback_query_handler(show_type_recipes_callback.filter())
async def send_answer(query: CallbackQuery, callback_data: dict):
    button_markup = InlineKeyboardMarkup()
    for elem in get_cards(f"https://www.russianfood.com/recipes/bytype/?{callback_data.get('group_name')}", 1, headers):
        button_markup.add(types.InlineKeyboardButton(f'{elem["name"]}', callback_data=photo_recipes_callback.new(
            page=1, href=f'{elem["href"].split("?rid=")[1]}')))
    button_markup.add(
        InlineKeyboardButton(f"{emoji.emojize(':arrow_left:', language='alias')}",
                             callback_data=f"previous:0:{callback_data.get('group_name')}"),
        InlineKeyboardButton("1", callback_data="null"),
        InlineKeyboardButton(f"{emoji.emojize(':arrow_right:', language='alias')}",
                             callback_data=f"next:2:{callback_data.get('group_name')}")
    )
    button_markup.add(types.InlineKeyboardButton(text="BACK", callback_data="back"))
    await query.message.answer(f"Выберете понравившийся рецепт", reply_markup=button_markup)


# функция вывода пролистывания страниц назад (вызывается из разных функций)
@dp.callback_query_handler(text_startswith="previous")
async def prev_page(query: CallbackQuery):
    await query.answer()
    data = int(query.data.split(":")[1])
    if data > 0:
        button_markup = InlineKeyboardMarkup()
        for elem in get_cards(f"https://www.russianfood.com/recipes/bytype/?{query.data.split(':')[2]}", data, headers):
            button_markup.add(types.InlineKeyboardButton(f'{elem["name"]}', callback_data=photo_recipes_callback.new(
                page=data, href=f'{elem["href"].split("?rid=")[1]}')))

        button_markup.add(
            InlineKeyboardButton(f"{emoji.emojize(':arrow_left:', language='alias')}",
                                 callback_data=f"previous:{data - 1}:{query.data.split(':')[2]}"),
            InlineKeyboardButton(str(data), callback_data="null"),
            InlineKeyboardButton(f"{emoji.emojize(':arrow_right:', language='alias')}",
                                 callback_data=f"next:{data + 1}:{query.data.split(':')[2]}"),
        )
        button_markup.add(types.InlineKeyboardButton(text="BACK", callback_data="back"))
        await query.message.edit_text(f"Выберете понравившийся рецепт", reply_markup=button_markup)


# функция вывода пролистывания страниц вперед (вызывается из разных функций)
@dp.callback_query_handler(text_startswith="next")
async def next_page(query: CallbackQuery):
    await query.answer()
    button_markup = InlineKeyboardMarkup()
    data = int(query.data.split(":")[1])
    for elem in get_cards(f"https://www.russianfood.com/recipes/bytype/?{query.data.split(':')[2]}", data, headers):
        button_markup.add(types.InlineKeyboardButton(f'{elem["name"]}', callback_data=photo_recipes_callback.new(
            page=data, href=f'{elem["href"].split("?rid=")[1]}')))
    button_markup.add(
        InlineKeyboardButton(f"{emoji.emojize(':arrow_left:', language='alias')}",
                             callback_data=f"previous:{data - 1}:{query.data.split(':')[2]}"),
        InlineKeyboardButton(str(data), callback_data="null"),
        InlineKeyboardButton(f"{emoji.emojize(':arrow_right:', language='alias')}",
                             callback_data=f"next:{data + 1}:{query.data.split(':')[2]}"),
    )
    button_markup.add(types.InlineKeyboardButton(text="BACK", callback_data="back"))
    await query.message.edit_text(f"Выберете понравившийся рецепт", reply_markup=button_markup)


@dp.callback_query_handler(photo_recipes_callback.filter())  # функция вывода рецептов с фото, ссылкой, рецептом и тп.
async def send_answer(query: CallbackQuery, callback_data: dict):
    button_markup = InlineKeyboardMarkup()
    lst = get_card(f"https://www.russianfood.com/recipes/recipe.php?rid={callback_data['href']}", headers)
    await bot.send_photo(query.message.chat.id, photo=f"{lst['img']}")
    await query.message.answer(f"{lst['description']}\n")
    await query.message.answer("\n".join(lst['products']))
    button_markup.add(types.InlineKeyboardButton(text="Добавить рецепт в понравившиеся",
                                                 callback_data=fav_recipes_callback.new(href=callback_data['href'])))
    await query.message.answer(f"Ссылка на подробный рецепт:\n"
                               f"https://www.russianfood.com/recipes/recipe.php?rid={callback_data['href']}",
                               reply_markup=button_markup)


@dp.callback_query_handler(text="type_recipes")  # функция вывода категорий блюд
async def type_recipes(call: types.CallbackQuery):
    type_keyboard = types.InlineKeyboardMarkup()
    with open('jsons/type_recipes.json') as type_json:
        data = json.load(type_json)
    for elem in data:
        type_keyboard.add(types.InlineKeyboardButton(text=f"{elem['group_recipes']}",
                                                     callback_data=type_recipes_callback.new(
                                                         recipe_type=f"{elem['group_recipes']}")))
    type_keyboard.add(types.InlineKeyboardButton(text="BACK", callback_data="back"))
    await call.message.answer("Выберете категорию блюда из списка", reply_markup=type_keyboard)


@dp.callback_query_handler(text="favourite_recipes")  # функция вывода понравившихся рецептов
async def type_recipes(call: types.CallbackQuery):
    button_markup = InlineKeyboardMarkup()
    button_markup.add(types.InlineKeyboardButton(text="BACK", callback_data="back"))
    try:
        await call.message.answer('\n'.join(list(
            map(lambda x: emoji.emojize(':large_orange_diamond:', language='alias') + x,
                show_href(call.from_user['id']).split(';;')[:-1]))), reply_markup=button_markup)
    except Exception:
        await call.message.answer("У вас пока что нет понравившихся рецептов", reply_markup=button_markup)


# функция вывода сообщения об успешном добавлении рецепта в понравившиеся
@dp.callback_query_handler(fav_recipes_callback.filter())
async def send_answer(query: CallbackQuery, callback_data: dict):
    button_markup = InlineKeyboardMarkup()
    main(query.from_user['id'], query.from_user['first_name'], query.from_user['last_name'],
         query.from_user['username'], f"https://www.russianfood.com/recipes/recipe.php?rid={callback_data['href']}")
    button_markup.add(types.InlineKeyboardButton(text="BACK", callback_data="back"))
    await query.message.answer(f"Этот рецепт успешно добавлен в список понравившихся\n"
                               f"https://www.russianfood.com/recipes/recipe.php?rid={callback_data['href']}",
                               reply_markup=button_markup)


if __name__ == '__main__':
    executor.start_polling(dp)
