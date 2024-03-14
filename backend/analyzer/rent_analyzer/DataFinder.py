import os
import re
import json
import requests
import random
import string

from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from time import time
from datetime import datetime, date


class DataFinder:

    @staticmethod
    def otodom_analyzer(page_limit=2):
        start_time = time()
        print("Starting data analysis...")

        user_agent = UserAgent().random
        headers = {'user-agent': user_agent}

        page = 1
        otodom_article_data = {}

        article_id = 1

        while page <= page_limit:
            base_url = f'https://www.otodom.pl/pl/wyniki/wynajem/mieszkanie/mazowieckie/warszawa/warszawa/warszawa?distanceRadius=0&limit=36&daysSinceCreated=1&by=LATEST&direction=DESC&viewType=listing&page={page}'
            response = requests.get(base_url, headers=headers).text

            soup = BeautifulSoup(response, 'lxml')
            articles_container = soup.find("div", {"data-cy": "search.listing.organic"})

            if articles_container:
                print(f'Analyzing page {page}...')

                articles_info = articles_container.find_all("article", {"data-cy": "listing-item"})
                page_offer_data = []

                for article in articles_info:
                    price_element = article.find("span", class_="css-i5x0io ewvgbgo0")
                    price_per_sqm_element = price_element.find("span", {"class": "css-v14eu1 ewvgbgo1"})

                    # Извлечение числовых значений из строк и преобразование их в целые числа
                    price_per_sqm_text = price_per_sqm_element.get_text().replace('zł/m²', '').strip()
                    price_per_sqm = int(re.sub('[^0-9]', '', price_per_sqm_text))

                    price_text = price_element.get_text().replace(price_per_sqm_element.get_text(), '').strip()
                    price = int(re.sub('[^0-9]', '', price_text))

                    district = article.find("p", class_="css-1dvtw4c e1qxnff70").text.split(", ")
                    district = district[1] if district[2] == "Warszawa" else district[2]

                    article_link = article.find("a", class_="css-16vl3c1 e1njvixn0").get("href")

                    article_flat_data = list(article.find("dl", {"class": "css-uki0wd e1jfjthv1"}).find_all("dd"))

                    # Извлечение числовых значений из строк и преобразование их в целые числа
                    rooms_text = re.sub('[^0-9]', '', article_flat_data[0].text)

                    # Проверка типа данных для площади (float или int)
                    area_text = article_flat_data[1].text
                    if '.' in area_text:
                        area = float(re.sub('[^0-9.]', '', area_text))
                    else:
                        area = int(re.sub('[^0-9]', '', area_text))

                    floor_text = re.sub('[^0-9]', '', article_flat_data[2].text) if len(article_flat_data) > 2 else ''

                    # Преобразование строковых значений в целые числа
                    rooms = int(rooms_text)

                    # Проверка наличия значения этажа и преобразование его в целое число, если оно указано
                    if floor_text:
                        floor = int(floor_text)
                    else:
                        floor = 0

                    offer_data = {
                        'article_id': article_id,
                        'price': price,
                        'price_per_sqm': price_per_sqm,
                        'district': district,
                        'rooms': rooms,
                        'area': area,
                        'floor': floor,
                        'link': f'https://www.otodom.pl{article_link}',
                    }
                    article_id += 1
                    page_offer_data.append(offer_data)

                otodom_article_data[f'page_{page}'] = page_offer_data
                print(f"Page {page} analyzed.")
                page += 1
            else:
                break

        end_time = time()
        processing_time = end_time - start_time
        print(f"Data analysis completed. Processing time: {processing_time:.2f} seconds.")

        return otodom_article_data

    @staticmethod
    def read_data(path):
        start_time = time()
        print("Starting data reading...")

        data_folder_path = f"./data/{path["current_date"]}"

        request_id = DataFinder.generate_request_id()

        if not os.path.exists(data_folder_path):
            os.makedirs(data_folder_path)

        otodom_data = DataFinder.otodom_analyzer()

        json_total_data = {
            "otodom_data": otodom_data,
            "request_id": request_id,
        }

        with open(path["file_path"], "w+") as data_file:
            json.dump(json_total_data, data_file, ensure_ascii=False, indent=4)

        end_time = time()
        processing_time = end_time - start_time
        print(f"Data reading completed. Processing time: {processing_time:.2f} seconds.")

    @staticmethod
    def get_path():
        current_date = datetime.now().strftime("%d-%m-%Y")
        current_datetime = datetime.now().strftime("%d-%m-%Y %H:%M")
        data_folder_path = f"./data/{current_date}"

        file_path = os.path.join(f"{data_folder_path}", f'{current_datetime}_testdata.json')

        path_info = {"current_date": current_date,
                     "current_datetime": current_datetime,
                     "file_path": file_path}

        return path_info

    @staticmethod
    def generate_request_id():
        request_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        # random_url = f"(https://example.com/){request_id}?"

        return request_id

    @staticmethod
    def get_request_id(path):
        with open(path["file_path"], 'r') as file:
            request_id = json.loads(file.read())["request_id"]

        return request_id
