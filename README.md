# ArxivLens — Evidence-Driven Research Intelligence

## Problem Statement

Research papers are published faster than researchers can manually review them.
ArxivLens aims to help users discover relevant research and generate evidence-grounded answers from scientific papers.

## Planned Pipeline

arXiv → PySpark ETL → Parquet → Embeddings → Chroma → RAG → FastAPI

## Results

| Metric | Result |
|---|---|
| Abstracts collected | Pending |
| Records after cleaning | Pending |
| Retrieval quality | Pending |
| Answer quality | Pending |

## Project Structure

- `data/raw/` — Raw research records
- `data/processed/` — Processed datasets
- `etl/` — Data ingestion and transformation
- `rag/` — Retrieval-Augmented Generation
- `api/` — FastAPI endpoints
- `agents/` — Research agent workflows
- `eval/` — Evaluation scripts
- `docs/` — Documentation
- `tests/` — Automated tests

## Technologies

Python, arXiv API, PySpark, Parquet, embeddings, Chroma, RAG, and FastAPI.
