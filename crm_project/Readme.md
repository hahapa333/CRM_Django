# CRM Project

CRM Project — это веб-приложение для управления клиентами, построенное на Django и PostgreSQL.

## Стек технологий

- **Backend**: Python, Django
- **Frontend**: JavaScript
- **База данных**: PostgreSQL
- **Контейнеризация**: Docker, Docker Compose
- **Линтинг**: Pylint

## Установка и запуск

### 1. Установка зависимостей

POSTGRES_DB=crm
POSTGRES_USER=crm_user
POSTGRES_PASSWORD=crm_pass
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

### 2. Настройка окружения

docker-compose up --build

### 3. После запуска контейнеров выполните миграции:

docker-compose exec web python manage.py migrate

### 4. Для проверки кода с помощью Pylint выполните:

docker-compose exec web pylint crm

```bash

### 1. Клонирование репозитория
```bash
git clone <URL_репозитория>
cd crm_project

