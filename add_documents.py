import requests
from bs4 import BeautifulSoup
import time

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120"}

def fetch_pdf(url, label):
    print(f"Fetching {label}...")
    try:
        response = requests.get(url, headers=HEADERS, timeout=20)
        response.raise_for_status()
        filename = "temp_fab.pdf"
        with open(filename, "wb") as f:
            f.write(response.content)
        from pypdf import PdfReader
        reader = PdfReader(filename)
        text = ""
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
        lines = [l for l in text.split("\n") if l.strip()]
        clean = "\n".join(lines)
        print(f"  Done: {len(clean)} characters")
        return clean
    except Exception as e:
        print(f"  Failed: {e}")
        return ""

FAB_DOCS = {
    "FAB KFS - Credit Cards": "https://apply.bankfab.com/-/media/fabgroup/home/personal/key-facts-statements/fab-consolidated-credit-cards.pdf?view=1",
    "FAB Fees and Charges": "https://www.bankfab.com/-/media/fabgroup/home/personal/charges-and-fees/fees-and-charges-first-abu-dhabi-bank.pdf?view=1",
}

all_content = []

print("Fetching FAB documents...")
print("")

for label, url in FAB_DOCS.items():
    text = fetch_pdf(url, label)
    if text:
        all_content.append(f"\n\n=== {label} ===\n\n{text}")
    time.sleep(2)

combined = "\n".join(all_content)

with open("master_faq.txt", "a", encoding="utf-8") as f:
    f.write(combined)

print("")
print(f"Documents added: {len(all_content)}")
print(f"Characters added: {len(combined)}")
print("master_faq.txt updated")
