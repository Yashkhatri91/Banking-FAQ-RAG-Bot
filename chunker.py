from langchain_text_splitters import RecursiveCharacterTextSplitter

with open("master_faq.txt", "r", encoding="utf-8") as f:
    text = f.read()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1500,
    chunk_overlap=150,
    separators=["\n\nQ:", "\n\n===", "\n\n", "\n", " "]
)

chunks = splitter.split_text(text)

print(f"Total chunks created: {len(chunks)}")
print(f"Average chunk size: {len(text) // len(chunks)} characters")
print("\n--- First chunk preview ---")
print(chunks[0])
print("\n--- Last chunk preview ---")
print(chunks[-1])

with open("chunks_output.txt", "w", encoding="utf-8") as f:
    for i, chunk in enumerate(chunks):
        f.write(f"--- Chunk {i+1} ---\n{chunk}\n\n")

print("\nChunks saved to chunks_output.txt")