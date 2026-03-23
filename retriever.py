import openai
import chromadb
from dotenv import load_dotenv
import os

load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="faq_vectors")

def get_embedding(text):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

def ask_bot(question):
    print(f"\nQuestion: {question}")
    print("-" * 50)

    question_embedding = get_embedding(question)

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=3
    )

    retrieved_chunks = results["documents"][0]
    context = "\n\n".join(retrieved_chunks)

    print("Relevant FAQ sections found:")
    for i, chunk in enumerate(retrieved_chunks):
        print(f"  Chunk {i+1}: {chunk[:80]}...")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful banking assistant for Emirates NBD and FAB bank customers in the UAE. Answer questions using ONLY the FAQ content provided. If the answer is not in the provided content, say so clearly. Be concise and accurate."
            },
            {
                "role": "user",
                "content": f"FAQ Content:\n{context}\n\nCustomer Question: {question}"
            }
        ]
    )

    answer = response.choices[0].message.content
    print(f"\nAnswer: {answer}")
    return answer

print("Banking FAQ Bot ready. Testing with sample questions...\n")

ask_bot("How do I open an account at Emirates NBD?")
ask_bot("What documents do I need for a personal loan at FAB?")
ask_bot("What is the maximum tenure for an Emirates NBD personal loan?")