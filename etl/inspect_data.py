
import sys
from pathlib import Path

sys.path.insert(0, r"D:\python-packages")

from pyspark.sql import SparkSession

Path(r"D:\spark-tmp").mkdir(parents=True, exist_ok=True)

spark = (
    SparkSession.builder
    .appName("ArxivLens")
    .master("local[*]")
    .config("spark.sql.shuffle.partitions", "8")
    .config("spark.local.dir", r"D:\spark-tmp")
    .getOrCreate()
)

print("Spark version:", spark.version)

df = spark.read.json("data/raw/arxiv_raw.jsonl")

print("\nDataset schema:")
df.printSchema()

print("\nTotal records:", df.count())

print("\nFirst 5 research papers:")
df.show(5, truncate=False)

spark.stop()
