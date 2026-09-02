from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

DB_NAME = "../vector_db"
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

vectorstore = Chroma(persist_directory=DB_NAME, embedding_function=embeddings)

# Pull every single chunk directly from the collection (no similarity search involved)
all_data = vectorstore._collection.get(include=["metadatas", "documents"])

total = len(all_data["ids"])
print(f"Total chunks in vector store: {total}")
print("=" * 60)

matches = []
for metadata, content in zip(all_data["metadatas"], all_data["documents"]):
    source = metadata.get("source", "")
    if "jamil" in source.lower() or "resume" in source.lower():
        matches.append((source, content))

print(f"Chunks whose SOURCE filename contains 'jamil' or 'resume': {len(matches)}")
print("=" * 60)

if matches:
    for source, content in matches:
        print(f"Source: {source}")
        print(f"Content preview: {content[:200]}")
        print()
else:
    print("No chunks found with a source filename matching the resume.")
    print("\nHere are ALL unique source files currently in the vector store:")
    unique_sources = sorted({m.get("source", "unknown") for m in all_data["metadatas"]})
    for s in unique_sources:
        print(f" - {s}")