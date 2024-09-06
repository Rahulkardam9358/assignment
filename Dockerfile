FROM python:3.10-slim-bullseye
WORKDIR /home/app
COPY requirements.txt /home/app/requirements.txt
COPY . .
RUN pip install -r requirements.txt
