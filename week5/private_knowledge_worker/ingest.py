import os
import glob
from pathlib import Path
from dotenv import load_dotenv

from langchain_community.document_loaders import (
    DirectoryLoader,
    TextLoader,
    PyPDFLoader,
    Docx2txtLoader,
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_openai import OpenAIEmbeddings  # paid alternative (not used here)

load_dotenv(override=True)
KNOWLEDGE_BASE = "../knowledge-base"
DB_NAME = "../vector_db"

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
# embeddings = OpenAIEmbeddings(model="text-embedding-3-large")  # paid alternative


def load_pdfs(folder: str) -> list:
    """Load all .pdf files inside a folder."""
    loader = DirectoryLoader(folder, glob="**/*.pdf", loader_cls=PyPDFLoader)
    return loader.load()


def load_text_and_markdown(folder: str) -> list:
    """Load all .txt and .md files inside a folder."""
    txt_loader = DirectoryLoader(
        folder, glob="**/*.txt", loader_cls=TextLoader, loader_kwargs={"encoding": "utf-8"}
    )
    md_loader = DirectoryLoader(
        folder, glob="**/*.md", loader_cls=TextLoader, loader_kwargs={"encoding": "utf-8"}
    )
    return txt_loader.load() + md_loader.load()


def load_word_documents(folder: str) -> list:
    """Load all .docx (Word) files inside a folder."""
    loader = DirectoryLoader(folder, glob="**/*.docx", loader_cls=Docx2txtLoader)
    return loader.load()


def fetch_documents() -> list:
    """
    Load PDF, TXT, MD, and DOCX files from every subfolder inside
    knowledge_base, tagging each Document with a doc_type metadata field.
    """
    documents = []
    subfolders = glob.glob(str(Path(KNOWLEDGE_BASE) / "*"))

    for folder in subfolders:
        if not os.path.isdir(folder):
            continue
        doc_type = os.path.basename(folder)

        folder_docs = []
        folder_docs.extend(load_pdfs(folder))
        folder_docs.extend(load_text_and_markdown(folder))
        folder_docs.extend(load_word_documents(folder))

        for doc in folder_docs:
            doc.metadata["doc_type"] = doc_type
            documents.append(doc)

    return documents


def create_chunks(documents: list) -> list:
    """Split large documents into smaller, overlapping chunks."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP
    )
    chunks = text_splitter.split_documents(documents)
    return chunks


def create_vector_store(chunks: list):
    """Embed the chunks and persist them into a Chroma vector DB."""
    if os.path.exists(DB_NAME):
        Chroma(persist_directory=DB_NAME, embedding_function=embeddings).delete_collection()

    vectorstore = Chroma.from_documents(
        documents=chunks, embedding=embeddings, persist_directory=DB_NAME
    )

    count = vectorstore._collection.count()
    print(f"Vector store created with {count:,} chunks at '{DB_NAME}/'")
    return vectorstore


if __name__ == "__main__":
    print("Loading documents from knowledge_base...")
    documents = fetch_documents()
    print(f"Loaded {len(documents)} documents")

    print("Splitting into chunks...")
    chunks = create_chunks(documents)
    print(f"Created {len(chunks)} chunks")

    print("Creating embeddings and vector store...")
    create_vector_store(chunks)

    print("Ingestion complete!")