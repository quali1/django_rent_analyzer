import json
import re

from g4f.client import Client


class DataAnalyzer:

    @staticmethod
    def extract_numbers(text):
        numbers = re.findall(r'\d+\.*\d*', text)
        return [float(num) for num in numbers]

    @staticmethod
    def calculate_profitability(apartments, amount=1):
        print(apartments)
        for apartment in apartments:
            apartment['price'] = apartment['price']
            apartment['price_per_sqm'] = apartment['price_per_sqm']

        sorted_apartments = sorted(apartments, key=lambda x: x['price_per_sqm'])
        print(sorted_apartments)
        return sorted_apartments[:amount]

    @staticmethod
    def analyze_apartments(path, amount=1):
        data = open(path["file_path"], "r")
        otodom_data = json.loads(data.read())["otodom_data"]

        apartments = []
        for page_data in otodom_data.values():
            if isinstance(page_data, list):
                apartments.extend(page_data)

        most_profitable = DataAnalyzer.calculate_profitability(apartments, amount)
        return most_profitable

    @staticmethod
    def ai_analyzer(apartments, amount=5):
        print("Data: ", apartments)
        message = f"Дан список объявлений об аренде квартир. Каждое объявление представлено в виде словаря со следующими ключами:\n- 'price': цена квартиры в злотых\n- 'price_per_sqm': цена за квадратный метр в злотых\n- 'district': район, в котором находится квартира\n- 'rooms': количество комнат в квартире\n- 'area': общая площадь квартиры в квадратных метрах\n- 'floor': этаж, на котором находится квартира\n- 'link': ссылка на объявление\n\nВаша задача - проанализировать эти данные и вывести следующую информацию:\n1. Среднюю цену квартиры в каждом районе.\n2. Среднюю цену за квадратный метр в каждом районе.\n3. Самую дорогую и самую дешевую квартиру.\n4. Ссылку на объявление с самой высокой и самой низкой ценой.\n5. 5 самых выгодных объявлений и ссылка на них.\n Данные: {apartments}"
        print("Sending data to ai")
        client = Client()
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message}],
        )

        print("Response: ", response.choices[0].message.content)
        return response.choices[0].message.content

    @staticmethod
    def find_profitable_apartments_advanced(apartments, amount=1):
        for apartment in apartments:
            apartment['profitability_score'] = apartment['price_per_sqm'] * 0.4 + apartment['rooms'] * 0.3 + apartment[
                'area'] * 0.2 + apartment['floor'] * 0.1

        sorted_apartments = sorted(apartments, key=lambda x: x['profitability_score'], reverse=True)
        return sorted_apartments[:amount]
