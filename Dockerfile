FROM python:3.9-slim-buster
WORKDIR /app
RUN apt-get update && apt-get -y install libpq-dev gcc
COPY . .
RUN pip3 install -r requirements.txt
# CMD ["gunicorn", "--conf", "./gunicorn.conf.py", "app:app", "--bind", "0.0.0.0:5000"]