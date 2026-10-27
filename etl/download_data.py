
import json
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

OUTPUT = Path("data/raw/arxiv_raw.jsonl")
OUTPUT.parent.mkdir(parents=True, exist_ok=True)

params = urllib.parse.urlencode({
    "search_query": "cat:cs.AI",
    "start": 0,
    "max_results": 20,
    "sortBy": "submittedDate",
    "sortOrder": "descending",
})

url = f"https://export.arxiv.org/api/query?{params}"
request = urllib.request.Request(
    url,
    headers={"User-Agent": "ArxivLensStudentProject/1.0"}
)

with urllib.request.urlopen(request, timeout=60) as response:
    xml_data = response.read()

root = ET.fromstring(xml_data)
ns = {
    "atom": "http://www.w3.org/2005/Atom",
    "arxiv": "http://arxiv.org/schemas/atom",
}

count = 0

with OUTPUT.open("w", encoding="utf-8") as file:
    for entry in root.findall("atom:entry", ns):
        paper_id = entry.findtext("atom:id", default="", namespaces=ns)
        title = entry.findtext("atom:title", default="", namespaces=ns)
        abstract = entry.findtext("atom:summary", default="", namespaces=ns)
        published = entry.findtext("atom:published", default="", namespaces=ns)

        categories = [
            item.attrib["term"]
            for item in entry.findall("atom:category", ns)
            if "term" in item.attrib
        ]

        paper = {
            "id": paper_id.rstrip("/").split("/")[-1],
            "title": title,
            "abstract": abstract,
            "published": published,
            "primary_category": categories[0] if categories else None,
        }

        file.write(json.dumps(paper, ensure_ascii=False) + "\n")
        count += 1

print(f"Downloaded {count} papers to {OUTPUT}")
