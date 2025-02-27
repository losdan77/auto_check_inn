FROM python:3.12

RUN mkdir /app

WORKDIR /app

COPY requeriments.txt .

RUN pip install -r requeriments.txt

COPY . .

RUN chmod a+x /app/*.sh

CMD [ "gunicorn", "main:app", "--workers", "2", "--timeout", "960", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000" ]