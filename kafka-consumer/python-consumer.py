from kafka import KafkaConsumer
import json
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import psycopg2
import nltk

nltk.download('vader_lexicon')
analyzer = SentimentIntensityAnalyzer()

conn = psycopg2.connect(
  dbname="postgres",
  user="postgres",
  password="postgres",
  host="postgres",
  port="5432"
)
cur = conn.cursor()

kafka_nodes = "kafka:9093"
my_topic = "sentence"

consumer = KafkaConsumer(
    my_topic,
    bootstrap_servers=kafka_nodes,
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

for message in consumer:
    data = message.value
    print(data)
    scores = analyzer.polarity_scores(data['sentence'])
    cur.execute(
        "INSERT INTO sentences (sentence, sentiment, created_at) VALUES (%s, %s, %s)",
        (data['sentence'], scores['compound'], data['created_at'])
    )
    conn.commit()
