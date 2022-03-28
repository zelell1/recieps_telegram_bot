import requests
from bs4 import BeautifulSoup
import json


def get_recieps(url):
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36'
    }
    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    all_recieps = []
    reciepss = soup.find("table", class_='rcpf').find_all('dl', class_="catalogue")
    for j in range(len(reciepss)):
        for i in range(len(reciepss[j].find_all('dt')[:])):
            recieps_name = reciepss[j].find_all('dt')[i]
            recieps_name_href = "https://www.russianfood.com"  + str(recieps_name)[str(recieps_name).find('href="') + 6:str(recieps_name).find('">')]
            recieps_names = reciepss[j].find_all('dd')[i]
            recieps = {
                'group_recieps': str(recieps_name.text),
                'group_recieps_href': recieps_name_href,
                'all_recieps': []
            }
            for elem in recieps_names:
                if elem.text != ", " and elem.text != " ":
                    recieps['all_recieps'].append({
                        'name': str(elem.text),      
                        "href":"https://www.russianfood.com"  + str(elem)[str(elem).find('href="') + 6:str(elem).find('">')]         
                    })
            all_recieps.append(recieps)
            with open("jsons/recieps.json", 'w', encoding='utf-8') as js:
                json.dump(all_recieps, js, ensure_ascii=False)

def main():
    get_recieps(url="https://www.russianfood.com/recipes/")

if __name__ == "__main__":
    main()