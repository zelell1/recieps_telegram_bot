import requests
from bs4 import BeautifulSoup
import random
from fake_useragent import UserAgent


# функция для возвращения со стороннего API картинки
def cat_pic():
    # генерируем фэйкового useragent для большей правдоподобности запроса
    ua = UserAgent()
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        'user-agent': ua.random
    }

    # ссылка на сторонний API
    url = 'https://http.cat/'
    # посылем запрос
    response = requests.get(url=url, headers=headers)
    # создаем обьект класса BeautifulSoup c парсером lxml
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
    print(cat_pic())


if __name__ == "__main__":
    main()
