FROM python:3.12.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app.py .

CMD ["faust", "-A", "app", "worker", "-l", "info"]
