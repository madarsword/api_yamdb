![YaMDb](https://pictures.s3.yandex.net/resources/Samostoiatelnyi_proekt_1587107358.svg)


# Проект YaMDb
Проект **YaMDb** собирает отзывы пользователей на произведения. Сами произведения в **YaMDb** не хранятся.

Произведения делятся на категории. Список категорий может быть расширен.

Произведению может быть присвоен жанр из списка предустановленных. 

Добавлять произведения, категории и жанры может только администратор.

Пользователи могут оставлять к произведениям текстовые отзывы и ставить произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок будет формироваться усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.

Пользователи могут оставлять комментарии к отзывам.

Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи.


## Техническое описание проекта YaMDb
Документация проекта: ***http://127.0.0.1:8000/redoc/***

### I. Ресурсы API YaMDb:
- ***auth***: аутентификация;
- ***users***: пользователи;
- ***titles***: произведения, к которым пишут отзывы;
- ***categories***: категории (типы) произведений. _Одно произведение может быть привязано только к одной категории_;
- ***genres***: жанры произведений. _Одно произведение может быть привязано к нескольким жанрам_;
- ***reviews***: отзывы на произведения. _Отзыв привязан к определённому произведению_;
- ***comments***: комментарии к отзывам. _Комментарий привязан к определённому отзыву_.

### II. Пользовательские роли и права доступа:
- ***Аноним*** — может просматривать описания произведений, читать отзывы и комментарии.
- ***Аутентифицированный пользователь (user)*** — может читать всё, как и *Аноним*, может публиковать отзывы и ставить оценки произведениям, может комментировать отзывы; может редактировать и удалять свои отзывы и комментарии, редактировать свои оценки произведений. Эта роль присваивается по умолчанию каждому новому пользователю.
- ***Модератор (moderator)*** — те же права, что и у *Аутентифицированного пользователя*, плюс право удалять и редактировать любые отзывы и комментарии.
- ***Администратор (admin)*** — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.
- ***Суперюзер Django*** должен всегда обладать правами *администратора*, *пользователя с правами admin*. Даже если изменить пользовательскую роль суперюзера — это не лишит его прав администратора. *Суперюзер — всегда администратор, но администратор — не обязательно суперюзер*.

### III. Установка и запуск проекта:

Клонировать репозиторий:
```
git clone https://github.com/madarsword/api_yamdb.git
```

Cоздать и активировать виртуальное окружение:
```
python -m venv venv
. venv/Scripts/activate
```

Установить зависимости (файл requirements.txt):
```
pip install -r requirements.txt
```

Выполнить миграции:
```
python manage.py makemigrations
python manage.py migrate
```

Запустить проект:
```
python manage.py runserver
```

### IV. Примеры запросов к API:

Регистрация нового пользователя:
- Получить код подтверждения на переданный email. Права доступа: Доступно без токена. Использовать имя 'me' в качестве username запрещено. Поля email и username должны быть уникальными
```
POST
/auth/signup/
```

Получение списка всех категорий:
- Права доступа: Доступно без токена
```
GET
/categories/
```

Удаление категории:
- Права доступа: Администратор.
```
DELETE
/categories/{slug}/
```

Изменение данных пользователя по username:
- Права доступа: Администратор. Поля email и username должны быть уникальными.
```
PATCH
/users/{username}/
```


## Авторы проекта:
- Александр Шпара
- Фазиль Исрафилов
- Артём Трянин
