
import sys
from pathlib import Path

sys.path.insert(0, r"D:\python-packages")

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, trim, regexp_replace, size, split, year, to_timestamp
)

Path(r"D:\spark-tmp").mkdir(parents=True, exist_ok=True)

spark = (
    SparkSession.builder
    .appName("ArxivLens-ETL")
    .master("local[*]")
    .config("spark.sql.shuffle.partitions", "8")
    .config("spark.local.dir", r"D:\spark-tmp")
    .getOrCreate()
)

df = spark.read.json("data/raw/arxiv_raw.jsonl")

print("Records before cleaning:", df.count())

df = df.withColumn(
    "title",
    trim(regexp_replace(col("title"), r"\s+", " "))
).withColumn(
    "abstract",
    trim(regexp_replace(col("abstract"), r"\s+", " "))
)

df = df.filter(
    col("abstract").isNotNull() & (col("abstract") != "")
)

df = df.dropDuplicates(["id"])

df = df.withColumn(
    "word_count",
    size(split(col("abstract"), r"\s+"))
).withColumn(
    "year",
    year(to_timestamp(col("published")))
)

print("Records after cleaning:", df.count())

output_path = "data/processed/papers.parquet"
df.write.mode("overwrite").parquet(output_path)

print("Cleaned data saved to:", output_path)

spark.stop()
