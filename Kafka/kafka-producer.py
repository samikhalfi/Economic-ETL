import requests
from kafka import KafkaProducer
import json
import time

# Your API key and API endpoint
API_KEY = 'TZyVXGH43NEyryARjXThVbKIPoSVUYLI'
API_URL = 'https://financialmodelingprep.com/api/v3/search?query=AA'

# Kafka topic to use
TOPIC = 'stock_data'

# Function to get stock data from the API using the API key
def fetch_stock_data():
    params = {
        'apikey': API_KEY
    }
    response = requests.get(API_URL, params=params)
    
    if response.status_code == 200:
        return response.json()  # Return the JSON data from the API
    else:
        print(f"Error fetching data: {response.status_code}")
        return None

# Kafka Producer function to send data
def kafka_producer():
    producer = KafkaProducer(
        bootstrap_servers=['localhost:9092'],  # Adjust if your Kafka server is running on a different host
        value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Serialize data to JSON format
    )

    while True:
        stock_data = fetch_stock_data()
        if stock_data:
            producer.send(TOPIC, value=stock_data)
            print(f"Sent data to Kafka: {stock_data}")
        time.sleep(60)  # Fetch data every minute

    producer.flush()
    producer.close()

if __name__ == "__main__":
    kafka_producer()
