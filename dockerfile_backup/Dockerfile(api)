FROM python:3.9.21-slim

# System setup
RUN apt-get update && apt-get install -y build-essential gcc

RUN mkdir /volleyballdata
COPY . /volleyballdata/
WORKDIR /volleyballdata/

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
RUN pip install poetry
RUN poetry sync

RUN VERSION=RELEASE python genenv.py

CMD ["poetry", "run", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8888"]