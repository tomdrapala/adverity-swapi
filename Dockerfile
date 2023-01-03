FROM python:3.10-alpine

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE 1
WORKDIR /app
RUN apk update
RUN apk add postgresql-dev gcc python3-dev musl-dev
# COPY requirements.txt requirements.txt
ADD . .
RUN pip install -r requirements.txt
COPY docker-entrypoint.sh /scripts/docker-entrypoint.sh
RUN ["chmod", "+x", "/scripts/docker-entrypoint.sh"]
ENTRYPOINT [ "/scripts/docker-entrypoint.sh" ]
