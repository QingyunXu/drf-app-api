# drf-app-api

## Run test in terminal

- [Test file](./app/core/tests/) location: ./app/core/tests

```sh
docker-compose run --rm app sh -c "python manage.py test && flake8"
```

## Getting started

To start project, run:

```sh
docker-compose up
```

The API will then be available at http://127.0.0.1:8000.

    Django starts much faster than Postgres DB, so a connection error will be raised. To solve this problm, a test case is created for the connection, and a loop will continue to test the connection until it becomes true. Then a command line will be called to start the app.
