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

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/270385be41e987fed7f0)

Run server and test locally with default `ADDR` Postman variable or replace it with `https://desolate-meadow-48491.herokuapp.com` to test against (hopefully) running Heroku dyno.
