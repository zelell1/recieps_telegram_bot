import requests
from bs4 import BeautifulSoup
import random


# функция для возвращения со стороннего API картинки
def cat_pic(headers):
    # ссылка на сторонний API
    url = 'https://http.cat/'
    # посылаем запрос
    response = requests.get(url=url, headers=headers)
    # создаем объект класса BeautifulSoup c парсером lxml
    soup = BeautifulSoup(response.text, 'lxml')
    # собираем все номера ошибок с карточек
    cards = soup.find_all("div", class_="Thumbnail_title__2iqYK")
    # список со всеми ошибками
    cards_dict = []

    # проходимся по каждой карточке
    for i in cards:
        # вычленяем номер ошибки из div-блоков
        nums = str(i)[str(i).find('>') + 1:str(i).find('</div>')]
        # добавляем в список 
        cards_dict.append(nums)
    # возвращаем рандомный номер ошибки
    return cards_dict[random.randint(0, len(cards))]


def main():
    pass


if __name__ == "__main__":
    main()
