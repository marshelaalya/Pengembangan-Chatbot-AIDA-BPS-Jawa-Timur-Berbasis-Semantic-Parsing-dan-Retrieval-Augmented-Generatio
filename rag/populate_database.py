import argparse
import os
import shutil
import pdfplumber

from langchain.schema.document import Document
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from get_embedding_function import get_embedding_function
from langchain_community.vectorstores import Chroma

CHROMA_PATH = "/data/chroma"
DATA_PATH = "/data/pdf"

def main():

    # Cek apakah database perlu diclear
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true", help="Reset the database.")
    args = parser.parse_args()
    if args.reset:
        print("✨ Clearing Database")
        clear_database()

    # Create (atau update) Data Store.
    documents = load_documents()
    chunks = split_documents(documents)
    add_to_chroma(chunks)

import os
import pdfplumber
from langchain.schema.document import Document

def load_documents():
    docs = []
    for file in os.listdir(DATA_PATH):
        if file.endswith(".pdf"):
            with pdfplumber.open(os.path.join(DATA_PATH, file)) as pdf:
                docs += [
                    Document(page_content=page.extract_text(layout=True), metadata={"source": file, "page": i + 1})
                    for i, page in enumerate(pdf.pages) if page.extract_text(layout=True)
                ]
    return docs

def split_documents(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=80,
        length_function=len,
        is_separator_regex=False,
    )
    return text_splitter.split_documents(documents)

def add_to_chroma(chunks: list[Document]):
    db = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=get_embedding_function()
    )

    chunks_with_ids = calculate_chunk_ids(chunks)

    existing_items = db.get(include=[])
    existing_ids = set(existing_items["ids"])
    print(f"Number of existing documents in DB: {len(existing_ids)}")

    new_chunks = []
    for chunk in chunks_with_ids:
        if chunk.metadata["id"] not in existing_ids:
            new_chunks.append(chunk)

    if len(new_chunks):
        print(f"👉 Adding new documents: {len(new_chunks)}")
        new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]

        BATCH_SIZE = 5000
        for i in range(0, len(new_chunks), BATCH_SIZE):
            batch_chunks = new_chunks[i:i+BATCH_SIZE]
            batch_ids = new_chunk_ids[i:i+BATCH_SIZE]
            print(f"📦 Adding batch {i} to {i+len(batch_chunks)}")
            db.add_documents(batch_chunks, ids=batch_ids)

        db.persist()
    else:
        print("✅ No new documents to add")

def calculate_chunk_ids(chunks):
    last_page_id = None
    current_chunk_index = 0

    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        current_page_id = f"{source}:{page}"

        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0

        chunk_id = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id

        chunk.metadata["id"] = chunk_id

    return chunks

def clear_database():
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)


if __name__ == "__main__":
    main()
