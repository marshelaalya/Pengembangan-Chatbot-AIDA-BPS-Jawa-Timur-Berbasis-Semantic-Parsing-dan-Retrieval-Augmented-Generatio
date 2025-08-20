from typing import Dict, List, Tuple, Optional
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
# from langchain_chroma import Chroma
# from langchain.vectorstores import Chroma
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import json
import re

from dotenv import load_dotenv
load_dotenv()

CHROMA_DIR = "/data/vector_store"
DB_PATH = "/data/bps_data.db"  

embedder = OpenAIEmbeddings()

llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
import sqlite3



# ==== Prompt GPT dengan intent definitions + few-shot ====
prompt = PromptTemplate.from_template("""
Kamu adalah asisten statistik BPS.

Tugasmu adalah mengekstrak struktur pertanyaan pengguna ke dalam format JSON seperti:
{{
  "topik": [...],  
  "tahun": [...],
  "disagg_terms": [...],
  "wilayah": "..."
}}

Penjelasan:
- "topik": kata kunci utama yang menunjukkan jenis indikator statistik
- "tahun": tahun yang disebut
- "disagg_terms": kategori pembeda seperti jenis kelamin, komoditas, kelompok pengeluaran (bukan wilayah)
- "wilayah": HANYA nama kabupaten/kota di Jawa Timur (misal: kota surabaya, kota kediri, banyuwangi). jangan hilangkan konteks kabupaten atau kotanya. karena ada perbedaan antara kota dan kabupaten

Aturan :
1. tidak usah anggap kata kata yang bermakna intent seperti jumlah, max, min. karena tugas kita nantinya hanya akan menyediakan data.
2. Jangan menghilongkan informasi penting
                                      
                                      
Contoh:

Pertanyaan: "Berapa jumlah pengangguran tahun 2023?"
Output:
{{"topik": ["pengangguran"], "tahun": [2023], "disagg_terms": [], "wilayah": ""}}

Pertanyaan: "Berapa konsumsi beras di Surabaya tahun 2022?"
Output:
{{"topik": ["konsumsi"], "tahun": [2022], "disagg_terms": ["beras"], "wilayah": "surabaya"}}

Pertanyaan: "Bagaimana inflasi transportasi di Kediri?"
Output:
{{"topik": ["inflasi"], "tahun": [], "disagg_terms": ["transportasi"], "wilayah": "kediri"}}

---

Pertanyaan pengguna:
"{pertanyaan}"

Berikan hanya output JSON tanpa penjelasan atau format markdown.
""")

SQL_GENERATION_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """Anda adalah seorang ahli SQL yang bekerja dengan tabel bernama 'statistik_data' dengan struktur sebagai berikut:
    
Tabel: statistik_data  
Kolom:  
- var_id: ID Variabel  
- vervar_label: Label variabel vertikal  
- turvar_label: Label variabel turunan  
- tahun_label: Label tahun  
- nilai: Nilai numerik  

Tugas Anda adalah membuat query SELECT berdasarkan pertanyaan pengguna dan informasi hasil parsing.

ATURAN PENTING:  
1. Selalu gunakan SELECT * untuk mengambil semua kolom, bukan hanya kolom tertentu  
2. Bersikaplah FLEKSIBEL dalam mencocokkan istilah dengan metadata  
3. Gunakan huruf kecil untuk perbandingan: LOWER(kolom) = 'nilai'  
4. Lihat metadata untuk menentukan kolom mana yang digunakan  
5. Jika suatu istilah secara masuk akal dapat cocok dengan sesuatu di metadata, GUNAKAN ITU  
6. Hanya kembalikan "NO_MATCH" jika benar-benar tidak ada yang bisa dicocokkan"""),
    
    ("human", """Pertanyaan: {question}

ID Variabel yang dipilih: {var_id}

Keinginan pengguna: {parsed_info}

Nilai yang tersedia di database:  
- Nilai vervar_label: {vervar_values}  
- Nilai turvar_label: {turvar_values}  

Tugas Anda: Buat query SQL yang HARUS menyertakan WHERE var_id = '{var_id}' dan memetakan istilah pengguna ke nilai metadata yang paling cocok di database.

Hasilkan query SQL. Hanya kembalikan query SQL tersebut.""")
])

