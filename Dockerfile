FROM python:3.12

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir --upgrade -r requirements.txt

ENTRYPOINT gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
