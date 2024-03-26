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
    def otodom_analyzer(page_limit=2, base_url=None):
        start_time = time()
        print("Starting data analysis...")

        user_agent = UserAgent().random
        headers = {'user-agent': user_agent}

        page = 1
        otodom_article_data = {}

        while page <= page_limit:
            # base_url = f'https://www.otodom.pl/pl/wyniki/wynajem/mieszkanie/mazowieckie/warszawa/warszawa/warszawa?distanceRadius=0&limit=36&daysSinceCreated=1&by=LATEST&direction=DESC&viewType=listing&page={page}'
            response = requests.get(base_url, headers=headers).text

            soup = BeautifulSoup(response, 'lxml')
            articles_container = soup.find("div", {"data-cy": "search.listing.organic"})

            if articles_container:
                print(f'Analyzing page {page}...')

                articles_info = articles_container.find_all("article", {"data-cy": "listing-item"})
                page_offer_data = []

                for article in articles_info:
                    price_element = article.find("span", {"class": "css-1uwck7i e1a3ad6s0"})
                    print(price_element)

                    if price_element is None:
                        continue

                    price = int(price_element.text.split("zł")[0].replace("\xa0", "") if "\xa0" in price_element.text.split("zł")[0] else price_element.text.split("zł")[0])

                    district = article.find("p", class_="css-1dvtw4c e12u5vlm0").text.split(", ")
                    district = district[1] if district[2] == "Warszawa" else district[2]

                    article_link = article.find("a", {"data-cy": "listing-item-link"}).get("href")

                    article_flat_data = list(article.find("dl", {"class": "css-uki0wd e12r8p6s1"}).find_all("dd"))

                    # Извлечение числовых значений из строк и преобразование их в целые числа
                    rooms_text = re.sub('[^0-9]', '', article_flat_data[0].text)
                    rooms = int(rooms_text)

                    # Проверка типа данных для площади (float или int)
                    area_text = article_flat_data[1].text
                    if '.' in area_text:
                        area = float(re.sub('[^0-9.]', '', area_text))
                    else:
                        area = int(re.sub('[^0-9]', '', area_text))

                    floor_text = re.sub('[^0-9]', '', article_flat_data[2].text) if len(article_flat_data) > 2 else ''
                    floor = int(floor_text) if floor_text else 0

                    price_per_sqm = round(price / area)

                    offer_data = {
                        'article_id': DataFinder.generate_request_id(),
                        'price': price,
                        'price_per_sqm': price_per_sqm,
                        'district': district,
                        'rooms': rooms,
                        'area': area,
                        'floor': floor,
                        'link': f'https://www.otodom.pl{article_link}',
                    }
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
    def read_data(path, filters):
        start_time = time()
        print("Starting data reading...")

        data_folder_path = f"./data/{path["current_date"]}"

        request_id = DataFinder.generate_request_id()

        if not os.path.exists(data_folder_path):
            os.makedirs(data_folder_path)

        url = DataFinder.generate_url(filters)

        otodom_data = DataFinder.otodom_analyzer(base_url=url)

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
    def generate_url(filters):
        room_numbers = {
            '1': 'ONE',
            '2': 'TWO',
            '3': 'THREE',
            '4': 'FOUR',
            '5': 'FIVE',
        }

        selected_rooms = filters['selected_rooms'][0]
        rooms_str = ''

        if selected_rooms:
            room_values = [room_numbers[room] for room in selected_rooms.split(',')]
            rooms_str = '%5B' + '%2C'.join(room_values) + '%5D'

        url = f"https://www.otodom.pl/pl/wyniki/wynajem/mieszkanie/mazowieckie/warszawa?distanceRadius=0&limit=36&daysSinceCreated=1&areaMax={filters['max_area'][0]}&priceMin={filters['min_price'][0]}&priceMax={filters['max_price'][0]}&areaMin={filters['min_area'][0]}&roomsNumber={rooms_str}&by=LATEST&direction=DESC&viewType=listing"
        return url

    @staticmethod
    def get_request_id(path):
        with open(path["file_path"], 'r') as file:
            request_id = json.loads(file.read())["request_id"]
        return request_id

