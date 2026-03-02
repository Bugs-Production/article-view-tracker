# Article View Tracker

Backend-сервис для отслеживания просмотров статей.

## Стек

- Python 3.12 + Django 5.1 + Django REST Framework
- PostgreSQL 16
- Redis 7
- Celery + Celery Beat
- Docker / Docker Compose

## Запуск

### Требования

- Docker
- Docker Compose
- Make

### Шаги

```bash
# 1. Клонировать репозиторий
git clone <repo_url>
cd article-view-tracker

# 2. Создать файл с переменными окружения
cp .env.example .env

# 3. Собрать образы
make build

# 4. Поднять контейнеры
make up

# 5. Применить миграции
make migrate

# 6. Запустить сервер
make runserver
```

Сервис доступен по адресу: `http://localhost:8000`

### Полезные команды

```bash
make up               # поднять контейнеры в фоне
make down             # остановить контейнеры
make logs             # логи всех сервисов
make migrate          # применить миграции
make makemigrations   # создать миграции
make shell            # Django shell
make test             # запустить тесты
make format           # форматирование кода (black + isort)
make createsuperuser  # создать суперпользователя для /admin/
```

## API

| Метод | URL | Описание |
|-------|-----|----------|
| `GET` | `/api/v1/articles/` | Список опубликованных статей |
| `POST` | `/api/v1/articles/` | Создать статью |
| `POST` | `/api/v1/articles/{id}/view/` | Зафиксировать просмотр |
| `GET` | `/api/v1/articles/popular/` | Топ статей за 24 часа |

### Примеры запросов

**Создать статью:**
```bash
curl -X POST http://localhost:8000/api/v1/articles/ \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "title": "My Article", "content": "Content here"}'
```

**Зафиксировать просмотр:**
```bash
curl -X POST http://localhost:8000/api/v1/articles/1/view/ \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1}'
```

**Получить популярные статьи:**
```bash
curl http://localhost:8000/api/v1/articles/popular/
```

## Архитектурные решения

### Производительность

**Учёт просмотров без узкого места в БД**

При высокой нагрузке наивный подход `UPDATE articles SET views = views + 1` создаёт row-level lock на одну строку. При тысячах просмотров в минуту это очередь ожидания и деградация всего сервиса.

Решение разделено на два уровня:
- `POST /articles/{id}/view` делает только `INSERT` в таблицу `ArticleView` — каждый просмотр это новая строка, блокировок нет, PostgreSQL легко держит тысячи параллельных вставок
- Обновление счётчика `views_counter` в статье выполняется асинхронно через Celery с использованием `F('views_counter') + 1` (атомарный UPDATE без race condition)

**Кеширование популярных статей**

`GET /articles/popular/` выполняет агрегирующий запрос с `COUNT` и `GROUP BY` по таблице `ArticleView`. При высокой нагрузке этот запрос не должен выполняться на каждый HTTP запрос.

Используется паттерн **cache-aside**:
1. Проверяем Redis — есть кеш? Возвращаем сразу
2. Нет — выполняем запрос к БД, кешируем результат на 5 минут
3. При тысячах запросов в минуту тяжёлый SQL выполняется раз в 5 минут

### Redis

Redis используется в двух ролях:

| Роль | Что хранит | TTL |
|------|-----------|-----|
| Кеш | Результат `/articles/popular/` | 5 минут |
| Брокер задач | Очередь Celery задач | — |

### Масштабирование

- **Web-слой** — горизонтально масштабируется добавлением воркеров gunicorn или репликами контейнера за load balancer
- **Celery workers** — независимо масштабируются для обработки очереди задач
- **PostgreSQL** — read replicas для снятия нагрузки с мастера на чтение
- **Redis** — Redis Cluster или Sentinel для высокой доступности кеша

### Фоновые задачи (Celery Beat)

| Задача | Расписание | Описание |
|--------|-----------|----------|
| `cleanup_old_article_views` | Раз в сутки | Удаляет записи `ArticleView` старше 30 дней |

Очистка старых записей необходима чтобы таблица `ArticleView` не росла бесконечно. Общий счётчик просмотров сохраняется в поле `Article.views_counter`.

### Rate Limiting

DRF throttling используется как бизнес-инструмент для ограничения накрутки просмотров:
- Глобально: `100 запросов/мин` для всех эндпоинтов
- `POST /articles/{id}/view/`: дополнительно `10 запросов/мин`

Защита от DDoS — зона ответственности инфраструктуры (Nginx / WAF).

### Структура проекта

```
api/                    # API слой (контроллеры, сериализаторы, роуты)
│ └── articles/
articles/               # Доменный слой
│ ├── models.py          # Модели данных
│ ├── managers.py        # Операции с БД
│ ├── services/          # Бизнес-логика
│ ├── mappers.py         # Преобразование данных
│ ├── tasks.py           # Celery задачи
│ └── transfer_objects/  # DTO
core/                   # Конфигурация Django
```