from pyspark.sql import SparkSession
import os

def create_spark_session():
    return SparkSession.builder \
        .appName("DeltaLakeDemo") \
        .config("spark.jars.packages", "io.delta:delta-core_2.12:2.3.0") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .getOrCreate()

def main():
    print("Initializing Delta Lake Demo...")
    print(f"Current working directory: {os.getcwd()}")

    spark = create_spark_session()

    try:
        # Import and run examples with full path
        from src.examples.basic_operations import run_basic_operations
        from src.examples.time_travel import run_time_travel
        from src.examples.streaming import run_streaming_example

        print("\nRunning Basic Operations Example...")
        run_basic_operations(spark)

        print("\nRunning Time Travel Example...")
        run_time_travel(spark)

        print("\nRunning Streaming Example...")
        run_streaming_example(spark)

    except ImportError as e:
        print(f"Import error: {e}")
        print("Python path:", os.environ.get('PYTHONPATH'))
    finally:
        spark.stop()

if __name__ == "__main__":
    main()