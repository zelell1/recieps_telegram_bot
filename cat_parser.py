import requests
from bs4 import BeautifulSoup
import random


def cat_pic():
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36'
    }
    url = 'https://http.cat/'
    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    cards = soup.find_all("div", class_="Thumbnail_title__2iqYK")
    cards_dict = []
    for i in cards:
        nums = str(i)[str(i).find('>') + 1:str(i).find('</div>')]
        cards_dict.append(nums)
    return cards_dict[random.randint(0, len(cards))]


def main():
    print(cat_pic())


if __name__ == "__main__":
    main()
