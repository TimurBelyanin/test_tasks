import unittest
from unittest.mock import patch, MagicMock
import os
import requests
from bs4 import BeautifulSoup
import csv

BASE_URL = "https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту"


def get_animals_count():
    alphabet_counts = dict(А=0, Б=0, В=0, Г=0, Д=0, Е=0, Ё=0, Ж=0, З=0, И=0, Й=0, К=0, Л=0, М=0, Н=0, О=0, П=0, Р=0,
                           С=0, Т=0, У=0, Ф=0, Х=0, Ц=0, Ч=0, Ш=0, Щ=0, Ъ=0, Ы=0, Ь=0, Э=0, Ю=0, Я=0)
    next_page = BASE_URL

    while next_page:
        response = requests.get(next_page)
        soup = BeautifulSoup(response.content, 'html.parser')
        all_animals = soup.find("div", id="mw-pages")

        for animal in all_animals.find_all(class_="mw-category-group"):
            letter = animal.find("h3").text.strip()

            if letter not in alphabet_counts:
                return alphabet_counts

            alphabet_counts[letter] += len(animal.find_all("li"))

        part_url = soup.find('div', id='mw-pages').contents[-2].get('href')
        next_page = ("https://ru.wikipedia.org" + part_url) if part_url else None
    return alphabet_counts


def save_to_csv(data, filename="animals.csv"):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Буква", "Количество животных"])
        for letter, count in data.items():
            writer.writerow([letter, count])


# print("Скачивание данных с википедии...")
# animals_count = get_animals_count()
#
# print(f"Запись данных в файл...")
# save_to_csv(animals_count)
#
# print("Готово! Данные сохранены")


class TestAnimalCount(unittest.TestCase):

    @patch('requests.get')
    def test_get_animals_count(self, mock_get):
        # Подготовим фиктивный HTML-ответ с несколькими страницами
        mock_html_page_1 = '''
        <div id="mw-pages">
            <div class="mw-category-group">
                <h3>А</h3>
                <ul>
                    <li>Акула</li>
                    <li>Аист</li>
                </ul>
            </div>
            <div class="mw-category-group">
                <h3>Б</h3>
                <ul>
                    <li>Бобер</li>
                </ul>
            </div>
            <div class="mw-category-group">
                <h3>В</h3>
                <ul>
                    <li>Волк</li>
                </ul>
            </div>
            <div class="mw-category-group">
                <h3>Г</h3>
                <ul>
                    <li>Гепард</li>
                </ul>
            </div>
            <div class="mw-category-group">
                <h3>Д</h3>
                <ul></ul>
            </div>
        </div>
        '''

        # Настроим мок для последовательных ответов
        mock_get.side_effect = [
            MagicMock(content=mock_html_page_1.encode('utf-8')),
        ]

        # Вызовем функцию
        counts = get_animals_count()

        # Проверим результаты
        expected_counts = {
            'А': 2, 'Б': 1, 'В': 1, 'Г': 1, 'Д': 0, 'Е': 0,
            'Ё': 0, 'Ж': 0, 'З': 0, 'И': 0, 'Й': 0, 'К': 0,
            'Л': 0, 'М': 0, 'Н': 0, 'О': 0, 'П': 0, 'Р': 0,
            'С': 0, 'Т': 0, 'У': 0, 'Ф': 0, 'Х': 0, 'Ц': 0,
            'Ч': 0, 'Ш': 0, 'Щ': 0, 'Ъ': 0, 'Ы': 0, 'Ь': 0,
            'Э': 0, 'Ю': 0, 'Я': 0
        }

        self.assertEqual(counts, expected_counts)

    def test_save_to_csv(self):
        test_data = {'А': 2, 'Б': 1}
        test_filename = "test_animals.csv"

        # Сохраним данные в CSV
        save_to_csv(test_data, test_filename)

        # Проверим содержимое файла
        with open(test_filename, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader)
            rows = list(reader)

        self.assertEqual(header, ["Буква", "Количество животных"])
        self.assertEqual(rows[0], ['А', '2'])
        self.assertEqual(rows[1], ['Б', '1'])

        # Удалим тестовый файл после проверки
        os.remove(test_filename)


if __name__ == '__main__':
    unittest.main()