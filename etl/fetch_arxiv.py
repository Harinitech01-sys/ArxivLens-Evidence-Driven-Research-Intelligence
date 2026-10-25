
import arxiv
import json
from pathlib import Path

OUTPUT_FILE = Path("data/raw/arxiv_raw.jsonl")
TARGET_PAPERS = 2000

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

client = arxiv.Client(
    page_size=100,
    delay_seconds=3,
    num_retries=3,
)

search = arxiv.Search(
    query="cat:cs.AI OR cat:cs.LG OR cat:cs.CL",
    max_results=TARGET_PAPERS,
    sort_by=arxiv.SortCriterion.SubmittedDate,
    sort_order=arxiv.SortOrder.Descending,
)

count = 0

with OUTPUT_FILE.open("w", encoding="utf-8") as file:
    for paper in client.results(search):
        record = {
            "id": paper.entry_id,
            "title": paper.title,
            "abstract": paper.summary,
            "categories": paper.categories,
            "primary_category": paper.primary_category,
            "published": paper.published.isoformat(),
        }

        file.write(json.dumps(record, ensure_ascii=False) + "\n")
        count += 1

        if count % 100 == 0:
            print(f"Collected {count}/{TARGET_PAPERS} papers")

        if count >= TARGET_PAPERS:
            break

print(f"Finished: {count} papers saved to {OUTPUT_FILE}")
