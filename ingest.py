from utils.loader import load_all_pdfs
from utils.splitter import split_documents
from utils.embedding import get_embedding_model
from langchain_community.vectorstores import Chroma

print("Loading PDFs...")

documents = load_all_pdfs()

print(f"Loaded {len(documents)} pages")

print("Splitting documents...")

chunks = split_documents(documents)

print(f"Created {len(chunks)} chunks")

print("Loading embedding model...")

embedding_model = get_embedding_model()

print("Creating ChromaDB vector store...")

vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embedding_model,
    persist_directory="chroma_db"
)

vectorstore.persist()

print("Embeddings stored successfully!")