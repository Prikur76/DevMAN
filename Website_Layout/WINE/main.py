import os
import sys
import collections
import argparse
from datetime import datetime
import pandas as pd
from dotenv import load_dotenv

from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape

load_dotenv()

env = Environment(loader=FileSystemLoader('.'),
                  autoescape=select_autoescape(['html', 'xml']))

template = env.get_template('template.html')
# source_file_path = os.environ['source_file_path']

def calculate_difference_between_two_years(foundation_year=0):
    """Возвращает разницу в годах между текущей и начальным годом"""
    now = datetime.now().year
    diff_years = now - foundation_year
    return diff_years


def get_correct_foundation_text(diff_years):
    """Возвращает корректный текст (год, года, лет)"""
    if (diff_years % 100 in [11, 12, 13, 14]) or (diff_years % 10 in [0, 5]):
        foundation_text = f"Уже {diff_years} лет с вами"
    elif diff_years % 10 == 1:
        foundation_text = f"Уже {diff_years} год с вами"
    elif diff_years % 10 in [2, 3, 4]:
        foundation_text = f"Уже {diff_years} года с вами"
    else:
        foundation_text = f"Уже {diff_years} лет с вами"
    return foundation_text


def get_records_from_excel(source_file_path):
    """Возвращает словарь с информацией, разбитой по категориям напитков"""
    records_from_source = pd.read_excel(io=source_file_path,
                                        sheet_name="Лист1",
                                        na_values='None',
                                        keep_default_na=False)\
        .sort_values(by=['Категория'], axis=0)
    sorted_records = collections.defaultdict(list)
    for row in records_from_source.to_dict(orient='records'):
        sorted_records[row['Категория']].append(row) 
    return sorted_records


def get_source_file_path():
    parser = argparse.ArgumentParser()
    parser.add_argument('-fp', '--filepath', default=False, help='Путь к местоположению файла .xlsx') 
    filepath_argument = parser.parse_args()
    print(filepath_argument.filepath)
    if filepath_argument.filepath:
        return filepath_argument.filepath
    else:
        print(os.getenv('source_file_path'))
        return os.getenv('source_file_path')


source_file_path = get_source_file_path()
wines = get_records_from_excel(source_file_path)
count_of_years = calculate_difference_between_two_years(foundation_year=1920)
foundation_text = get_correct_foundation_text(count_of_years)

rendered_page = template.render(foundation_text=foundation_text,
                                wines=wines)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
