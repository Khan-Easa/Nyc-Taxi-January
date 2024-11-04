import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, dayofweek, hour, avg
from pyspark.sql.functions import unix_timestamp

# AWS credentials from environment variables
aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")

# Initialize Spark session with S3 configuration
spark = SparkSession.builder \
    .appName("NYC Taxi Data Processing") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .config("spark.hadoop.fs.s3a.access.key", aws_access_key) \
    .config("spark.hadoop.fs.s3a.secret.key", aws_secret_key) \
    .config("spark.hadoop.fs.s3a.endpoint", "s3.amazonaws.com") \
    .getOrCreate()

# S3 paths for raw and processed data
input_path_2023 = "s3a://nyc-taxi-data-sets/raw/Jan_2023/yellow_tripdata_2023-01.parquet"
input_path_2024 = "s3a://nyc-taxi-data-sets/raw/Jan_2024/yellow_tripdata_2024-01.parquet"
output_path_2023 = "s3a://nyc-taxi-data-sets/processed/Jan_2023/"
output_path_2024 = "s3a://nyc-taxi-data-sets/processed/Jan_2024/"

# Read raw data from S3
df_2023 = spark.read.parquet(input_path_2023)
df_2024 = spark.read.parquet(input_path_2024)

# Data cleaning: Drop rows with nulls in essential columns
df_2023_cleaned = df_2023.dropna(subset=["PULocationID", "DOLocationID", "fare_amount"])
df_2024_cleaned = df_2024.dropna(subset=["PULocationID", "DOLocationID", "fare_amount"])

# Calculate trip duration in minutes
df_2023_cleaned = df_2023_cleaned.withColumn(
    "trip_duration",
    (unix_timestamp("tpep_dropoff_datetime") - unix_timestamp("tpep_pickup_datetime")) / 60
)
df_2024_cleaned = df_2024_cleaned.withColumn(
    "trip_duration",
    (unix_timestamp("tpep_dropoff_datetime") - unix_timestamp("tpep_pickup_datetime")) / 60
)

# Add pickup day and hour columns
df_2023_cleaned = df_2023_cleaned.withColumn("pickup_day", dayofweek("tpep_pickup_datetime"))
df_2024_cleaned = df_2024_cleaned.withColumn("pickup_day", dayofweek("tpep_pickup_datetime"))

df_2023_cleaned = df_2023_cleaned.withColumn("pickup_hour", hour("tpep_pickup_datetime"))
df_2024_cleaned = df_2024_cleaned.withColumn("pickup_hour", hour("tpep_pickup_datetime"))

# Aggregation: Average fare amount by day and hour
df_2023_avg_fare = df_2023_cleaned.groupBy("pickup_day", "pickup_hour").agg(avg("fare_amount").alias("avg_fare"))
df_2024_avg_fare = df_2024_cleaned.groupBy("pickup_day", "pickup_hour").agg(avg("fare_amount").alias("avg_fare"))

# Write the processed data back to S3, creating the `processed` folder if it doesn’t exist
df_2023_avg_fare.write.mode("overwrite").parquet(output_path_2023)
df_2024_avg_fare.write.mode("overwrite").parquet(output_path_2024)

print("Processed data has been successfully saved to S3 in the 'processed' folder.")

# Stop Spark session
spark.stop()
