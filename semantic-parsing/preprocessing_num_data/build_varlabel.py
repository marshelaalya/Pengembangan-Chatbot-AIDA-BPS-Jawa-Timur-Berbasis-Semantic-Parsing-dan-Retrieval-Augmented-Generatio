import sqlite3
import json
from tqdm import tqdm
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
import os
from dotenv import load_dotenv

load_dotenv()

DB_PATH = "bps_data.db"
CHROMA_DIR = os.path.join("chatbot_core", "vector_store")

embedder = OpenAIEmbeddings()

def get_all_var_ids(conn):
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT var_id FROM statistik_data")
    return [row[0] for row in cur.fetchall()]

def get_var_label(conn, var_id):
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT var_label FROM statistik_data WHERE var_id = ? LIMIT 1", (var_id,))
    row = cur.fetchone()
    return row[0] if row else f"Indikator {var_id}"

def get_disagg_info(conn, var_id):
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT labelvervar FROM statistik_data WHERE var_id = ?", (var_id,))
    labelvervar = sorted(set([row[0] for row in cur.fetchall() if row[0]]))

    cur.execute("SELECT DISTINCT vervar_label FROM statistik_data WHERE var_id = ?", (var_id,))
    vervar = sorted(set([row[0] for row in cur.fetchall() if row[0]]))

    cur.execute("SELECT DISTINCT turvar_label FROM statistik_data WHERE var_id = ?", (var_id,))
    turvar = sorted(set([row[0] for row in cur.fetchall() if row[0]]))

    cur.execute("SELECT DISTINCT tahun_label FROM statistik_data WHERE var_id = ?", (var_id,))
    tahun = sorted(set([str(row[0]) for row in cur.fetchall() if row[0]]))

    cur.execute("SELECT DISTINCT turtahun_label FROM statistik_data WHERE var_id = ?", (var_id,))
    turtahun_label = sorted(set([row[0] for row in cur.fetchall() if row[0]]))

    return labelvervar, vervar, turvar, tahun, turtahun_label

def main():
    conn = sqlite3.connect(DB_PATH)
    var_ids = get_all_var_ids(conn)

    docs = []
    for var_id in tqdm(var_ids, desc="📦 Membuat vectorstore var_label"):
        var_label = get_var_label(conn, var_id)
        labelvervar, vervar, turvar, tahun, turtahun_label = get_disagg_info(conn, var_id)

        # 🔁 Format page_content yang lebih kaya dan semantik-friendly
        vervar_str = ", ".join(vervar) if vervar else "-"
        labelvervar_str = ", ".join(labelvervar) if labelvervar else "-"
        turvar_str = ", ".join(turvar) if turvar else "-"
        tahun_str = ", ".join(tahun) if tahun else "-"
        turtahun_label_str = ", ".join(turtahun_label) if turtahun_label else "-"

        page_content = f"""Indikator: {var_label}.
        Disaggregasi berdasarkan {labelvervar_str} seperti: {vervar_str}.
        Kategori turunan lainnya: {turvar_str}.
        Tahun tersedia: {tahun_str}.
        Label tahun: {turtahun_label_str}.
        """

        doc = Document(
            page_content=page_content.strip(),
            metadata={
                "var_id": var_id,
                "var_label": var_label,
                "labelvervar": json.dumps(labelvervar),
                "vervar": json.dumps(vervar),
                "turvar": json.dumps(turvar),
                "tahun": json.dumps(tahun),
                "turtahun_label": json.dumps(turtahun_label)
            }
        )

        docs.append(doc)

    vectordb = Chroma.from_documents(
        docs,
        embedding=embedder,
        persist_directory=CHROMA_DIR
    )
    vectordb.persist()
    print("✅ Semua var_label berhasil di-embed dan disimpan ke vectorstore baru.")

if __name__ == "__main__":
    main()
