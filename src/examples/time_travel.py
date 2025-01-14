from delta.tables import DeltaTable
from pyspark.sql.functions import col

def run_time_travel(spark):
    # Create sample data with versions
    print("Creating versioned data...")

    # Version 0
    data_v0 = [(1, "Product A", 100),
               (2, "Product B", 200)]

    df_v0 = spark.createDataFrame(data_v0, ["id", "name", "price"])
    df_v0.write.format("delta").mode("overwrite").save("/app/data/products")

    # Version 1 - Update price
    delta_table = DeltaTable.forPath(spark, "/app/data/products")
    delta_table.update(
        condition="name = 'Product A'",
        set={"price": "150"}
    )

    # Version 2 - Add new product
    data_v2 = [(3, "Product C", 300)]
    df_v2 = spark.createDataFrame(data_v2, ["id", "name", "price"])
    delta_table.alias("old").merge(
        df_v2.alias("new"),
        "old.id = new.id"
    ).whenNotMatchedInsertAll().execute()

    # Show current version
    print("\nCurrent version:")
    delta_table.toDF().show()

    # Show version 0
    print("\nVersion 0:")
    spark.read.format("delta").option("versionAsOf", 0).load("/app/data/products").show()

    # Show version history
    print("\nVersion history:")
    delta_table.history().show()