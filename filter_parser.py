import requests
from bs4 import BeautifulSoup
import json


def get_cards(url, page, headers):
    url = f"{url}&page={page}#rcp_list"
    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    cards = soup.find_all("div", class_='title_o')
    cards_dict = []
    for i in range(len(cards)):
        href = "https://www.russianfood.com" + str(cards[i].find('a'))[
                                               str(cards[i].find('a')).find('href="') + 6:str(cards[i].find('a')).find(
                                                   '" name=')]
        card = {
            "name": cards[i].text.strip().replace('\"', ""),
            "href": href
        }
        cards_dict.append(card)
    return cards_dict


def get_card(url, headers):
    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    card = soup.find('td', class_="padding_l padding_r")
    img = card.find("img")
    img_href = str(img)[str(img).find('"//'): str(img).find(' title')].replace('\"', "")
    description = card.find_all('div')[-1].text
    products = [soup.find('table', class_="ingr").find('td', class_="padding_l ingr_title").text.strip()] \
               + [i.text for i in soup.find('table', class_="ingr").find_all('span', class_="")]
    if img_href == '':
        img_href = 'https://http.cat/102'
    card_now = {
        'img': img_href,
        'description': description,
        'products': products
    }
    return card_now


def main():
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36'
    }
    print(get_card(url="https://www.russianfood.com/recipes/recipe.php?rid=148403", headers=headers))

if __name__ == "__main__":
    main()
