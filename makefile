build:
	docker compose -f local.yaml up --build -d --remove-orphans
up:
	docker compose -f local.yaml up -d

down:
	docker compose -f local.yaml down

show-logs:
	docker compose -f local.yaml logs

show-log-api:
	docker compose -f local.yaml logs api

makemigrations:
	docker compose -f local.yaml run --rm api python manage.py makemigrations

migrate:
	docker compose -f local.yaml run --rm api python manage.py migrate --database default

sync_cassandra:
	docker compose -f local.yaml run --rm api python manage.py sync_cassandra

db_shell:
	docker compose -f local.yaml run --rm api python manage.py dbshell

collectstatic:
	docker compose -f local.yaml run --rm api python manage.py collectstatic

superuser:
	docker compose -f local.yaml run --rm api python manage.py createsuperuser

down-v:
	docker compose -f local.yaml down -v

volume:
	docker volume inspect src_local_postgres_data

flake8:
	docker compose -f local.yaml exec api flake8 .

black-check:
	docker compose -f local.yaml exec api black --check --exclude=migrations .

black-diff:
	docker compose -f local.yaml exec api black --diff --exclude=migrations .

black:
	docker compose -f local.yaml exec api black --exclude=migrations .

isort-check:
	docker compose -f local.yaml exec api isort . --check-only --skip env --skip migrations

isort-diff:
	docker compose -f local.yaml exec api isort . --diff --skip env --skip migrations

isort:
	docker compose -f local.yaml exec api isort . --skip env --skip migrations

create-backup:
	docker compose -f local.yaml exec postgres backup.sh

list-backup:
	docker compose -f local.yaml exec postgres backups.sh

# Use: make seed_users count=50
seed_users:
	docker compose -f local.yaml exec api python manage.py seed_users ${count}

# Use: make seed_relationship count=50
seed_relationships:
	docker compose -f local.yaml exec api python manage.py seed_user_relationship ${count}

# Use: make seed_stories count=50
seed_stories:
	docker compose -f local.yaml exec api python manage.py seed_stories ${count}

# make command="python manage.py createsuperuser"
exec: 
	docker compose -f local.yaml exec api ${command}