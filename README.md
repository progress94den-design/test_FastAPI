# FastAPI Blog API

Backend API для блога на **FastAPI** с поддержкой:

* аутентификации пользователей
* статей и категорий
* фоновых задач (Taskiq + RabbitMQ)
* PostgreSQL (async SQLAlchemy)
* MinIO для хранения файлов
* Docker / Docker Compose

Проект спроектирован как **production-ready API** с чистой архитектурой и документацией.

---

## 🧱 Технологический стек

* **Python 3.13**
* **FastAPI**
* **SQLAlchemy (async)**
* **PostgreSQL**
* **FastAPI Users**
* **Taskiq**
* **RabbitMQ**
* **MinIO**
* **Pydantic v2**
* **Docker & Docker Compose**

---

## 📁 Структура проекта

```text
.
├── compose/                 # Docker конфигурация
│   ├── compose-compose.yml  # Docker Compose для приложения
│   ├── Dockerfile           # Dockerfile приложения
│   └── entrypoint.sh        # Точка входа контейнера
├── src/                     # Исходный код
│   ├── alembic/             # Миграции базы данных
│   ├── api/                 # API эндпоинты
│   │   ├── api_v1/          # Роутеры по ресурсам
│   │   ├── dependencies/    # Зависимости для роутеров
│   │   └── routers.py       # Главный роутер
│   ├──core/                 # Ядро приложения
│   │  ├── authentication/   # Настройки UserManager
│   │  ├── config.py         # Настройки проекта
│   │  └── db_helper.py      # Настройки базы данных
│   ├── crud/                # CRUD операции
│   ├── models/              # SQLAlchemy модели
│   ├── schemas/             # Pydantic схемы
│   ├── services/            # Сервисы (mail, taskiq, article, category, minio)
│   ├── env.app              # Переменные окружения для приложения
│   ├── env.cont             # Переменные окружения для Docker container
│   ├── alembic.ini          # Файл для alembic
│   └── main.py              # Точка входа FastAPI
│── pyproject.toml           # Зависимости проекта
└── README.md                # Описание проекта
```

---

## 🚀 Быстрый старт

### 1. Клонирование репозитория

```bash
git clone https://github.com/your-username/test_FastAPI.git
cd test_FastAPI
```

---

### 2. Перейти в папку compose
```bash
cd compose
```

---

### 3. Запуск проекта

```bash
docker compose up --build
```

После запуска будут доступны:

| Сервис   | URL                                                        |
|----------| ---------------------------------------------------------- |
| API      | [http://localhost:8000](http://localhost:8000)             |
| Swagger  | [http://localhost:8000/docs](http://localhost:8000/docs)   |
| Redoc    | [http://localhost:8000/redoc](http://localhost:8000/redoc) |
| RabbitMQ | [http://localhost:15672](http://localhost:15672)           |
| MinIO    | [http://localhost:9001](http://localhost:9001)             |
| MailDev  | [http://localhost:8080](http://localhost:8080)             |

---

## 📖 Документация API

Swagger UI доступен по адресу:

```
http://localhost:8000/docs
```

В документации есть:

* описания ручек
* примеры запросов и ответов
* схемы данных

---

## 🔐 Аутентификация

Используется **FastAPI Users**:

* JWT авторизация
* cookies
* защищённые эндпоинты

---

## 📝 Статьи

### Возможности:

* создание статьи
* загрузка изображения
* поиск
* пагинация
* привязка категорий
* обновление и удаление

---

## 🗂 Категории

### Возможности:

* создание категории
* получение по ID
* список категорий с пагинацией

---

## ⚙️ Фоновые задачи

Для фоновых задач используется **Taskiq** + **RabbitMQ**.

Worker запускается в отдельном контейнере и обрабатывает задачи асинхронно.

---

## 🗄 Подключение к базе данных (DBeaver)

Для подключения к PostgreSQL через DBeaver:

* **Host:** `localhost`
* **Port:** `5432`
* **Database:** `api_db`
* **User:** `us_api_db`
* **Password:** `pas_api_db`

---

