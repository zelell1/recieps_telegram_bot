import requests
from bs4 import BeautifulSoup
import json


def get_dishes_recipes(url):
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36'
    }
    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    all_recipes = []
    recipes_imp = soup.find_all("table", class_='rcpf')[6].find_all('dl', class_="catalogue")
    for j in range(len(recipes_imp)):
        for i in range(len(recipes_imp[j].find_all('dt')[:])):
            recipes_name = recipes_imp[j].find_all('dt')[i]
            recipes_name_href = "https://www.russianfood.com" + str(recipes_name)[
                                                                 str(recipes_name).find('href="') + 6:str(
                                                                     recipes_name).find('">')]
            recipes = {
                'type_recipes': str(recipes_name.text),
                'type_recipes_href': recipes_name_href,
            }

            all_recipes.append(recipes)
            with open("jsons/dishes_recipes.json", 'w', encoding='utf-8') as js:
                json.dump(all_recipes, js, ensure_ascii=False)
    return "jsons/dishes_recipes.json"


def main():
    get_recipes(url="https://www.russianfood.com/recipes/")


if __name__ == "__main__":
    main()
