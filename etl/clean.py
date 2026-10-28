
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, trim, regexp_replace, length, split

spark = (
    SparkSession.builder
    .appName("ArxivLensDataCleaning")
    .getOrCreate()
)

# Step 1: Read raw JSON Lines data
df = spark.read.json("data/raw/arxiv_raw.jsonl")

print("Original record count:", df.count())

# Step 2: Remove extra spaces from text columns
df = df.withColumn("title", trim(col("title")))
df = df.withColumn(
    "abstract",
    trim(regexp_replace(col("abstract"), r"\s+", " "))
)

# Step 3: Remove records with missing or empty abstracts
df = df.filter(
    col("abstract").isNotNull() &
    (length(col("abstract")) > 0)
)

# Step 4: Remove duplicate papers by ID
df = df.dropDuplicates(["id"])

# Step 5: Calculate abstract word count
df = df.withColumn(
    "word_count",
    length(trim(col("abstract"))) -
    length(regexp_replace(trim(col("abstract")), r"\s+", "")) + 1
)

print("Cleaned record count:", df.count())

# Step 6: Preview cleaned data
df.select("id", "title", "word_count").show(5, truncate=50)

# Step 7: Save cleaned data in Parquet format
df.write.mode("overwrite").parquet("data/processed/arxiv_clean")

print("Cleaning completed successfully!")

spark.stop()
