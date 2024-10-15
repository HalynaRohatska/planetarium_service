FROM python:3.12-alpine3.18
LABEL maintainer="horatskahr@gmail.com"

ENV PYTHONUNBUFFERED=1

WORKDIR /app/

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

RUN adduser \
    --disabled-password \
    --no-create-home \
    my_user

RUN mkdir -p /files/media/uploads && \
    chown -R my_user /files/media

RUN chmod -R 755 /files/media

USER my_user