# Few-shot Prompting
EXAMPLES = [
    {
        "question": "data laki laki",
        "var_id": "123",
        "parsed_info": "disagg_terms: ['laki laki']",
        "vervar_values": "['i/a', 'i/b']",
        "turvar_values": "['laki-laki', 'perempuan']",
        "query": "SELECT * FROM statistik_data WHERE var_id = '123' AND LOWER(turvar_label) = 'laki-laki' LIMIT 100"
    },
    {
        "question": "pns golongan 2",
        "var_id": "456",
        "parsed_info": "disagg_terms: ['golongan 2']",
        "vervar_values": "['golongan i', 'golongan ii', 'golongan iii']",
        "turvar_values": "['laki-laki', 'perempuan']",
        "query": "SELECT * FROM statistik_data WHERE var_id = '456' AND LOWER(vervar_label) = 'golongan ii' LIMIT 100"
    },
    {
        "question": "data golongan 3 perempuan",
        "var_id": "789",
        "parsed_info": "disagg_terms: ['golongan 3', 'perempuan']",
        "vervar_values": "['golongan i', 'golongan ii', 'golongan iii']",
        "turvar_values": "['laki-laki', 'perempuan']",
        "query": "SELECT * FROM statistik_data WHERE var_id = '789' AND LOWER(vervar_label) = 'golongan iii' AND LOWER(turvar_label) = 'perempuan' LIMIT 100"
    }
]

# ==== Fungsi utama: parse + tokenisasi + filter ====
def parse_question_semantic_gpt(pertanyaan: str, disagg_label_list: list[str] = []) -> dict:
    # 1. Tokenisasi ringan
    tokens = [t.lower() for t in re.findall(r'\b\w+\b', pertanyaan) if len(t) > 2 and not t.isdigit()]

    # 2. Parsing ke GPT
    formatted = prompt.format(pertanyaan=pertanyaan)
    response = llm.invoke(formatted)

    try:
        parsed = json.loads(response.content.strip())
    except Exception as e:
        parsed = {}

    # 3. Normalisasi hasil
    topik = parsed.get("topik", [])
    tahun = parsed.get("tahun", [])
    disagg_terms = parsed.get("disagg_terms", [])
    wilayah = parsed.get("wilayah", "")

    # 4. Tambahkan disagg_terms yang cocok dari metadata
    if disagg_label_list:
        label_lower = [d.lower() for d in disagg_label_list]
        for token in tokens:
            match = next((dl for dl in disagg_label_list if token in dl.lower()), None)
            if match and match not in disagg_terms:
                disagg_terms.append(match)

    return {
        "topik": topik,
        "tahun": tahun,
        "disagg_terms": disagg_terms,
        "wilayah": wilayah
    }

def parse_metadata_lists(meta: dict) -> dict:
    for key in ["tahun", "vervar", "turvar"]:
        if isinstance(meta.get(key), str) and meta[key].startswith("["):
            try:
                meta[key] = json.loads(meta[key])
            except:
                meta[key] = []
    return meta


