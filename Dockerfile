FROM python:3.10.9-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /src

RUN mkdir -p /src

COPY ./requirements.txt /src/requirements.txt

RUN apt-get update
RUN apt-get install -y gcc
RUN apt-get install -y default-libmysqlclient-dev
RUN pip install --no-cache-dir --upgrade -r /src/requirements.txt

COPY ./ /src/

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]