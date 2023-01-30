FROM python:3.8-slim-buster

RUN apt-get update &&\
    apt install --assume-yes gunicorn

COPY pyproject.toml poetry.lock ./

RUN pip install poetry &&\
    poetry config virtualenvs.in-project true &&\
    poetry install

 EXPOSE 8050

COPY . ./

CMD python /frontend_app/app.py

