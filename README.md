## Django FastStart Boilerplate

Welcome to Django FastStart Boilerplate – your quick and easy solution for initializing Django projects with speed and efficiency. This boilerplate comes with a well-organized project structure and pre-configured settings to kickstart your development process.

### Features
- JWT Authen
- User Management
  - Follow / Unfollow
- local compose
   + posgresql - default database
   + celery - for async task
   + rabbitmq - used with celery
- cli for working with containers

### Project Structure
#### Production
| Backend | Web |
| --- | --- |
| ... | ... |

#### Local
| Backend | Web |
| --- | --- |
| [localhost:8080](http://localhost:8080/) | --- |

### Development

#### Prerequisites
- Docker
- Makefile
- Python - pip
- Virtualenv (optional but recommended)

#### Installation
```shell
make build # Build container
```
#### Make changes
- Database schema changes
```shell
make makemigrations
make migrate
```
- Create super user
```shell
make superuser
```
- shutdown
```shell
make down
make down-v
```

#### Seed Data
- create dump users
```shell
make seed_user count=10
```
- make users follow others
```shell
make seed_relationships count=50
```
For more commands, refer to the [Makefile](./makefile).

### Contribution
If you have suggestions for improvements or spot any issues with the project, feel free to submit an issue or pull request to this repo. Your contributions are highly valued!