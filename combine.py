with open("raw_faq_text.txt", "r", encoding="utf-8") as f:
    scraped = f.read()

with open("faq_manual.txt", "r", encoding="utf-8") as f:
    manual = f.read()

combined = scraped + "\n\n" + manual

with open("master_faq.txt", "w", encoding="utf-8") as f:
    f.write(combined)

print("Combined successfully!")
print(f"Scraped content: {len(scraped)} characters")
print(f"Manual content: {len(manual)} characters")
print(f"Total master file: {len(combined)} characters")