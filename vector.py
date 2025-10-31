# امسح OllamaEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings # (ده الجديد)
from langchain_chroma import Chroma
from langchain_community.document_loaders import DirectoryLoader
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
import google.generativeai as genai # (ده الجديد)

# --- (ده الجديد: لازم تحط الـ Key بتاعك) ---
# (اوعى تكتب الـ Key هنا، هنعمله بطريقة أحسن)
# temporarily, you can set it here for testing:
# os.environ["GOOGLE_API_KEY"] = "YOUR_API_KEY_HERE"
# (الحل الأحسن هنشوفه في الخطوة 3)
# ---

print("--- vector.py: Script Started ---")

# (استخدمنا الموديل بتاع جوجل)
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

db_location = "./chrome_langchain_db_google" # (غيرنا الاسم)
add_documents = not os.path.exists(db_location)

print(f"--- vector.py: Database exists? {not add_documents} ---")

vector_store = Chroma(
    collection_name="sap_signavio_docs_google", # (غيرنا الاسم)
    persist_directory=db_location,
    embedding_function=embeddings
)

if add_documents:
    # ... (نفس كود الـ if add_documents بتاعك بالظبط، مفيش تغيير) ...
    print("--- vector.py: No DB found. Building from scratch... ---")
    loader = DirectoryLoader('.', glob="**/*.md") 
    documents = loader.load()
    print(f"--- vector.py: Loaded {len(documents)} documents. ---")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs_chunks = text_splitter.split_documents(documents)
    print(f"--- vector.py: Split into {len(docs_chunks)} chunks. ---")
    print("--- vector.py: Adding chunks to ChromaDB (This is the slow part)... ---")
    vector_store.add_documents(documents=docs_chunks)
    print("--- vector.py: Vector store built successfully. ---")


retriever = vector_store.as_retriever(
    search_kwargs={"k": 3}
)

print("--- vector.py: Retriever is ready. Script Finished. ---")