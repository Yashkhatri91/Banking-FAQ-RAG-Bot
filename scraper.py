import requests, time
from bs4 import BeautifulSoup
 
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120"}
 
def scrape_faq_page(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        for tag in soup.find_all(["script", "style"]):
            tag.decompose()
        text = soup.get_text(separator="\n", strip=True)
        lines = [l for l in text.split("\n") if l.strip()]
        return "\n".join(lines)
    except Exception as e:
        print(f"Could not scrape {url}: {e}")
        return None
 
FAQ_SOURCES = {
    "Emirates NBD FAQ": "https://www.emiratesnbd.com/en/help-and-support",
    "FAB Help":         "https://www.bankfab.com/en-ae/personal/help-and-support",
"FAB FAQs":         "https://www.bankfab.com/en-ae/personal/help-and-support/faqs",}
 
all_text = []
for name, url in FAQ_SOURCES.items():
    print(f"Scraping {name}...")
    text = scrape_faq_page(url)
    if text:
        all_text.append(f"\n\n=== {name} ===\n\n" + text)
        print(f"  Done: {len(text)} characters collected")
    time.sleep(2)
 
combined_text = "\n\n".join(all_text)
 
with open("raw_faq_text.txt", "w", encoding="utf-8") as f:
    f.write(combined_text)
 
print(f"\nAll done. Total characters: {len(combined_text)}")
print("Saved to raw_faq_text.txt - open this file to review")
