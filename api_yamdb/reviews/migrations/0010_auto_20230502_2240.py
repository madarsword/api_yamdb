# Generated by Django 3.2 on 2023-05-02 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0009_auto_20230502_2237'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='review',
            name='review_unique',
        ),
        migrations.AddConstraint(
            model_name='review',
            constraint=models.UniqueConstraint(fields=('title', 'author'), name='review_unique'),
        ),
    ]
