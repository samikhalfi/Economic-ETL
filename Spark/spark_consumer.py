from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType, FloatType
from kafka import KafkaConsumer
import json

# Define your schema for stock data
schema = StructType() \
    .add("symbol", StringType()) \
    .add("name", StringType()) \
    .add("price", FloatType())

# Initialize Spark session
spark = SparkSession.builder \
    .appName("KafkaSparkCassandraConsumer") \
    .config("spark.cassandra.connection.host", "cassandra") \
    .getOrCreate()

# Kafka Consumer to read data
consumer = KafkaConsumer(
    'stock_data',
    bootstrap_servers=['localhost:9092'],  # Adjust if Kafka is on another server
    auto_offset_reset='earliest',
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))  # Deserialize JSON data
)

for message in consumer:
    stock_data = message.value
    # Create a DataFrame from the incoming stock data
    df = spark.read.json(spark.sparkContext.parallelize([stock_data]), schema)

    # Write to Cassandra
    df.write \
        .format("org.apache.spark.sql.cassandra") \
        .options(table="stocks", keyspace="your_keyspace") \
        .mode("append") \
        .save()

spark.stop()
