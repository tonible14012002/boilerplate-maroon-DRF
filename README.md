## Instagram Stories Clone

## Getting Started

### Project Structure
#### Production
| Backend | Web |
| --- | --- |
| ... | ... |

#### Local
| Backend | Web |
| --- | --- |
| [localhost:8080](http://localhost:8080/)  | --- |

### Development
#### prerequisite
- Docker
- Makefile
- Python - pip
- Virtualenv (optional - suggest)
#### Installation
### Run Server
- Build system
```shell
make build # Build container
```
### Make Changes
- Changes in database schema
```shell
make makemigrations
make migrate
```

- Create superuser
```shell
make superuser
```

- Shutdown system
```shell
make down
make down-v # for delete the volumn also
```

### Seed Data
- Seed users instance
```shell
make seed_users count=20
```
- Seed users' relationships
```shell
make seed_relationships count=50
```

For more commands -> [Makefile](./makefile)

## Contribution
If you have suggestions for improvements or spot any issues with the project, feel free to submit an issue or pull request to this [repo](https://github.com/tonible14012002/Instagram-Stories) 
