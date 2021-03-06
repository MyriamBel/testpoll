Опрос пользователей (Django REST Framework)

Задача: спроектировать и разработать API для системы опросов пользователей.

Функционал для администратора системы:

    авторизация в системе (регистрация не нужна)
    добавление/изменение/удаление опросов. Атрибуты опроса: название, дата старта, дата окончания, описание. После создания поле "дата старта" у опроса менять нельзя
    добавление/изменение/удаление вопросов в опросе. Атрибуты вопросов: текст вопроса, тип вопроса (ответ текстом, ответ с выбором одного варианта, ответ с выбором нескольких вариантов)

Функционал для пользователей системы:

    получение списка активных опросов
    прохождение опроса: в качестве идентификатора пользователя в API передаётся числовой ID, по которому сохраняются ответы пользователя на вопросы; один пользователь может участвовать в любом количестве опросов
    получение пройденных пользователем опросов с детализацией по ответам (что выбрано) по ID уникальному пользователя

Использовать следующие технологии: Django 2.2.10, Django REST framework.

Результат выполнения задачи:

    исходный код приложения в github (только на github, публичный репозиторий)
    инструкция по разворачиванию приложения (в docker или локально)
    документация по API

Как запустить
Потребуются установленные в системе pyenv с Python 3.7, virtualenv, установленная и настроенная БД postgres (username testpoll, password testpoll).
Изоляция проекта (для Ubuntu):
1) mkdir testvenv && cd testvenv
2) активируем pyenv
3) активируем virtualenv из pyenv
4) устанавливаем зависимости из файла requirements.txt
5) выполняем миграции и создание суперюзера:
  python manage.py migrate
  python manage.py createsuperuser
!!!Создаём супер-юзера с именем testpoll и паролем testpoll.

Проверка версий Python и Django:
python -m django --version
python3 -V

Документация по ендпоинтам доступна после запуска проекта по ссылке: http://127.0.0.1:8000/swagger/
