# AI-Workshop backend

## Описание проекта

### Используемые технологии:

<img src="https://github.com/user-attachments/assets/f2b1a202-83ef-4842-8ed0-0315a1377f6f" title="Python" alt="python" width="75" height="75"/>
<img src="https://github.com/user-attachments/assets/48086997-d4eb-4876-848c-9baaf8e728eb" title="FastAPI" alt="fastapi" width="75" height="75"/>
<img src="https://github.com/user-attachments/assets/cb88c094-5f7e-43d2-970c-4640c8e203ae" title="FastAPI-Users" alt="fastapi-users" width="225" height="225"/>
<img src="https://github.com/user-attachments/assets/1f8c4daa-dce1-465f-bb11-1a95bc72a1c6" title="Postgres" alt="postgres" width="75" height="75"/>
<img src="https://github.com/user-attachments/assets/74fcd7e2-345f-4eb2-afbf-8fd701726be8" title="SQLAlchemy" alt="sqlalchemy" width="75" height="75"/>
<img src="https://github.com/user-attachments/assets/b0e8f3ae-84b6-4121-8c2c-9ed8f0355e14" title="Poetry" alt="poetry" width="75" height="75"/>
<img src="https://github.com/user-attachments/assets/6a28d993-e235-4314-9860-f12e71238614" title="Pydantic" alt="pydantic" width="75" height="75"/>
<img src="https://github.com/user-attachments/assets/096102ab-304b-4b89-b2d6-08f76b1aaa76" title="Redis" alt="redis" width="75" height="75"/>
<img src="https://github.com/user-attachments/assets/e8ae669f-3be6-4171-9dd5-15011505ecfd" title="Minio" alt="minio" width="225" height="225"/>
<img src="https://github.com/user-attachments/assets/648aa8d0-0ba1-4362-a281-2e252e2ec97b" title="Docker" alt="docker" width="75" height="75"/>

### Основные функции:
- JWT-аутентификация (access token)
- Ролевая модель управления доступом (RBAC)
- Асинхронные CRUD-операции с PostgreSQL
- Автоматическая генерация миграций (Alembic)
- Валидация данных с Pydantic v2
- Загрузка/скачивание файлов через REST API
- Интеграция с MinIO (S3-совместимое хранилище)
- Кеширование запросов к базе данных
- Интерактивная документация Swagger UI

### Предварительные требования:
- Python v3.13.2 или выше
- Postgres v14.18 или выше
- Redis v8.2.0 или выше
- Minio vRELEASE.2025-04-08T15-41-24Z или выше
- Poetry v2.1.1 или выше
- Docker v27.5.1 (для docker-запуска)

## Установка и запуск (без Docker)

1. Клонируйте репозиторий:
```
git clone https://github.com/PD-AI-Workshop/backend
cd backend
```
2. Создайте виртуальное окружение, активируйте его и установите poetry:
```
python -m venv .venv

# MacOS и Linux
source .venv/bin/activate
# Windows
.venv/Scripts/activate

pip install poetry
```
3. Создайте файл .env в корне проекта и заполните значение:
```
# Локальная база данных (замените значения на свои!)
DB_HOST=localhost
DB_PORT=your_db_port
DB_NAME=ai-workshop
DB_USER=your_db_user
DB_PASS=your_db_password

# Локальное S3-хранилище (замените значения на свои!)
MINIO_HOST=localhost
MINIO_PORT=your_minio_port
MINIO_ACCESS_KEY=your_minio_access_key
MINIO_SECRET_KEY=your_minio_secret_key

# Шифрование (придумайте свой секретный ключ)
SECRET_KEY=your_secret_key

# Локальная база данных Redis (замените значения на свои!)
REDIS_HOST=localhost
REDIS_PORT=your_redis_port

# Локальный хост (замените значение на свое!)
HOST=your_host
```
4. Скачайте зависимости:
```
poetry install
```
5. Примените миграции к базе данных:
```
alembic upgrade head
```
6. Запуск приложения:
```
python main.py
```

