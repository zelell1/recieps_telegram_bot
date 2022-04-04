import requests
from bs4 import BeautifulSoup
import json


# функция для сбора с сайта по виду блюд
def get_type_recipes(url, headers):
    # посылаем запрос
    response = requests.get(url=url, headers=headers)
    # создаем об]ект класса BeautifulSoup c парсером lxml
    soup = BeautifulSoup(response.text, 'lxml')
    # список блюд по их видам
    all_recipes = []
    # находим таблицу со всеми тегами dl с классом catalogue
    recipes_imp = soup.find("table", class_='rcpf').find_all('dl', class_="catalogue")

    # проходимся по размеру таблицы, т.к на сайте она разбита на две внутри лежащих
    for j in range(len(recipes_imp)):
        for i in range(len(recipes_imp[j].find_all('dt')[:])):
            # собираем нужную информацию
            recipes_name = recipes_imp[j].find_all('dt')[i]
            recipes_name_href = "https://www.russianfood.com" + str(recipes_name)[
                                                                str(recipes_name).find('href="') + 6:str(
                                                                    recipes_name).find('">')]
            recipes_names = recipes_imp[j].find_all('dd')[i]
            recipes = {
                'group_recipes': str(recipes_name.text),
                'group_recipes_href': recipes_name_href,
                'all_recipes': []
            }
            for elem in recipes_names:
                if elem.text != ", " and elem.text != " ":
                    recipes['all_recipes'].append({
                        'name': str(elem.text),
                        "href": "https://www.russianfood.com" + str(elem)[
                                                                str(elem).find('href="') + 6:str(elem).find('">')]
                    })
            all_recipes.append(recipes)

            # записываем в json
            with open("jsons/type_recipes.json", 'w', encoding='utf-8') as js:
                json.dump(all_recipes, js, ensure_ascii=True)
    # возвращаем путь до json-а
    return 'jsons/type_recipes.json'


def main():
    pass


if __name__ == "__main__":
    main()
