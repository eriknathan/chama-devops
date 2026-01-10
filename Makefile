.PHONY: up down build logs migrate superuser shell test clean populate reset-db fresh-start help docs backup css-dev css-build

help:
	@echo "Available commands:"
	@echo "  make up          - Start containers in detached mode"
	@echo "  make down        - Stop containers"
	@echo "  make build       - Build containers"
	@echo "  make logs        - Follow logs"
	@echo "  make migrate     - Run database migrations"
	@echo "  make superuser   - Create a Django superuser"
	@echo "  make populate    - Populate database with initial data"
	@echo "  make shell       - Open Django shell"
	@echo "  make test        - Run tests"
	@echo "  make restart     - Run down and up"
	@echo "  make reset-db    - Stop containers and remove volumes (Full DB reset)"
	@echo "  make fresh-start - Reset DB, start containers, and migrate"
	@echo "  make clean       - Alias for reset-db"
	@echo "  make backup      - Create a database backup"
	@echo "  make css-dev     - Watch and compile Tailwind CSS (dev mode using Docker)"
	@echo "  make css-build   - Build minified Tailwind CSS (production)"
	@echo "  make css-logs    - Follow Tailwind build logs"

css-logs:
	docker-compose logs -f tailwind

up:
	docker-compose up -d

down:
	docker-compose down

restart:
	docker-compose down
	docker-compose up -d --build

build:
	docker-compose up -d --build

logs:
	docker-compose logs -f

migrate:
	docker-compose exec web python manage.py migrate

superuser:
	docker-compose exec web python manage.py createsuperuser

populate:
	docker-compose exec web python populate_db.py

shell:
	docker-compose exec web python manage.py shell

test:
	docker-compose exec web python manage.py test

reset-db:
	docker-compose down -v --remove-orphans
	@echo "Database volume removed. Run 'make up' and 'make migrate' to start fresh."

fresh-start: reset-db up
	@echo "Waiting for database to be ready..."
	@sleep 5
	$(MAKE) migrate
	@echo "Project ready! You can now run 'make populate' or 'make superuser'."

clean: reset-db

backup:
	@echo "Creating database backup..."
	docker-compose exec -T db bash -c 'pg_dump -U $$POSTGRES_USER $$POSTGRES_DB' > db_backup_$$(date +%Y-%m-%d_%H-%M-%S).sql
	@echo "Backup saved to current directory."

css-dev:
	npm run dev

css-build:
	npm run build
