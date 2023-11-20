## DJANGO_SIMPLE_BOILERPLATE

## Getting Started

### Project Structure

| -- | -- |
| Backend | Web |
| ... | ... |

### With Docker (recommend)

```shell
docker compose -f local.yaml up --build -d --remove-orphans
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
