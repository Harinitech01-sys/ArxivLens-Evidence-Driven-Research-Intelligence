
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, count

spark = (
    SparkSession.builder
    .appName("ArxivLensEDA")
    .getOrCreate()
)

df = spark.read.parquet("data/processed/arxiv_clean")

# 1. Total number of papers
print("Total papers:", df.count())

# 2. Average abstract word count
df.select(
    avg("word_count").alias("average_words")
).show()

# 3. Papers grouped by year
if "year" in df.columns:
    df.groupBy("year").agg(
        count("*").alias("paper_count")
    ).orderBy("year").show()

# 4. Five papers with the longest abstracts
df.orderBy(
    col("word_count").desc()
).select(
    "id", "title", "word_count"
).show(5, truncate=50)

spark.stop()
