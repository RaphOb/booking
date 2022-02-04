FROM tiangolo/uvicorn-gunicorn:python3.8

WORKDIR /app

COPY requirements.txt /app

RUN pip install -r requirements.txt

#EXPOSE 8080


COPY . /app
#CMD ["uvicorn", "booking.main:app", "--host", "0.0.0.0", "--port", "8080"]
