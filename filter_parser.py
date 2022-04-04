import requests
from bs4 import BeautifulSoup
from cat_parser import cat_pic
from fake_useragent import UserAgent


# функция для сбора с сайта текущей страницы
def get_cards(url, page, headers):
    # генерируем url с нужной пагинацией
    url = f"{url}&page={page}#rcp_list"
    # посылем запрос
    response = requests.get(url=url, headers=headers)
    # создаем обьект класса BeautifulSoup c парсером lxml
    soup = BeautifulSoup(response.text, 'lxml')
    # находим div-блоки c классом title_o
    cards = soup.find_all("div", class_='title_o')
    # список со всеми карточками на странице
    cards_dict = []

    # проходимся по всем карточкам на странице
    for i in range(len(cards)):
        # собираем нужную информацию
        href = "https://www.russianfood.com" + str(cards[i].find('a'))[
                                               str(cards[i].find('a')).find('href="') + 6:str(cards[i].find('a')).find(
                                                   '" name=')]
        card = {
            "name": cards[i].text.strip().replace('\"', ""),
            "href": href
        }
        cards_dict.append(card)

    # сразу возвращаем список с карточками
    return cards_dict


# функция для сбора со страницы нужной карточки
def get_card(url, headers):
    # посылем запрос
    response = requests.get(url=url, headers=headers)
    # создаем обьект класса BeautifulSoup c парсером lxml
    soup = BeautifulSoup(response.text, 'lxml')
    # находим td с классом padding_l padding_r
    card = soup.find('td', class_="padding_l padding_r")
    # находим img
    img = card.find("img")
    # находим ссылку на картинку
    img_href = str(img)[str(img).find('"//'): str(img).find(' title')].replace('\"', "")
    # берем описание с карточки
    description = card.find_all('div')[-1].text
    # берем cписок продуктов, лежащий в отдельной таблице
    products = [soup.find('table', class_="ingr").find('td', class_="padding_l ingr_title").text.strip()] \
               + [i.text for i in soup.find('table', class_="ingr").find_all('span', class_="")]

    # обрабатываем ситуацию, когда нет картинки
    if img_href == '':
        # используем функцию cat_pic из cat_parser, чтобы вывести картинку со случайной ошибкой
        img_href = f'//http.cat/{cat_pic()}'
    card_now = {
        'img': f'https:{img_href}',
        'description': description,
        'products': products
    }

    # сразу возвращаем содержание карточки
    return card_now


def main():
    ua = UserAgent()
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        'user-agent': ua.random
    }
    print(get_card(url="https://www.russianfood.com/recipes/recipe.php?rid=148403", headers=headers))


if __name__ == "__main__":
    main()
