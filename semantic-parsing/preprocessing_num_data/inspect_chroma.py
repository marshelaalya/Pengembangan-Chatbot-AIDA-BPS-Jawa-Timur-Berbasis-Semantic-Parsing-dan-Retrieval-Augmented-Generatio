import json
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

CHROMA_DIR = "chatbot_core/vector_store"

from dotenv import load_dotenv
load_dotenv()

def tampilkan_dokumen(var_id_target):
    vectordb = Chroma(persist_directory=CHROMA_DIR, embedding_function=OpenAIEmbeddings())
    data = vectordb.get(include=["documents", "metadatas"])

    for doc, meta in zip(data["documents"], data["metadatas"]):
        if str(meta.get("var_id")) == str(var_id_target):
            print("\n📌 Ringkasan:")
            print(doc)
            print("\n📎 Metadata:")
            for k, v in meta.items():
                try:
                    parsed = json.loads(v) if isinstance(v, str) and v.startswith("[") else v
                except:
                    parsed = v
                print(f"- {k}: {parsed}")
            return

    print(f"❌ var_id {var_id_target} tidak ditemukan di vector store.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("🔧 Cara pakai: python inspect_chroma.py <var_id>")
    else:
        tampilkan_dokumen(sys.argv[1])
