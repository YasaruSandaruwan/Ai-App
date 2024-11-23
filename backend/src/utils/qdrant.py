from langchain_qdrant import QdrantVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader  
from qdrant_client import QdrantClient, models
from decouple import config
import os

import logging
logging.basicConfig(level=logging.DEBUG)


qdrant_api_key = config("QDRANT_API_KEY")
qdrant_url = config("QDRANT_URL")
google_api_key = config("GOOGLE_API_KEY")
collection_name = "Websites"

if not qdrant_api_key or not qdrant_url or not google_api_key:
    raise ValueError("Missing required environment variables: QDRANT_API_KEY, QDRANT_URL, GOOGLE_API_KEY")

client = QdrantClient(
    url=qdrant_url,
    api_key=qdrant_api_key
)


client.create_collection(
    collection_name="Websites",
    vectors_config={
        "size": 4,
        "distance": "Cosine"
    }
)

vector_store = QdrantVectorStore(
    client=client,
    collection_name="Websites",
    embedding=embedding
)
embedding = GoogleGenerativeAIEmbeddings(
    api_key=google_api_key,
    model="google/gemini-1.5-flash"  
)

vector_store = QdrantVectorStore(
    client=client,
    collection_name=collection_name,
    embedding=embedding
    #  embedding_fn=embedding  
)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=20,
    length_function=len
)

def create_collection(collection_name):
    try:
        collections = client.get_collections()
        print(f"Existing collections: {collections}")
        if isinstance(collections, tuple):  
            collections = collections[0]              
        existing_collections = [col[0] for col in collections]  
        if collection_name in existing_collections:
            print(f"Collection {collection_name} already exists.")
        else:
            client.create_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE),
            )
            print(f"Collection {collection_name} created successfully")
    except Exception as e:
        print(f"Error creating collection {collection_name}: {e}")

def upload_website_to_collection(url: str):
    try:
        loader = WebBaseLoader(url)
        docs = loader.load_and_split(text_splitter)
        print(f"Loaded {len(docs)} documents from {url}")
        
        for doc in docs:
            doc.metadata = {"source_url": url}

        vector_store.add_documents(docs)
        print(f"Successfully uploaded {len(docs)} documents to collection {collection_name}")
    except Exception as e:
        print(f"Error uploading website to collection {collection_name}: {e}")

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("BeautifulSoup (bs4) not found. Installing...")
    os.system("pip install beautifulsoup4")

create_collection(collection_name)
upload_website_to_collection("https://www.pewresearch.org/internet/2018/12/10/artificial-intelligence-and-the-future-of-humans/")
