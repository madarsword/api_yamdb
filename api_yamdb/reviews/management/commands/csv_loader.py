import csv

from django.core.management.base import BaseCommand
from django.conf import settings

from reviews.models import Category, Genre, Review, Title, Comment
from users.models import User


FILES = {
    User: 'users.csv',
    Category: 'category.csv',
    Genre: 'genre.csv',
    Title: 'titles.csv',
    Title.genre.through: 'genre_title.csv',
    Review: 'review.csv',
    Comment: 'comments.csv',
}


class Command(BaseCommand):
    help = 'Uploading data from CSV'

    def handle(self, *args, **options):
        for model, csv_file in FILES.items():
            with open(
                f'{settings.BASE_DIR}/static/data/{csv_file}', 'r',
                encoding="utf-8",
            ) as file:
                reader = csv.DictReader(file)
                data = []
                for row in reader:
                    data.append(model(**row))
            model.objects.bulk_create(data)
            self.stdout.write(self.style.SUCCESS(
                f'Load complete {csv_file}'
            ))
