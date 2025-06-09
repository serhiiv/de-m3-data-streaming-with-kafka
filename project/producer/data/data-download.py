import random
import requests

# List your input filenames
urls = [
    "https://raw.githubusercontent.com/cardiffnlp/xlm-t/main/data/sentiment/english/train_text.txt",
    "https://raw.githubusercontent.com/cardiffnlp/xlm-t/main/data/sentiment/french/train_text.txt",
    "https://raw.githubusercontent.com/cardiffnlp/xlm-t/main/data/sentiment/german/train_text.txt",
    "https://raw.githubusercontent.com/cardiffnlp/xlm-t/main/data/sentiment/italian/train_text.txt",
]

all_lines = []
for url in urls:
    response = requests.get(url)
    response.raise_for_status()  # Ensure we notice bad responses
    all_lines.extend(response.content.decode("utf-8").splitlines())

random.shuffle(all_lines)
# Limit to 10000 lines
all_lines = all_lines[:5000] + ['Finita']

# Write to output file
with open("multilingual.txt", "w", encoding="utf-8") as out:
    for line in all_lines:
        out.write(line + "\n")
