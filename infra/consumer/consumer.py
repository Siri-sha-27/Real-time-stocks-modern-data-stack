#Import requirements
import json
import boto3
import time
from kafka import KafkaConsumer

#Minio Connection
s3 = boto3.client(
    "s3",
    endpoint_url="http://localhost:9002",
    aws_access_key_id="Sirisha",
    aws_secret_access_key="Sirisha123"
)

bucket_name = "bronze-transactions"

#Define Consumer
consumer1 = KafkaConsumer(
    "stock-quotes",
    bootstrap_servers=["localhost:29092"],
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="bronze-consumer",
    value_deserializer=lambda v: json.loads(v.decode("utf-8"))
)

print("Consumerstreaming and saving to MinIO...")

#Main Function
for message in consumer1:
    record = message.value
    symbol = record.get("symbol", "unknown")
    ts = record.get("fetched_at",int(time.time()))
    key = f"{symbol}/{ts}.json"

    s3.put_object(
        Bucket=bucket_name,
        Key=key,
        Body=json.dumps(record),
        ContentType="application/json"
    )
    print(f"Saved record for {symbol} = s3://{bucket_name}/{key}")
                    