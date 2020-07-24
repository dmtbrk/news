# News

This is a HackerNews-like API server developed with Django REST Framework.

## How to run

`.env` file should be present in root directory:
```
DEBUG=1

HOST=localhost
PORT=8000

DATABASE_URL=postgresql://postgres:postgres@db:5432/postgres
```

Install packages:
```
pip install -r requirements.txt
```

Run docker-compose:
```
docker-compose up
```

## How to use

Import Postman collection:

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/270385be41e987fed7f0#?env%5BNEWS_PROD%5D=W3sia2V5IjoiQUREUiIsInZhbHVlIjoiaHR0cDovL2Rlc29sYXRlLW1lYWRvdy00ODQ5MS5oZXJva3VhcHAuY29tIiwiZW5hYmxlZCI6dHJ1ZX1d)

The Postman environment variable `ADDR` is set to `https://desolate-meadow-48491.herokuapp.com` to test against (hopefully) running Heroku dyno.
