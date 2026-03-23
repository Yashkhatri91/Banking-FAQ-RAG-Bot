import openai
import chromadb
from dotenv import load_dotenv
import os
 
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=api_key)
 
with open("master_faq.txt", "r", encoding="utf-8") as f:
    raw_text = f.read()
 
from langchain_text_splitters import RecursiveCharacterTextSplitter
splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=150,
    separators=["\n\nQ:", "\n\n===", "\n\n", "\n", " "])
chunks = splitter.split_text(raw_text)
print(f"Chunks to embed: {len(chunks)}")
 
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="faq_vectors")
 
def get_embedding(text):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding
 
for i, chunk in enumerate(chunks):
    print(f"Embedding chunk {i+1}/{len(chunks)}...", end="\r", flush=True)
    embedding = get_embedding(chunk)
    collection.add(documents=[chunk], embeddings=[embedding], ids=[f"chunk_{i}"])
 
print(f"\nDone. {len(chunks)} chunks embedded and stored in ChromaDB.")
print("Database saved in ./chroma_db folder")