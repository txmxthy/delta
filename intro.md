# Delta Lake Fundamentals: A Practical Guide

## What is Delta Lake?

Delta Lake is an open-source storage layer that brings reliability to data lakes. Think of it as adding a sophisticated versioning system (like Git) to your data storage, with additional features that ensure data quality and reliability. Here are the key benefits it provides:

1. ACID Transactions: Ensures your data operations are reliable and consistent
2. Time Travel: Ability to access and restore previous versions of your data
3. Schema Enforcement: Prevents data corruption by enforcing consistent data structures
4. Support for Streaming: Can handle both batch and streaming data seamlessly

Let's explore these concepts through our demonstration project.

## Core Concepts Demonstrated

### 1. Basic Operations (CRUD)
Looking at `basic_operations.py`, we can see how Delta Lake handles fundamental data operations:

```python
# Create a table
df.write.format("delta").mode("overwrite").save("/app/data/delta-table")

# Read from the table
delta_table = DeltaTable.forPath(spark, "/app/data/delta-table")

# Update data
delta_table.update(
    condition="name = 'John'",
    set={"age": "31"}
)

# Insert new data using merge
delta_table.alias("old").merge(
    new_df.alias("new"),
    "old.id = new.id"
).whenNotMatchedInsertAll().execute()
```

This demonstrates how Delta Lake provides SQL-like operations while maintaining data integrity. The `merge` operation is particularly powerful as it handles upserts (update + insert) atomically.

### 2. Time Travel
The `time_travel.py` example shows one of Delta Lake's most powerful features:

```python
# Access specific version
spark.read.format("delta").option("versionAsOf", 0).load("/app/data/products")

# View version history
delta_table.history()
```

Every change to your data creates a new version, and you can:
- Access any previous version of your data
- Track what changes were made
- Restore data to a previous state if needed

### 3. Streaming Data
In `streaming.py`, we see how Delta Lake handles streaming data:

```python
stream_df = spark.readStream.schema(schema).format("parquet").load(data_path)

query = stream_df.writeStream
    .format("delta")
    .outputMode("append")
    .option("checkpointLocation", checkpoint_path)
    .start(output_path)
```

This demonstrates how Delta Lake can:
- Process streaming data with the same reliability as batch data
- Ensure exactly-once processing
- Maintain ACID properties even with streaming updates

## Running the Demo

The project uses Docker to simplify setup. Here's how to run it:

1. Create required directories:
```bash
mkdir -p data/delta-table data/products data/streaming-source data/streaming-output data/checkpoints
```

2. Start the container:
```bash
docker-compose up -d
```

3. Run the examples:
```bash
docker exec -it delta-spark-1 python3 -m src.main
```
