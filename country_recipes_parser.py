import requests
from bs4 import BeautifulSoup
import json


# функция для сбора с сайта блюд по национальности
def get_country_recipes(url, headers):
    # посылаем запрос
    response = requests.get(url=url, headers=headers)
    # создаем объект класса BeautifulSoup c парсером lxml
    soup = BeautifulSoup(response.text, 'lxml')
    # список со всеми блюдами по национальности
    all_recipes_for_letter = []
    # находим таблицу
    recipes_nes = soup.find("table", class_='rcpf2').find_all("table", class_='sb_nations')

    # проходимся по размеру таблицы, т.к на сайте она разбита на две внутри лежащих
    for j in range(len(recipes_nes)):
        for i in range(0, len(recipes_nes[j].find_all('td')[:]), 2):
            # собираем нужную информацию
            recipes_name = recipes_nes[j].find_all('td')[i]
            recipes_names = recipes_nes[j].find_all('td')[i + 1]
            recipes = {
                'group_recipes': str(recipes_name.text),
                'all_recipes': []
            }
            for elem in recipes_names:
                if elem.text != ", " and elem.text != " " and elem.text != '\n':
                    recipes['all_recipes'].append({
                        'name': str(elem.text),
                        "href": "https://www.russianfood.com" + str(elem)[
                                                                str(elem).find('href="') + 6:str(elem).find('">')]
                    })
            all_recipes_for_letter.append(recipes)
            
            # записываем в json
            with open("jsons/country_recipes.json", 'w', encoding='utf-8') as js:
                json.dump(all_recipes_for_letter, js, ensure_ascii=True)
    # возвращаем путь до json-а
    return 'jsons/country_recipes.json'


def main():
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36'
    }
    get_country_recipes("https://www.russianfood.com/recipes/", headers)


if __name__ == "__main__":
    main()
