FROM --platform=$BUILDPLATFORM python:3.7-alpine AS builder
EXPOSE 8000
WORKDIR /app 
COPY requirements.txt /app
RUN pip3 install -r requirements.txt --no-cache-dir
COPY . /app 
COPY ./entrypoint.sh /app/entrypoint.sh
CMD [ "/app/entrypoint.sh" ]

