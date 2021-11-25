  <div id='top'></div>
  <h1 align="center">Musikx</h3>

<!-- ABOUT THE PROJECT -->

## About The Project

First of all, let’s assume that there’s no streaming audio providers in the world. No Spotify, no Apple music... So, it’s time for us to create one!

Musikx is an audio streaming service provider, aiming to become the world's largest music streaming service provider.

There are millions of songs from a variety of genres and artists, from obscure indie rock, to top 40 pop, to movie soundtracks and classical music. Musikx provides a new way of music management.

- [Project proposal](./Proposal.pdf)
- [API Document](./Musikx.postman_collection.json)

### Built With

- [Django REST framework](https://www.django-rest-framework.org/)
- [PostgreSQL](https://www.postgresql.org/)
- [docker](https://www.docker.com/)
- [Travis CI](https://www.travis-ci.com/)
- [Postman](https://www.postman.com/pricing/)

<!-- GETTING STARTED -->

## Getting Started

### Prerequisites

This is a docker based project. Make sure that you have already istalled Docker engine and compose. [Get Docker](https://docs.docker.com/get-docker/)

### Run test in terminal

- [Test file](./app/core/tests/) location: ./app/core/tests

```sh
docker-compose run --rm app sh -c "python manage.py test && flake8"
```

Django starts much faster than Postgres DB, so a connection error will be raised. To solve this problm, a test case is created for the connection, and a loop will continue to test the connection until it becomes true. Then a command line will be called to start the app.

### Start

To start project, run:

```sh
# builds Docker images
docker-compose build
# run app
docker-compose up
```

The API will then be available at http://127.0.0.1:8000.

<!-- LICENSE -->

## License

Distributed under the MIT License. See [LICENSE](./LICENSE) for more information.
