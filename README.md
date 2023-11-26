## Instagram Stories Clone

## Getting Started

### Project Structure
#### Production
| Backend | Web |
| --- | --- |
| ... | ... |

### Local Development
| Backend | Web |
| --- | --- |
| [localhost:8080](http://localhost:8080/)  | --- |

### With Docker
1. Edit file .envs/.rabbitmq to update rabbitmq ip *RabbitMq use machine ip, localhost is not allowed*
```
CELERY_BROKER=amqp://guest:guest@{replace_current_machine_ip}:5672/
```
2. Build system
```shell
docker compose -f local.yaml up --build -d --remove-orphans
```
Or using makefile
```shell
make build # Build container
make down # Shutdown the container
```

### Local Installation

1. create Virtual environment (optional/suggest)
   Go to project folder, run these commands

```
virtualenv env
```

2. Activate virtual env
   For deactivate the env later, use `deactivate` cmd.

```
source env/bin/activate
```

3. Install Dependencies

```shell
python -m pip install -r requirements/local.txt
```

4. Connect the Database
   he project use SQLite for default. To connect to custom database, config the DATABASE VARIABLE in `config/settings/base.py`.

   Follow the Django docs for more details.

5. Migrate database adn staticfiles

```shell
python manage.py migrate --no-input
python manage.py collectstatic --no-input
```

6. Run the server through network

```shell
python manage.py runserver 0.0.0.0:8000
```

## Development
#### Seed Data
- Seed users instance
```shell
make seed_users count=20
```
- Seed users' relationships
```shell
make seed_relationships count=50
```
- Seed stories
```shell
make seed_stories count=50
```

For more commands -> [Makefile](./makefile)

## Contribution
If you have suggestions for improvements or spot any issues with the project, feel free to submit an issue or pull request to this [repo](https://github.com/tonible14012002/Instagram-Stories) 