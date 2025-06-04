FROM python:3.12.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY streams.py .

CMD ["faust", "-A", "streams", "worker", "-l", "info"]