## Запуск с помощью Docker
1. Клонируйте репозиторий:
```
git clone https://github.com/PD-AI-Workshop/backend
cd backend
```
2. Создайте виртуальное окружение, активируйте его и установите poetry:
```
python -m venv .venv

# MacOS и Linux
source .venv/bin/activate
# Windows
.venv/Scripts/activate

pip install poetry
```
3. Создайте файл .env в корне проекта и заполните значение:
```
# База данных в Docker (замените значения на свои!)
DB_HOST=postgres (название сервиса в Docker-compose)
DB_PORT=your_db_port
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASS=your_db_password

# S3-хранилище в Docker (замените значения на свои!)
MINIO_HOST=minio (название сервиса в Docker-compose)
MINIO_PORT=your_minio_port
MINIO_ACCESS_KEY=your_minio_access_key
MINIO_SECRET_KEY=your_minio_secret_key

# Шифрование (придумайте свой секретный ключ)
SECRET_KEY=your_secret_key

# База данных Redis в Docker (замените значения на свои!)
REDIS_HOST=redis (название сервиса в Docker-compose)
REDIS_PORT=your_redis_port

# Локальный хост (замените значение на свое!)
HOST=your_host
```
4. В папке выше напишите файл Docker-compose.yml:
```
name: "ai-workshop-stack"

services:
  postgres:
    image: postgres:14-alpine
    container_name: ai-workshop-postgres
    env_file: .env
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_PORT: ${POSTGRES_PORT}
    volumes:
      - pgdata:/var/lib/postgresql/data
    
  minioS3:
    image: minio/minio:latest
    container_name: ai-workshop-minioS3
    env_file: .env
    environment:
      MINIO_ROOT_USER: ${MINIO_ROOT_USER}
      MINIO_ROOT_PASSWORD: ${MINIO_ROOT_PASSWORD}
    ports:
      - "9000:9000"
      - "9001:9001"
    volumes:
      - miniodata:/data
    command: minio server /data

  redis:
    image: redis:8.2-alpine
    container_name: ai-workshop-redis
    volumes:
      - redisdata:/data

  backend:
    build: 
      context: ./backend
      dockerfile: Dockerfile
    container_name: ai-workshop-backend
    ports:
      - "8000:8000"
    command: sh -c "poetry run alembic upgrade head && poetry run uvicorn main:app --host 0.0.0.0 --port 8000"

volumes:
  miniodata:
  redisdata:
  pgdata:
```
5. Создайте на том же уровне .env файл и заполните его переменными окружениями:
```
# Переменные окружения для postgres контейнера (замените значения на свои!)
POSTGRES_USER=your_postgres_user
POSTGRES_PASSWORD=your_postgres_password
POSTGRES_DB=your_postgres_db
POSTGRES_PORT=your_postgres_port

# Переменные окружения для minio контейнера (замените значения на свои!)
MINIO_ROOT_USER=your_minio_user
MINIO_ROOT_PASSWORD=your_minio_password

# Переменные окружения для grafana контейнера (замените значения на свои!)
GF_SECURITY_ADMIN_USER=your_grafana_user
GF_SECURITY_ADMIN_PASSWORD=your_grafana_password
GF_SERVER_HTTP_PORT=your_grafana_port
```  
6. Запустите Docker-compose:
```
docker compose up
```
Приложение будет доступно по адресу: http://localhost:8000

## Основные скрипты

- ```python main.py``` - запуск приложения
- ```black .``` - форматирование кода с Black

## Структура проекта
```
backend/
├── APIRouter.py              # Основной файл для регистрации роутеров API
├── Dockerfile                # Конфигурация для сборки Docker-образа приложения
├── README.md                 # Основная документация проекта
├── alembic                   # Папка со скриптами миграций
├── alembic.ini               # Конфигурация alembic
├── auth                      # Аутентификация и авторизация 
├── config                    # Дополнительные конфигурационные файлы
├── controller                # Обработчики HTTP-запросов
├── db                        # Утилиты для работы с БД
├── dependencies              # FastAPI-зависимости (DI)
├── dto                       # Data Transfer Objects (DTO)
├── enums                     # Перечисления
├── exception                 # Кастомные исключения и обработчики ошибок
├── main.py                   # Точка входа в приложение. Инициализирует FastAPI, подключает middleware, роутеры.
├── mapper                    # Утилиты для преобразования объектов
├── metrics                   # Сбор метрик
├── model                     # ORM-модели (SQLAlchemy) для работы с БД
├── poetry.lock               # Конфигурация зависимостей и виртуального окружения (Poetry)
├── pyproject.toml            # Конфигурация зависимостей и виртуального окружения (Poetry)
├── repository                # Абстракции для доступа к БД
├── service                   # Бизнес-логика
└── settings.py               # Настройки приложения. Загрузка переменных окружения.
```
