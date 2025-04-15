
# ⚡ Real-Time Sentiment Analysis with Kafka, PostgreSQL & Elasticsearch

> A deep dive into building a fast, fault-tolerant streaming NLP pipeline using Kafka, VADER, Logstash, and Streamlit.

---

## 🚀 Introduction
![kafka-logstash-database drawio (1)](https://github.com/user-attachments/assets/0c68533f-70ce-4f71-b220-792da24e4ad8)

What if you could detect sentiment in real-time from a firehose of messages - and make that data instantly searchable and visible on a live dashboard?

In this blog, we'll show you how to build exactly that:

- 🔁 Kafka - Real-time message streaming backbone that decouples producers and consumers  
- 🤖 Faker + VADER - Synthetic text generator plus a lightweight NLP sentiment analyzer  
- 💾 PostgreSQL - Durable storage and source of truth for sentiment analysis  
- 🔍 Logstash + Elasticsearch - Real-time ingestion and full-text search engine for blazing-fast keyword queries  
- 📊 Streamlit - Lightweight, Pythonic UI layer that pulls from Postgres for live dashboards  
- 🧭 Kafka Manager UI (localhost:9000) - Monitor your Kafka cluster, check topic offsets, consumer lags, and inspect replication health with a visual control panel

Whether you're processing customer feedback, social sentiment, or live chat, this pipeline is the launchpad to build real-time intelligence into your stack.

---

## 🧠 Use Case

You're building a dashboard that answers: "How do people feel right now about our product?"  
To get there, you need to:  
- Continuously ingest new messages  
- Analyze them instantly  
- Store them reliably  
- Make them instantly searchable  
- Display them beautifully

---

## 🧱 Architecture at a Glance

---

## 🔧 Components Breakdown
<table>
  <tr>
    <td><img src="https://github.com/user-attachments/assets/2ee1310f-d8c1-43a5-aef7-9ab105dd4bb2" width="100%"></td>
    <td><img src="https://github.com/user-attachments/assets/7a4efd4f-2b24-4dda-9cb3-301363acb016" width="100%"></td>
  </tr>
  <tr>
    <td><img src="https://github.com/user-attachments/assets/7e9d0a52-f824-4a23-808a-9d38be5b8ded" width="100%"></td>
    <td><img src="https://github.com/user-attachments/assets/4d897330-affd-4ee4-9d55-a33c26619b83" width="100%"></td>
  </tr>
  <tr>
    <td><img src="https://github.com/user-attachments/assets/dda124df-5b71-41b1-84ac-db24043ad1c1" width="100%"></td>
    <td><img src="https://github.com/user-attachments/assets/90bd2baa-c3ff-4d0e-953f-5eadcac5740b" width="100%"></td>
  </tr>
  <tr>
    <td><img src="https://github.com/user-attachments/assets/6ab0a9a5-490f-42b6-bc2f-e8bcf20b259d" width="100%"></td>
    <td><img src="https://github.com/user-attachments/assets/a6029a78-083f-4159-9b2f-23696d7362f6" width="100%"></td>
  </tr>
  <tr>
    <td><img src="https://github.com/user-attachments/assets/9a6f60df-7e34-4e0e-a367-315f91e8ee9f" width="100%"></td>
    <td><img src="https://github.com/user-attachments/assets/5e138623-a676-4f86-abd0-92c3d8fd2ca5" width="100%"></td>
  </tr>
</table>



### Python Producer (Dockerized)
- Generates fake sentences using Faker  
- Adds a UTC timestamp (created_at)  
- Pushes data into Kafka topic sentence  

### Python Consumer (Dockerized)
- Subscribes to topic sentence in consumer-group-db  
- Applies VADER sentiment scoring  
- Inserts results into PostgreSQL  

### Logstash (Localhost)
- Independent consumer from the same topic using logstash-sentence-consumer  
- Transports raw messages to Elasticsearch  

### PostgreSQL (Docker)
- Serves as the long-term sentiment database  
- Feeds into the Streamlit dashboard  

### Elasticsearch + Kibana
- Powers full-text search  
- Visualizes indexed data from Kafka/Logstash  

### Streamlit UI (Docker)
- Live-updating dashboard powered by SQL  
- Clean and simple interface for viewing sentiment trends  

---

## 🔌 Kafka Listener Logic: Internal vs External

Kafka is configured with dual listeners:  
```
KAFKA_LISTENERS: INSIDE://0.0.0.0:9093,OUTSIDE://0.0.0.0:9092  
KAFKA_ADVERTISED_LISTENERS: INSIDE://kafka:9093,OUTSIDE://localhost:9092  
```

This separation lets external tools connect to Kafka securely and reliably, while Docker containers interact via internal DNS.

---

## 🧑‍💻 Kafka Manager UI

Kafka Manager is available at http://localhost:9000 and offers a rich GUI for monitoring Kafka health.

- View partitions and offsets  
- Track consumer group lag  
- Monitor topic replication  
- Inspect ISR (in-sync replicas)  

It’s your one-stop GUI for Kafka health.

---

## 🔄 Data Flow in Action

### Step 1: Faker + Timestamp → Kafka
```python
KafkaProducer().send('sentence', {'sentence': 'This is great!', 'created_at': '2025-04-14T08:00:00Z'})
```

### Step 2: VADER Sentiment → PostgreSQL
```sql
INSERT INTO sentences (sentence, sentiment, created_at)  
VALUES ('This is great!', 0.85, '2025-04-14T08:00:00Z');
```

### Step 3: Logstash → Elasticsearch
```json
{
  "sentence": "This is great!",
  "created_at": "2025-04-14T08:00:00Z"
}
```

### Step 4: Search via Postman
```
GET /sentence_idx/_search?q=great
```

### Step 5: Streamlit Dashboard (Live SQL View)
```sql
SELECT * FROM sentences ORDER BY created_at DESC;
```

---

## 🤝 Why Use One Kafka Topic With Two Consumer Groups?

Kafka retains the message log. Each consumer group reads independently, maintains its own offset, and can scale separately.

**Benefits:**  
- 🔗 Loose coupling  
- 🔁 Replayability  
- 🔍 Independent fault tolerance

---

## 🐳 Docker Stack Overview

Kafka is tuned with:  
```
KAFKA_LOG_RETENTION_MS: 172800000      # 2 days  
KAFKA_LOG_RETENTION_BYTES: 1073741824  # 1 GB  
```

---

## 🧵 Exactly-Once Semantics in Python?

Kafka supports idempotent producers natively  
To avoid duplicates in PostgreSQL:  
- Use ON CONFLICT DO NOTHING  
- Or de-duplicate using primary keys (e.g., hash of sentence + timestamp)  

For stricter guarantees, look into Kafka Streams + transactional producers.

---

## 📊 Results

- End-to-end latency under 1 second  
- Searchable & queryable sentiment data  
- Modular, fault-tolerant architecture

---

## 🧪 Try It Yourself

🧑‍💻 GitHub Repo: [hasnain393/kafka-postgres-elasticsearch-sync](https://github.com/hasnain393/kafka-postgres-elasticsearch-sync)  
```bash
git clone https://github.com/hasnain393/kafka-postgres-elasticsearch-sync
cd kafka-postgres-elasticsearch-sync
docker-compose up --build
```

Then visit:  
- 🧭 http://localhost:8501 — Streamlit Dashboard  
- 📦 http://localhost:9000 — Kafka Manager  
- 🔍 http://localhost:9200 — Elasticsearch (query with Postman)  

---

## ✅ Wrap Up

You now have a scalable architecture that transforms real-time messages into structured, searchable, and visualized insights.

Use it to:  
- Monitor brand sentiment  
- Tag customer messages  
- Search support queries  
- Or power your next NLP-based SaaS platform

---

Let me know if you'd like a part two on Kafka Connect, Kafka Streams, or multi-node clustering!






