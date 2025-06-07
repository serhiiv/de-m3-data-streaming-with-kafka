FROM python:3.12.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN mkdir -p data

COPY producer.py .

CMD ["python", "producer.py"]
