FROM python:3.9-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PIP_ROOT_USER_ACTION=ignore

EXPOSE 8080

WORKDIR /opt/app

RUN apk add bash postgresql-client build-base postgresql-dev

COPY requirements.txt /opt/app/
RUN pip install --no-cache-dir --disable-pip-version-check -r requirements.txt

COPY . /opt/app

VOLUME ["/media"]