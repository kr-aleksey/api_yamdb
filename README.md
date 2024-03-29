# API проекта YaMDb

## Авторы

* **Тимлид + разработчик №1** - [Алексей Кравцун](https://github.com/kr-aleksey)
> Структура проекта, Управление пользователями

* **Разработчик №2** - [Наташа Широкая](https://github.com/shirokonidze)
> Модели, view и эндпойнты для произведений, категорий, жанров

* **Разработчик №3** - [Екатерина Иванова](https://github.com/KateIndri)
> Модели, view и эндпойнты для отзывов и комментариев


## Описание

Проект **YaMDb** собирает отзывы пользователей на произведения.
Сами произведения в YaMDb не хранятся, здесь _нельзя_ посмотреть фильм или послушать музыку.
С **YaMDb** _можно_:
1. оставить к произведениям текстовые отзывы
2. поставить произведению оценку

Произведения делятся на _категории_ и _жанры_.
Из пользовательских оценок формируется _рейтинг произведения_.
На одно произведение пользователь может оставить только один отзыв.

Используя этот API пользователи смогут работать с **YaMDb** через мобильное приложение или чат-бот.
Через него же можно передавать данные в любое приложение или на фронтенд.


## Пользовательские роли и права доступа

* **Аноним** — может просматривать описания произведений, читать отзывы и комментарии.
* **Аутентифицированный пользователь (```user```)** — может читать всё, как и Аноним, может публиковать отзывы и ставить оценки произведениям (фильмам/книгам/песенкам), может комментировать отзывы; может редактировать и удалять свои отзывы и комментарии, редактировать свои оценки произведений. Эта роль присваивается по умолчанию каждому новому пользователю.
* **Модератор (```moderator```)** — те же права, что и у **Аутентифицированного пользователя,** плюс право удалять и редактировать **любые** отзывы и комментарии.
* **Администратор (```admin```)** — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.
* **Суперюзер Django** должен всегда обладать правами администратора, пользователя с правами admin. Даже если изменить пользовательскую роль суперюзера — это не лишит его прав администратора. Суперюзер — всегда администратор, но администратор — не обязательно суперюзер.


## Установка

* Клонировать репозиторий и перейти в него в командной строке:
```
git clone https://github.com/kr-aleksey/api_yamdb
```

* Создать и активировать виртуальное окружение:
```
python3 -m venv env
source env/bin/activate
```

* Установить зависимости из файла requirements.txt:
```
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```

* Выполнить миграции:
```
python3 manage.py migrate
```

* Запустить проект:
```
python3 manage.py runserver
```


## Некоторые примеры запросов к API.

1. Получение списка всех произведений

GET-запрос
http://127.0.0.1:8000/api/v1/titles/

_Response:_
```
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "id": 0,
        "name": "string",
        "year": 0,
        "rating": 0,
        "description": "string",
        "genre": [
          {
            "name": "string",
            "slug": "string"
          }
        ],
        "category": {
          "name": "string",
          "slug": "string"
        }
      }
    ]
  }
]
```

2. Получение списка всех отзывов к произведению

GET-запрос
http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/

_Response:_
```
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "id": 0,
        "text": "string",
        "author": "string",
        "score": 1,
        "pub_date": "2019-08-24T14:15:22Z"
      }
    ]
  }
]
```


3. Добавление комментария к отзыву

POST-запрос
http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/

_Request:_ 
```
{
  "text": "string"
}
```

_Response:_
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "pub_date": "2019-08-24T14:15:22Z"
}
```

4. Частичное обновление информации о произведении

PATCH-запрос
http://127.0.0.1:8000/api/v1/titles/{titles_id}/

_Request:_ 
```
{
  "name": "string",
  "year": 0,
  "description": "string",
  "genre": [
    "string"
  ],
  "category": "string"
}
```

_Response:_
```
{
  "id": 0,
  "name": "string",
  "year": 0,
  "rating": 0,
  "description": "string",
  "genre": [
    {
      "name": "string",
      "slug": "string"
    }
  ],
  "category": {
    "name": "string",
    "slug": "string"
  }
}
```
