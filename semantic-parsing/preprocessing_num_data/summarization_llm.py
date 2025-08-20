import sqlite3
import json
from tqdm import tqdm
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.schema import Document
import os
from dotenv import load_dotenv

load_dotenv()

DB_PATH = "bps_data.db"
CHROMA_DIR = os.path.join("chatbot_core", "vector_store")

llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
embedder = OpenAIEmbeddings()
vectordb = Chroma(persist_directory=CHROMA_DIR, embedding_function=embedder)

def get_all_var_ids(conn):
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT var_id FROM statistik_data")
    return [row[0] for row in cur.fetchall()]

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

def get_var_label(conn, var_id):
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT var_label FROM statistik_data WHERE var_id = ? LIMIT 1", (var_id,))
    row = cur.fetchone()
    return row[0] if row else f"Indikator {var_id}"

def build_few_shot_prompt(labelvervar, vervar, turvar, tahun, turtahun_label):
    contoh = """
Contoh:
- labelvervar: ['Lapangan Usaha 17 Sektor']
- turvar: ['laki-laki', 'perempuan']
- tahun: ['2022', '2023']
- turtahun_label: ['Januari', 'Februari','Maret','April']
→ Ringkasan: Indikator ini dibedakan berdasarkan lapangan usaha 17 sektor, jenis kelamin, tahun 2022-2023, bulan Januari-Desember.

Contoh:
- labelvervar: ['jenis kelamin dan kelompok umur']
- turvar: []
- tahun: ['2021', '2022', ['2023'], ['2024']]
- turtahun_label: []
→ Ringkasan: Indikator ini dibedakan berdasarkan jenis kelamin dan kelompok umur dan tahun 2021-2024.

Contoh:
- labelvervar: ['klasifikasi hotel']
- turvar: []
- tahun: ['2021', '2022']
- turtahun_label: ['triwulan I', 'Triwulan II', 'Triwulan III', 'Triwulan IV']
→ Ringkasan: Indikator ini dibedakan berdasarkan klasifikasi hotel, tahun 2021-2022 dan triwulan I-IV.
"""
    current = f"""
Berikut struktur indikator:
- labelvervar: {labelvervar if labelvervar else '-'}
- vervar: {vervar if vervar else '-'}
- turvar: {turvar if turvar else '-'}
- tahun: {tahun if tahun else '-'}
- turtahun_label: {turtahun_label if turtahun_label else '-'}
→ Ringkasan:
"""
    return contoh + "\n" + current

def generate_summary(labelvervar, vervar, turvar, tahun, turtahun_label):
    prompt = build_few_shot_prompt(labelvervar, vervar, turvar, tahun, turtahun_label)
    response = llm.invoke(prompt)
    return response.content.strip()

def main():
    conn = sqlite3.connect(DB_PATH)
    var_ids = get_all_var_ids(conn)

    for var_id in tqdm(var_ids, desc="Generating summaries"):
        var_label = get_var_label(conn, var_id)
        labelvervar, vervar, turvar, tahun, turtahun_label = get_disagg_info(conn, var_id)

        try:
            summary = generate_summary(labelvervar, vervar, turvar, tahun, turtahun_label)
        except Exception as e:
            print(f"[SKIP] {var_id}: Error during GPT call → {e}")
            continue

        doc = Document(
            page_content=summary,
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

        vectordb.add_documents([doc])

    vectordb.persist()
    print("✅ Semua ringkasan berhasil disimpan ke Chroma")

if __name__ == "__main__":
    main()
