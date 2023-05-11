FROM python:3.9-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PIP_ROOT_USER_ACTION=ignore

WORKDIR /opt/app
COPY requirements.txt /opt/app/
RUN pip install -r --disable-pip-version-check requirements.txt
COPY . /opt/app

EXPOSE 8080

VOLUME ["/media"]