def cari_var_id_dari_pertanyaan(pertanyaan: str):
    # Step 1: Semantic parsing
    parsed = parse_question_semantic_gpt(pertanyaan)

    # Step 2: Buat query vektor dari topik + disagg_terms
    query = " ".join(parsed.get("topik", []) + parsed.get("disagg_terms", []))

    # Step 3: Search ke vector DB
    vectordb = Chroma(persist_directory=CHROMA_DIR, embedding_function=embedder)
    hasil = vectordb.similarity_search_with_score(query, k=10)  # Ambil top 3

    # print("=== HASIL SIMILARITY SEARCH ===")
    # for i, (doc, score) in enumerate(hasil):
    #     print(f"[{i}] Score: {score:.4f}")
    #     print(f"    Label: {doc.metadata.get('var_label')}")
    #     print(f"    Content: {doc.page_content[:1000]}...\n")

    if not hasil:
        return None, parsed, None, {}

    scoring_prompt = PromptTemplate.from_template("""
Kamu adalah sistem scoring untuk menilai relevansi dokumen statistik BPS.

Pertanyaan user: "{pertanyaan}"
Parsed: {parsed}

Berikut adalah dokumen-dokumen kandidat:
{candidates}

ATURAN SCORING KETAT:
1. Berikan skor 0-10 berdasarkan RELEVANSI TOPIK, bukan kesamaan kata
2. Skor 8-10: Hanya untuk dokumen yang BENAR-BENAR menjawab pertanyaan
3. Skor 5-7: Dokumen yang ada hubungan tapi tidak langsung
4. Skor 0-4: Dokumen yang TIDAK RELEVAN dengan pertanyaan

PENTING:
- "jadwal pertandingan sepak bola" TIDAK RELEVAN dengan data statistik padi, penduduk, ekonomi, dll
- "resep masakan" TIDAK RELEVAN dengan data inflasi, pengangguran, dll
- Jika pertanyaan di luar konteks statistik BPS, SEMUA dokumen harus mendapat skor rendah (<5)

Pertanyaan user adalah tentang: {pertanyaan}
Apakah ini pertanyaan statistik BPS? Jika tidak, semua dokumen harus skor <5.

Output dalam format JSON:
{{
    "selected_index": <index dokumen terpilih atau -1 jika tidak ada yang relevan>,
    "scores": [<skor doc 0>, <skor doc 1>, ...],
    "reason": "<alasan singkat>",
    "is_relevant_query": <true/false - apakah pertanyaan relevan dengan data BPS>
}}
""")

    # Format kandidat untuk prompt
    candidates_text = []
    for i, (doc, score) in enumerate(hasil):
        meta = parse_metadata_lists(doc.metadata)
        candidates_text.append(f"""
Dokumen {i}:
- Label: {doc.metadata.get('var_label')}
- Konten: {doc.page_content[:300]}...
- Tahun tersedia: {', '.join(meta.get('tahun', [])[:10])}
""")
    
    # Minta GPT untuk scoring
    prompt = scoring_prompt.format(
        pertanyaan=pertanyaan,
        parsed=json.dumps(parsed, indent=2),
        candidates="\n".join(candidates_text)
    )
    
    try:
        response = llm.invoke(prompt)
        scoring_result = json.loads(response.content.strip())
        # Di dalam scoring result
        if scoring_result.get('scores'):
            max_score = max(scoring_result.get('scores', [0]))
            if max_score < 5:  # Threshold relevansi
                return None, parsed, None, {}
            
        selected_idx = scoring_result.get("selected_index", 0)
        
        # print(f"[GPT SCORING] Scores: {scoring_result.get('scores', [])}")
        # print(f"[GPT SCORING] Selected: Doc {selected_idx} - {scoring_result.get('reason', '')}")
        
        # Validasi index
        if 0 <= selected_idx < len(hasil):
            selected_doc = hasil[selected_idx]
        else:
            selected_doc = hasil[0]  # Fallback
            
    except Exception as e:
        # print(f"[ERROR] GPT Scoring failed: {e}")
        # Fallback ke similarity score tertinggi
        selected_doc = hasil[0]

    # Step 5: Ambil metadata
    doc, score = selected_doc
    meta = parse_metadata_lists(doc.metadata)

    meta["var_id"] = meta.get("var_id")
    meta["var_label"] = meta.get("var_label", "")
    meta["vervar"] = meta.get("vervar", [])
    meta["turvar"] = meta.get("turvar", [])
    meta["tahun"] = [str(t) for t in meta.get("tahun", [])]

    var_id = meta["var_id"]
    var_label = meta["var_label"]

    # print(f"\n[SELECTED] var_id: {var_id}")
    # print(f"[SELECTED] var_label: {var_label}")
    # print(f"[META] vervar: {meta['vervar'][:5]}..." if len(meta['vervar']) > 5 else f"[META] vervar: {meta['vervar']}")
    # print(f"[META] turvar: {meta['turvar']}")
    # print(f"[META] tahun: {meta['tahun']}")

    return var_id, parsed, var_label, meta

