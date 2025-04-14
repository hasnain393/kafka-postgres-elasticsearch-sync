FROM python:3.8-slim

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app

COPY wait-for-it.sh wait-for-it.sh
COPY python-consumer.py .

RUN chmod +x wait-for-it.sh

CMD ["sh", "-c", "./wait-for-it.sh -s -t 30 \"$ZOOKEEPER_SERVER\" -- ./wait-for-it.sh -s -t 30 \"$KAFKA_SERVER\" -- python -u python-consumer.py"]
