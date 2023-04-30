import datetime as dt


def validate_year(year):
    now_year = dt.date.today()
    if year > now_year.year:
        raise ValueError(
            'Год выпуска не может быть больше текущего. '
            f'Год {year}'
        )
