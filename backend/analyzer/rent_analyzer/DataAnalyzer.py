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
        for apartment in apartments:
            apartment['price'] = apartment['price']
            apartment['price_per_sqm'] = apartment['price_per_sqm']

        sorted_apartments = sorted(apartments, key=lambda x: x['price_per_sqm'])

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
        print(type(most_profitable))
        return most_profitable

    @staticmethod
    def ai_analyzer(apartments, amount=5):
        message = f"Не представляйся. Проанализируй рынок квартир на основе предоставленных данных. Укажи {amount} самых выгодных предложений. Отвечай на русском языке. Для каждой квартиры имеются следующие данные: {apartments}"

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
