# importing required modules
from datetime import datetime
from pathlib import Path
import re
import fitz

# Opening document
doc = fitz.open(Path(__file__).parents[2] / 'schoolshootersinfo/Kimveer_Gill/documents/Kimveer Gill Online Electronic Version.pdf')

# Extracting text
pages = []
for page in doc:
    pages.append(page.get_text().rstrip())

# Split into posts
posts = re.split(r"\s+--------\s+", "".join(pages))


# post cleaning
def row_builder(post: str):
    # Find header and body
    header = "".join(re.split(r'(\b\d{2}:\d{2}:[ap]m\b)', post)[:2]).replace("\n", "")
    body = post.replace(header, "").replace("\n", " ").strip()

    # Sort out title from header
    date_regex = "(January|February|March|April|May|June|July|August|September|October|November|December) \d{2}, \d{4}, \d{2}:\d{2}:(am|pm)"
    match = re.search(date_regex, header)
    datestring = match.group() if match else ""
    title = header.replace(datestring, "").replace("\n", "")

    # Convert date format
    date = datetime.strptime(datestring, "%B %d, %Y, %H:%M:%p")
    datestring = date.strftime("%Y-%m-%d")
    res = datestring + "‎ " + title + body
    return res


# Create data.csv
with open(Path(__file__).parent / "data.csv", "w+") as f:
    f.write("date‎ text\n")
    for post in posts:
        f.write(row_builder(post))
        f.write("\n")
