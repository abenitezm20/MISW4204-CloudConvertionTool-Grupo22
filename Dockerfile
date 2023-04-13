FROM python:3.9-slim-buster
WORKDIR /conversiontool
RUN apt-get update && apt-get -y install libpq-dev gcc
COPY . .
RUN pip3 install -r requirements.txt
RUN ls
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]