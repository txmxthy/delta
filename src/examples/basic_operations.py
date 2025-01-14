from pyspark.sql.types import StructType, StructField, StringType, IntegerType
from delta.tables import DeltaTable

def run_basic_operations(spark):
    # Define schema
    schema = StructType([
        StructField("id", IntegerType(), True),
        StructField("name", StringType(), True),
        StructField("age", IntegerType(), True)
    ])

    # Create initial data
    data = [
        (1, "John", 30),
        (2, "Alice", 25),
        (3, "Bob", 35)
    ]

    # Create DataFrame and write as Delta table
    print("Creating initial Delta table...")
    df = spark.createDataFrame(data, schema)
    df.write.format("delta").mode("overwrite").save("/app/data/delta-table")

    # Read from Delta table
    print("\nReading from Delta table:")
    delta_table = DeltaTable.forPath(spark, "/app/data/delta-table")
    delta_table.toDF().show()

    # Update data
    print("\nUpdating age for John...")
    delta_table.update(
        condition="name = 'John'",
        set={"age": "31"}
    )
    delta_table.toDF().show()

    # Insert new data
    print("\nInserting new record...")
    new_data = [(4, "Carol", 28)]
    new_df = spark.createDataFrame(new_data, schema)
    delta_table.alias("old").merge(
        new_df.alias("new"),
        "old.id = new.id"
    ).whenNotMatchedInsertAll().execute()

    delta_table.toDF().show()