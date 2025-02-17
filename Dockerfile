FROM python:3.12

RUN mkdir /app

WORKDIR /app

COPY requeriments.txt .

RUN pip install -r requeriments.txt

COPY . .

RUN chmod a+x /app/*.sh

CMD [ "gunicorn", "backend.main:app", "--workers", "1", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000" ]