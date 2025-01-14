from pyspark.sql.functions import current_timestamp
from pyspark.sql.types import StructType, StructField, StringType, LongType, TimestampType
import time
import shutil
import os

def run_streaming_example(spark):
    # Create streaming data source
    data_path = "/app/data/streaming-source"
    checkpoint_path = "/app/data/checkpoints"
    output_path = "/app/data/streaming-output"

    print("Setting up streaming example...")

    # Clean up previous data if exists
    for path in [data_path, checkpoint_path, output_path]:
        if os.path.exists(path):
            shutil.rmtree(path)
        os.makedirs(path)

    # Define schema for streaming data
    schema = StructType([
        StructField("event_name", StringType(), True),
        StructField("value", LongType(), True),  # Changed from IntegerType to LongType
        StructField("timestamp", TimestampType(), True)
    ])

    # Generate sample streaming data
    query = None
    try:
        for i in range(3):
            df = spark.createDataFrame(
                [(f"event_{i}", i)],
                ["event_name", "value"]
            ).withColumn("timestamp", current_timestamp())

            df.write.format("parquet").mode("append").save(data_path)

            if i == 0:
                # Set up streaming query
                stream_df = spark.readStream \
                    .schema(schema) \
                    .format("parquet") \
                    .load(data_path)

                # Write stream to Delta table
                query = stream_df.writeStream \
                    .format("delta") \
                    .outputMode("append") \
                    .option("checkpointLocation", checkpoint_path) \
                    .start(output_path)

            print(f"Writing batch {i+1}/3...")
            time.sleep(2)

        # Wait for streaming to process all data
        if query:
            query.awaitTermination(timeout=10)  # Wait up to 10 seconds
            query.stop()

        # Read and show results if table exists
        if os.path.exists(output_path):
            print("\nStreaming results:")
            spark.read.format("delta").load(output_path).show()
        else:
            print("\nNo streaming results available - Delta table was not created")

    except Exception as e:
        print(f"Error in streaming example: {str(e)}")
    finally:
        if query:
            query.stop()