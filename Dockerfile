FROM python:3.11.6-alpine3.17

ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apk update \
    && apk add --no-cache gcc musl-dev postgresql-dev python3-dev libffi-dev \
    && pip install --upgrade pip \
    && apk del gcc musl-dev postgresql-dev python3-dev libffi-dev \
    && rm -rf /var/cache/apk/*

COPY ./requirements.txt ./

RUN pip install -r requirements.txt

COPY ./ ./

EXPOSE 8000

CMD ["sh", "/app/django.sh"]