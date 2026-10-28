
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = (
    SparkSession.builder
    .appName("ArxivLensValidation")
    .getOrCreate()
)

df = spark.read.parquet("data/processed/arxiv_clean")

print("Total papers:", df.count())

print("Missing IDs:", df.filter(
    col("id").isNull()
).count())

print("Missing titles:", df.filter(
    col("title").isNull()
).count())

print("Missing abstracts:", df.filter(
    col("abstract").isNull()
).count())

print("Empty abstracts:", df.filter(
    col("abstract") == ""
).count())

print("Zero-word abstracts:", df.filter(
    col("word_count") <= 0
).count())

print("Duplicate IDs:", df.count() - df.dropDuplicates(
    ["id"]
).count())

print("\nSample validated records:")
df.select(
    "id", "title", "word_count"
).show(5, truncate=50)

spark.stop()
