import streamlit as st
import openai
import chromadb
import os
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_embedding(text):
    res = client.embeddings.create(model="text-embedding-3-small", input=text)
    return res.data[0].embedding

def build_database():
    with open("master_faq.txt", "r", encoding="utf-8") as f:
        raw_text = f.read()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=150,
        separators=["\n\nQ:", "\n\n===", "\n\n", "\n", " "]
    )
    chunks = splitter.split_text(raw_text)
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    existing = [c.name for c in chroma_client.list_collections()]
    if "faq_vectors" in existing:
        chroma_client.delete_collection(name="faq_vectors")
    collection = chroma_client.get_or_create_collection(name="faq_vectors")
    for i, chunk in enumerate(chunks):
        embedding = get_embedding(chunk)
        collection.add(documents=[chunk], embeddings=[embedding], ids=["chunk_" + str(i)])
    return collection

def get_collection():
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    existing = [c.name for c in chroma_client.list_collections()]
    if "faq_vectors" in existing:
        collection = chroma_client.get_collection(name="faq_vectors")
        if collection.count() > 0:
            return collection
    st.info("Building knowledge base for first time. Please wait 2 minutes...")
    return build_database()

def get_answer(question, collection):
    q_embed = get_embedding(question)
    results = collection.query(query_embeddings=[q_embed], n_results=3)
    context = "\n\n".join(results["documents"][0])
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful UAE banking assistant for Emirates NBD and FAB. Answer using ONLY the FAQ content provided. If the answer is not in the content say: I dont have that information in my FAQ database. Be concise and accurate."},
            {"role": "user", "content": "FAQ Content:\n" + context + "\n\nCustomer question: " + question}
        ]
    )
    return response.choices[0].message.content

st.set_page_config(page_title="Banking FAQ Bot", layout="wide")
st.title("Emirates NBD and FAB Banking FAQ Assistant")
st.caption("Ask any question about accounts, cards, loans, or banking services.")

if "collection" not in st.session_state:
    st.session_state.collection = get_collection()

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! I can answer questions about Emirates NBD and FAB banking products. What would you like to know?"}]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask about accounts, cards, loans..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Searching FAQ database..."):
            answer = get_answer(prompt, st.session_state.collection)
        st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