def generate_sql_query(
    question: str,
    parsed: dict,
    metadata: dict,
    var_id: str, 
    use_few_shot: bool = True,
    debug: bool = False
) -> Tuple[Optional[str], List[str]]:
    """
    Membuat SQL dengan Smart-Term-Matching
    """
    warnings = []
    
    # if debug:
    #     print(f"\n🔍 Parsed terms: {parsed.get('disagg_terms', [])}")
    #     print(f"📊 Var ID: {var_id}")
    
    # Format inputs
    vervar_values = str(metadata.get("vervar", []))
    turvar_values = str(metadata.get("turvar", []))
    
    try:
        # Membuat SQL dengan LLM, agar mencocokan dengan metadata
        prompt = SQL_GENERATION_PROMPT.format_messages(
            question=question,
            var_id=var_id, 
            parsed_info=str(parsed.get("disagg_terms", [])), 
            vervar_values=vervar_values,
            turvar_values=turvar_values
        )
        
        response = llm.invoke(prompt)
        sql = response.content.strip()
        
        # Clean up SQL
        sql = sql.replace("```sql", "").replace("```", "").strip()
        if sql.lower().startswith("sql:"):
            sql = sql[4:].strip()
        
        # Jika SQL yang dihasilkan tidak ada data
        if sql.upper() == "NO_MATCH":
            return None, ["Data yang diminta tidak tersedia dalam variabel ini"]
        
        # if debug:
        #     print(f"\nGenerated SQL: {sql}")
        
        return sql, warnings
        
    except Exception as e:
        # if debug:
        #     print(f"\n LLM Error: {str(e)}")
        
        # Fallback to simple SQL generation with just var_id
        sql = f"SELECT * FROM statistik_data WHERE var_id = '{var_id}' LIMIT 100"
        warnings.append(f"Error occurred: {str(e)}, using simple query")
        return sql, warnings

def run_sql_query(sql: str, db_path: str = DB_PATH) -> list[dict]:
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        conn.close()

        return [dict(row) for row in rows]
    except Exception as e:
        # print(f"Gagal eksekusi SQL: {e}")
        return []


def format_answer(var_ids: list[int], all_data: list[list[dict]], var_labels: dict, parsed: dict, metadata: dict = None) -> str:
    if not var_ids or not all_data or not any(all_data):
        return "Maaf, data yang Anda minta tidak tersedia."

    topk = len(var_ids)
    jawaban = ["Halo, ini yang saya temukan.\n"]

    for i, var_id in enumerate(var_ids):
        data = all_data[i]
        label = var_labels.get(var_id, f"Indikator {var_id}")
        jawaban.append(f"📌 Judul Data:\n{label}\n")

        if not data:
            # Analisis kenapa data tidak ditemukan
            jawaban.append("❌ Data tidak ditemukan.\n")
            jawaban.append("📋 Kriteria yang diminta:")
            
            # Detail kriteria
            if parsed.get("tahun"):
                jawaban.append(f"   • Tahun: {', '.join(map(str, parsed['tahun']))}")
            if parsed.get("disagg_terms"):
                jawaban.append(f"   • Kategori: {', '.join(parsed['disagg_terms'])}")
            if parsed.get("wilayah"):
                jawaban.append(f"   • Wilayah: {parsed['wilayah']}")
            
            # Rekomendasi berdasarkan metadata
            if metadata:
                jawaban.append("\n💡 Data yang tersedia untuk indikator ini:")
                
                # Tahun
                if metadata.get("tahun"):
                    tahun_list = metadata["tahun"][:10]  # Max 10
                    jawaban.append(f"   • Tahun: {', '.join(tahun_list)}")
                    if len(metadata["tahun"]) > 10:
                        jawaban.append(f"     (dan {len(metadata['tahun']) - 10} tahun lainnya)")
                
                # Kategori vervar
                if metadata.get("vervar") and metadata["vervar"] != ["Tidak ada"]:
                    vervar_list = metadata["vervar"][:8]  # Max 8
                    jawaban.append(f"   • Kategori vertikal: {', '.join(vervar_list)}")
                    if len(metadata["vervar"]) > 8:
                        jawaban.append(f"     (dan {len(metadata['vervar']) - 8} kategori lainnya)")
                
                # Kategori turvar - UPDATED: skip if "Tidak ada"
                if metadata.get("turvar"):
                    # Filter out "Tidak ada" values
                    turvar_filtered = [t for t in metadata["turvar"] if t.lower() != "tidak ada"]
                    if turvar_filtered:  
                        turvar_list = turvar_filtered[:8]
                        jawaban.append(f"   • Kategori horizontal: {', '.join(turvar_list)}")
                        if len(turvar_filtered) > 8:
                            jawaban.append(f"     (dan {len(turvar_filtered) - 8} kategori lainnya)")
                
                jawaban.append("\n📝 Saran: Gunakan kriteria yang sesuai dengan data yang tersedia di atas.")
            
            jawaban.append("")
            continue

        # [kode untuk menampilkan data - sama seperti sebelumnya]
        baris = []
        for row in data[:5]:
            tahun = row.get("tahun_label", "-")
            vervar = row.get("vervar_label", "-")
            turvar = row.get("turvar_label", "-")
            nilai = row.get("nilai", "-")
            
            # UPDATED: Format display based on turvar value
            if turvar.lower() == "tidak ada" or turvar == "-":
                # Skip turvar jika isinya "Tidak ada"
                baris.append(f"- Tahun: {tahun}, Kategori: {vervar}, Nilai: {nilai}")
            else:
                # Masukkan Turvar jika ada isinya
                baris.append(f"- Tahun: {tahun}, Kategori: {vervar} / {turvar}, Nilai: {nilai}")

        jawaban.append("📊 Isi Data:\n" + "\n".join(baris) + "\n")

    return "\n".join(jawaban)

