# Проект DRF LMS

Этот проект представляет собой систему управления обучением (LMS) на основе Django и Django REST Framework (DRF). Проект использует Docker и Docker Compose для простого развертывания и управления.

## Требования

- Docker: https://docs.docker.com/get-docker/
- Docker Compose: https://docs.docker.com/compose/install/

## Содержимое репозитория

- `Dockerfile`: Описание Docker-образа для приложения.
- `docker-compose.yml`: Конфигурация Docker Compose для запуска нескольких контейнеров.
- `pyproject.toml` и `poetry.lock`: Файлы конфигурации Poetry для управления зависимостями.
- `manage.py`: Скрипт управления Django.
- `app/`: Директория с исходным кодом приложения.
- `tests/`: Директория с тестами.

## Установка

1. Клонируйте репозиторий:

    ```bash
    git clone https://github.com/maxmit69/DRF-lms.git
    cd DRF-lms
    ```

2. Создайте файл `.env` с необходимыми переменными окружения:

    ```env
    POSTGRES_USER=your_postgres_user
    POSTGRES_PASSWORD=your_postgres_password
    POSTGRES_DB=drf_lms_db
    ```

## Использование

### Запуск проекта

-
   ```bash
   docker-compose up -d --build
   ```

### Структура проекта

- `app`: Основное приложение Django.
- `db`: Контейнер с PostgreSQL.
- `redis`: Контейнер с Redis.
- `celery`: Воркеры Celery для асинхронных задач.
- `celery-beat`: Планировщик задач Celery.

### API

#### Список эндпоинтов

| Метод    | Эндпоинт                          | Описание                                   |
|----------|-----------------------------------|--------------------------------------------|
| GET      | /lms/courses/                     | Получить список курсов                     |
| POST     | /lms/courses/                     | Создать новый курс                         |
| GET      | /lms/courses/:id                  | Получить информацию о курсе                |
| PUT      | /lms/courses/:id                  | Обновить информацию о курсе                |
| DELETE   | /lms/courses/:id                  | Удалить курс                               |
| PATCH    | /lms/course/:id/                  | Обновление одной сущности курса            |
|----------|-----------------------------------|--------------------------------------------|
| GET      | /lms/subscription/                | Получить список подписок                   |
| POST     | /lms/subscription/                | Создать подписку                           |
| POST     | /lms/subscription/subscribe/      | Подписка на курс                           |
| POST     | /lms/subscription/unsubscribe/    | Отмена подписки на курс                    |
| GET      | /lms/subscription/:id/            | Чтение одной сущности подписки             |
| PUT      | /lms/subscription/:id/            | Обновление подписки                        |
| PATCH    | /lms/subscription/:id/            | Обновление одной сущности подписки         |
| DELETE   | /lms/subscription/:id/            | Удаление подписки                          |
|----------|-----------------------------------|--------------------------------------------|
| GET      | /lms/lesson/                      | Получить список уроков                     |
| POST     | /lms/lesson/create/               | Создать новый урок                         |
| GET      | /lms/lesson/:id                   | Получить информацию о уроке                |
| PUT      | /lms/lesson/:id/update/           | Обновить информацию о уроке                |
| DELETE   | /lms/lesson/:id/delete/           | Удалить урок                               |
| PATCH    | /lms/lesson/{id}/update/          | Обновление одной сущности урока            |
|----------|-----------------------------------|--------------------------------------------|
| GET      | /users/check-payment-status/:id/  | Проверка статуса платежа                   |
| POST     | /users/create-payment/            | Создание платежа                           |
| POST     | /users/login/                     | Авторизация                                |
| POST     | /users/register/                  | Регистрация                                |
| POST     | /users/token/refresh/             | Обновление токена                          |

#### Примеры запросов

- Получить список курсов:

    ```bash
    curl -X GET http://localhost:8000/lms/courses/ 
    ```

- Создать новый курс:

    ```bash
    curl -X POST http://localhost:8000/lms/courses/  -H "Content-Type: application/json" -d '{"name": "New Course", "description": "Course Description"}'
    ```

- Обновить информацию о курсе:

    ```bash
    curl -X PUT http://localhost:8000/lms/courses/1/ -H "Content-Type: application/json" -d '{"name": "Updated Course", "description": "Updated Description"}'
    ```

- Удалить курс:

    ```bash
    curl -X DELETE http://localhost:8000/lms/courses/1/
    ```

### Тестирование

- Для запуска тестов выполните следующую команду:

    ```bash
    docker-compose run app poetry run python manage.py test

### Загрузка фикстур

- Для загрузки данных фикстур используйте следующую команду:

    ```bash
  docker-compose run app poetry run python manage.py loaddata fixtures/groups.json
  docker-compose run app poetry run python manage.py loaddata fixtures/payments_data.json

### Команды управления

- Остановить контейнеры:

    ```bash
    docker-compose down
    ```

- Просмотр логов:

    ```bash
    docker-compose logs -f
    ```

- Перезапуск контейнеров:

    ```bash
    docker-compose restart
    ```

## Дополнительная информация

Для получения дополнительной информации и настроек, смотрите документацию:
- [Django](https://docs.djangoproject.com/en/stable/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Docker](https://docs.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Poetry](https://python-poetry.org/docs/)
