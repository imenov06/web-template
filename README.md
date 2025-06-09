# Шаблон веб-приложения с Telegram-ботом на FastAPI и Docker

Этот проект представляет собой готовый к развертыванию шаблон для создания веб-приложений на Python (с использованием FastAPI) с интегрированным Telegram-ботом, работающим через веб-хуки. Вся инфраструктура управляется с помощью Docker и Docker Compose.

## Основные компоненты

*   **Веб-приложение (FastAPI):** Находится в директории `web/`. Реализует API и логику для Telegram-бота.
*   **Telegram-бот:** Настраивается через переменные окружения и использует веб-хуки для получения обновлений.
*   **Nginx-proxy:** Обратный прокси-сервер, настроенный для работы с FastAPI и автоматического управления SSL-сертификатами. Конфигурация в `nginx/`.
*   **acme-companion:** Контейнер для автоматического получения и обновления SSL-сертификатов от Let's Encrypt.
*   **PostgreSQL:** Реляционная база данных для хранения данных приложения.
*   **Redis:** Быстрое хранилище ключ-значение, может использоваться для кеширования, сессий или задач Celery (если будет добавлено).
*   **Docker & Docker Compose:** Для контейнеризации и оркестрации всех сервисов.

## Структура проекта

```
.
├── .dockerignore        # Файлы, игнорируемые Docker при сборке
├── .gitignore           # Файлы, игнорируемые Git
├── README.md            # Этот файл
├── docker-compose.yml   # Конфигурация Docker Compose для всех сервисов
├── nginx/               # Конфигурация и Dockerfile для Nginx
│   ├── Dockerfile
│   └── ... (другие файлы конфигурации nginx)
└── web/                 # Исходный код Python-приложения (FastAPI, бот)
    ├── Dockerfile
    ├── requirements.txt (или pyproject.toml для Poetry/PDM)
    └── src/               # Основной исходный код
        ├── main.py        # Точка входа FastAPI
        ├── core/
        │   └── config.py  # Настройки приложения (Pydantic)
        ├── bot/
        │   └── ...        # Логика Telegram-бота
        └── ... (другие модули и компоненты)
```

## Предварительные требования

*   Docker
*   Docker Compose (обычно устанавливается вместе с Docker)
*   Зарегистрированный домен (или поддомен), DNS-запись которого указывает на IP-адрес сервера, где будет развернуто приложение (для получения SSL-сертификатов).

## Настройка и запуск

1.  **Клонируйте репозиторий:**
    ```bash
    git clone https://github.com/imenov06/web-template.git
    cd web-template
    ```

2.  **Создайте файл `.env`:**
    Создайте новый `.env` в корне проекта на основе следующего шаблона и заполните его вашими значениями:

    ```env
    # .env файл

    # --- Telegram Bot Settings ---
    BOT_TOKEN=ВАШ_ТЕЛЕГРАМ_БОТ_ТОКЕН
    DOMAIN_NAME=вашдомен.ru 
    WEBHOOK_PATH=/bot/hook/уникальный_путь # Например, /bot/hook/случайный-uuid
    WEBHOOK_SECRET=СУПЕР_СЕКРЕТНЫЙ_КЛЮЧ_ДЛЯ_ВЕБХУКА

    # --- PostgreSQL Settings ---
    POSTGRES_SERVER=db_postgres
    POSTGRES_USER=myuser
    POSTGRES_PASSWORD=mypassword
    POSTGRES_DB=mydatabase
    POSTGRES_PORT=5432 # Порт на хосте (если нужен внешний доступ)

    # --- Redis Settings ---
    REDIS_HOST=db_redis
    REDIS_PORT=6379    # Порт на хосте (если нужен внешний доступ)
    REDIS_DB=0
    REDIS_PASSWORD=yourStrongRedisPassword # Обязательно задайте, если используется requirepass

    # --- Nginx & Let's Encrypt ---
    # Домен(ы) для VIRTUAL_HOST и LETSENCRYPT_HOST (через запятую, без пробелов)
    ALLOWED_HOST=вашдомен.ru,www.вашдомен.ru
    LETSENCRYPT_EMAIL=ваш_email@example.com # Email для уведомлений от Let's Encrypt
    ```
    **Важно:**
    *   `BOT_TOKEN`: Токен вашего Telegram-бота.
    *   `DOMAIN_NAME`: Основной домен, на котором будет доступно приложение.
    *   `WEBHOOK_PATH`: Уникальный путь для веб-хука Telegram.
    *   `WEBHOOK_SECRET`: Секретный ключ для проверки подлинности запросов от Telegram к вашему веб-хуку.
    *   `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`: Учетные данные для PostgreSQL.
    *   `REDIS_PASSWORD`: Пароль для Redis (если настроен `requirepass`).
    *   `ALLOWED_HOST`: Список доменов и поддоменов, для которых Nginx будет принимать запросы и для которых будут выпускаться SSL-сертификаты.
    *   `LETSENCRYPT_EMAIL`: Ваш email для регистрации SSL-сертификатов Let's Encrypt.

3.  **Сборка и запуск контейнеров:**
    ```bash
    docker-compose build # Собрать образы (если есть изменения в Dockerfile или коде)
    docker-compose up -d # Запустить все сервисы в фоновом режиме
    ```
    Для просмотра логов используйте:
    ```bash
    docker-compose logs -f
    # или для конкретного сервиса, например, web:
    # docker-compose logs -f web
    ```

4.  **Настройка веб-хука Telegram (автоматически):**
    Приложение `web` при старте автоматически попытается установить веб-хук для Telegram, используя `DOMAIN_NAME` и `WEBHOOK_PATH` из `.env`.

5.  **Проверка:**
    *   Откройте ваш домен (`https://вашдомен.ru`) в браузере. Вы должны увидеть ответ от вашего FastAPI-приложения (если настроены соответствующие эндпоинты) или стандартную страницу Nginx, если приложение еще не отвечает.
    *   Проверьте работу Telegram-бота, отправив ему команду.