def chatbot_jawab(pertanyaan: str) -> str:
    # Step 1: parsing + pencocokan + validasi metadata
    var_id, parsed, var_label, metadata = cari_var_id_dari_pertanyaan(pertanyaan)
    
    if not var_id:
        # Buat pesan error yang lebih informatif
        pesan_error = ["Maaf, saya tidak menemukan data yang sesuai dengan kriteria Anda."]
        
        pesan_error.append("\n💡 Saran: Coba gunakan kata kunci yang lebih umum atau periksa penulisan wilayah/kategori.")
        
        return "\n".join(pesan_error)

    sql, alasan_gagal = generate_sql_query(pertanyaan, parsed, metadata, var_id, debug=True)
    
    # Jika SQL generation gagal
    if sql is None:
        jawaban = [f"📌 Judul Data:\n{var_label}\n"]
        jawaban.append("❌ Tidak dapat memproses permintaan Anda karena:")
        for alasan in alasan_gagal:
            jawaban.append(f"   • {alasan}")
        
        # Tampilkan kategori yang tersedia
        if metadata.get("vervar") or metadata.get("turvar"):
            jawaban.append("\n📋 Kategori yang tersedia:")
            if metadata.get("vervar"):
                jawaban.append(f"   • Vertikal: {', '.join(metadata['vervar'][:5])}...")
            if metadata.get("turvar"):
                jawaban.append(f"   • Horizontal: {', '.join(metadata['turvar'])}")
        
        return "\n".join(jawaban)

    # Step 3: Menjalankan Query SQL untuk mengambil data
    hasil = run_sql_query(sql)
    
    # Step 4: Membuat jawaban
    return format_answer([var_id], [hasil], {var_id: var_label}, parsed, metadata)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        try:
            result = chatbot_jawab(query)
            print(result)
            sys.exit(0)  
        except Exception as e:
            print(f"Error: {str(e)}")
            sys.exit(1) 
    else:
        # untuk CLI mode
        print("Chatbot Statistik BPS!\n(Ketik kosong untuk keluar.)")
        while True:
            try:
                pertanyaan = input("\n❓ Pertanyaan Anda: ").strip()
                if not pertanyaan:
                    break
                print("\nJawaban:\n")
                print(chatbot_jawab(pertanyaan))
            except KeyboardInterrupt:
                print("\nBye!")
                break
            except Exception as e:
                print(f"Error: {str(e)}")
                continue