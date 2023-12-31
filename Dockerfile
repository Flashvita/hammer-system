FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app/backend
COPY ./requirements.txt /app/backend/requirements.txt
RUN pip install -r requirements.txt
COPY . /app/backend

