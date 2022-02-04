# My Booking service

## General

### Short description

Booking API

### Technos

- Python 3
- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)

### Run local server

``` bash
virtualenv venv
source venv/bin/activate
pip install -r requirements-dev.txt
uvicorn booking.main:app --reload
```

[Swagger UI](http://localhost:8000/docs)
[Redoc UI](http://localhost:8000/redoc)
[Health_Check](http://localhost:8000/health)

### Run code lint

``` bash
flake8
```

### Run type checking

``` bash
mypy filexchange
```

### Format code

``` bash
black .
```

### Run Tests
```
pytest tests --junitxml report.xml --cov-report term --cov=booking
```

### Build container image

```bash
docker build -t book:test .
```

### Run container image

```bash
docker run -it -p 8080:80 book:test
```