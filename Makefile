.PHONY: build up down restart logs runserver shell migrate makemigrations test startapp createsuperuser format

build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

restart:
	docker compose restart

logs:
	docker compose logs -f

runserver:
	docker compose exec web python manage.py runserver 0.0.0.0:8000

# Django
migrate:
	docker compose exec web python manage.py migrate

makemigrations:
	docker compose exec web python manage.py makemigrations

shell:
	docker compose exec web python manage.py shell

createsuperuser:
	docker compose exec web python manage.py createsuperuser

startapp:
	docker compose exec web python manage.py startapp $(name)

# Linters
format:
	docker compose exec web black .
	docker compose exec web isort .

# Tests
test:
	docker compose exec web pytest

# Celery
celery-logs:
	docker compose logs -f celery