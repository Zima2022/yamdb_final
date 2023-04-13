import csv
import os

from django.core.management import BaseCommand
from django.db import IntegrityError
from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title
from users.models import User

from api_yamdb.settings import CSV_DATA_DIR

FILES_MODELS = {
    'category.csv': Category,
    'genre.csv': Genre,
    'titles.csv': Title,
    'genre_title.csv': GenreTitle,
    'users.csv': User,
    'review.csv': Review,
    'comments.csv': Comment,
}

FIELDS = {
    'category': ('category', Category),
    'title_id': ('title', Title),
    'genre_id': ('genre', Genre),
    'author': ('author', User),
    'review_id': ('review', Review),
}


def open_csv_file(file_name):
    """Менеджер контекста для открытия csv-файлов."""
    csv_path = os.path.join(CSV_DATA_DIR, file_name)
    try:
        with (open(csv_path, encoding='utf-8')) as file:
            return list(csv.reader(file))
    except FileNotFoundError:
        print(f'Файл {file_name} не найден.')


def change_foreign_values(data_csv):
    """Заменяет foreing key из загружаемой таблицы на объекты"""
    data_csv_copy = data_csv.copy()
    for field_key, field_value in data_csv.items():
        if field_key in FIELDS.keys():
            field_key0 = FIELDS[field_key][0]
            data_csv_copy[field_key0] = FIELDS[field_key][1].objects.get(
                pk=field_value)
    return data_csv_copy


def load_csv(file_name, model):
    """Загружает данные из csv-файла в БД"""
    data = open_csv_file(file_name)
    rows = data[1:]
    for row in rows:
        data_csv = dict(zip(data[0], row))
        data_csv = change_foreign_values(data_csv)
        try:
            table = model(**data_csv)
            table.save()
        except (ValueError, IntegrityError) as error:
            print(f'Ошибка в загружаемых данных. {error}. '
                  f'Таблица {model.__name__} не загружена.')
            break
    print(f'Таблица {model.__name__} загружена.')


class Command(BaseCommand):
    """Класс загрузки тестовой базы данных."""
    def handle(self, *args, **options):
        for file, model in FILES_MODELS.items():
            print(f'Загрузка таблицы {model.__name__}')
            load_csv(file, model)
