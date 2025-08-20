import argparse
from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from get_embedding_function import get_embedding_function
import os
from datetime import datetime

# Perbaiki masalah path
CHROMA_PATH = "/data/chroma"

# Pastikan direktori ada
if not os.path.exists(CHROMA_PATH):
    os.makedirs(CHROMA_PATH, exist_ok=True)

# Template prompt yang lebih engaging dengan personality Ning Aida
PROMPT_TEMPLATE = """
Kamu adalah Ning Aida, AI Data Assistant BPS Provinsi Jawa Timur yang ramah, informatif, dan profesional.

Berdasarkan konteks dokumen BPS di bawah ini, jawablah pertanyaan pengguna dengan gaya yang hangat namun tetap kredibel.

Konteks Dokumen BPS:
{context}

---

Pertanyaan Pengguna: {question}

Panduan menjawab:
1. Berikan jawaban yang komprehensif berdasarkan konteks yang tersedia
2. Jika ada istilah teknis, jelaskan dengan bahasa yang mudah dipahami
3. Gunakan emoji yang sesuai untuk membuat respons lebih engaging (📊📈💡🔍📚)
4. Jika konteks tidak mencakup informasi yang diminta, jelaskan dengan sopan dan berikan alternatif
5. Akhiri dengan tawaran bantuan lebih lanjut

Format jawaban dengan struktur yang jelas menggunakan heading dan bullet points jika diperlukan.

Jawaban:
"""

def get_greeting():
    """Buat sapaan berdasarkan waktu"""
    hour = datetime.now().hour
    if 5 <= hour < 10:
        return "Selamat pagi! ☀️"
    elif 10 <= hour < 15:
        return "Selamat siang! 🌞"
    elif 15 <= hour < 18:
        return "Selamat sore! 🌅"
    else:
        return "Selamat malam! 🌙"

def format_enhanced_response(response_text, sources_dict, question):
    """Format respons dengan gaya BPS Jatim yang engaging dengan link HTML"""
    
    # Mulai dengan sapaan
    greeting = get_greeting()
    intro = f"{greeting} Saya Ning Aida, AI Data Assistant BPS Provinsi Jawa Timur. Senang bisa membantu Anda! 😊\n\n"
    
    # Respons utama - convert markdown links ke HTML
    output = intro + convert_to_html_links(response_text)
    
    # Format sumber referensi
    if sources_dict:
        output += "\n\n📚 **Referensi Dokumen BPS:**"
        for i, (filename, pages) in enumerate(sources_dict.items(), 1):
            clean_filename = filename.replace(" (1).pdf", "").replace(".pdf", "")
            unique_pages = sorted(list(set(pages)))
            
            if len(unique_pages) == 1:
                output += f"\n{i}. 📄 {clean_filename} (Halaman {unique_pages[0]})"
            else:
                pages_str = ", ".join(unique_pages[:3])
                if len(unique_pages) > 3:
                    output += f"\n{i}. 📄 {clean_filename} (Halaman {pages_str}, dan {len(unique_pages)-3} lainnya)"
                else:
                    output += f"\n{i}. 📄 {clean_filename} (Halaman {pages_str})"
    
    # Tambahkan sumber informasi tambahan dengan HTML links
    output += "\n\n🔗 **Sumber Informasi Tambahan:**"
    output += '\n• 📊 Tabel Statistik: <a href="https://jatim.bps.go.id/id/statistics-table" target="_blank">jatim.bps.go.id/statistics-table</a>'
    output += '\n• 📈 Query Builder: <a href="https://jatim.bps.go.id/id/query-builder" target="_blank">jatim.bps.go.id/query-builder</a>'
    output += '\n• 📖 Publikasi Lengkap: <a href="https://jatim.bps.go.id/id/publication" target="_blank">jatim.bps.go.id/publication</a>'
    output += '\n• 🔍 Metadata & Konsep: <a href="https://sirusa.bps.go.id/" target="_blank">sirusa.bps.go.id</a>'
    output += '\n• 👨‍💼 Konsultasi Statistisi Ahli: <a href="https://halopst.web.bps.go.id/konsultasi" target="_blank">halopst.web.bps.go.id/konsultasi</a>'
    
    # Call to action
    output += "\n\n❓ Ada pertanyaan lanjutan atau butuh data yang lebih spesifik? Saya siap membantu!"
    
    # Link survei dengan HTML
    output += '\n\n📝 *Bantu kami meningkatkan layanan dengan mengisi <a href="http://s.bps.go.id/skd3500" target="_blank">survei singkat</a>*'
    
    return output

def convert_to_html_links(text):
    """Convert URL dalam text menjadi HTML links"""
    import re
    
    # Pattern untuk mendeteksi URL
    url_pattern = r'(https?://[^\s]+)'
    
    # Replace URL dengan HTML anchor tags
    def replace_url(match):
        url = match.group(0)
        # Bersihkan URL dari karakter trailing
        url = url.rstrip('.,;:)')
        # Extract domain untuk display text yang lebih pendek
        display_text = url.replace('https://', '').replace('http://', '').split('/')[0]
        return f'<a href="{url}" target="_blank">{display_text}</a>'
    
    return re.sub(url_pattern, replace_url, text)

def format_no_context_response(question):
    """Buat respons yang helpful ketika tidak ada konteks yang relevan dengan HTML links"""
    greeting = get_greeting()
    
    # Encode query untuk URL
    import urllib.parse
    encoded_query = urllib.parse.quote(question)
    
    response = f"""{greeting} Saya Ning Aida dari BPS Provinsi Jawa Timur. 😊

Mohon maaf, saya tidak menemukan informasi spesifik tentang pertanyaan Anda dalam dokumen yang tersedia. 🤔

Namun, saya bisa membantu Anda dengan cara lain:

📊 **Coba Akses Data Melalui:**
- Tabel Statistik: <a href="https://jatim.bps.go.id/id/statistics-table" target="_blank">jatim.bps.go.id/statistics-table</a>
- Query Builder untuk data custom: <a href="https://jatim.bps.go.id/id/query-builder" target="_blank">jatim.bps.go.id/query-builder</a>
- Publikasi BPS: <a href="https://jatim.bps.go.id/id/publication" target="_blank">jatim.bps.go.id/publication</a>

🔍 **Untuk Definisi & Metadata:**
- Sistem Rujukan Statistik: <a href="https://sirusa.bps.go.id/" target="_blank">sirusa.bps.go.id</a>
- Cari '{question}' di: <a href="https://sirusa.bps.go.id/index.php/search?keywords={encoded_query}" target="_blank">SIRUSA</a>

👨‍💼 **Konsultasi Langsung:**
- Chat dengan Statistisi Ahli: <a href="https://halopst.web.bps.go.id/konsultasi" target="_blank">HaloPST Konsultasi</a>
- Layanan konsultasi: Senin-Kamis (08.00-15.30), Jumat (08.00-16.00)

💡 **Tips Pencarian:**
- Gunakan kata kunci yang lebih spesifik
- Coba variasi istilah (misal: 'IPM' atau 'Indeks Pembangunan Manusia')
- Sebutkan tahun atau wilayah jika mencari data spesifik

Ada yang bisa saya bantu dengan cara lain? Jangan ragu untuk bertanya! 😊"""
    
    return response

def main():
    # Buat CLI
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text
    query_rag(query_text)

def query_rag(query_text: str):
    # Siapkan database
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Cari di database dengan threshold relevansi
    results = db.similarity_search_with_score(query_text, k=5)
    
    # Filter hasil berdasarkan skor relevansi
    relevant_results = [(doc, score) for doc, score in results if score < 1.5]  # Sesuaikan threshold jika perlu
    
    if not relevant_results:
        # Tidak ada konteks relevan
        print(format_no_context_response(query_text))
        return "No relevant context found"
    
    # Buat konteks dari hasil yang relevan
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in relevant_results])
    
    # Gunakan template prompt yang enhanced
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    
    # Dapatkan respons dari model
    model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)  # Sedikit temperature untuk kreativitas
    response_text = model.invoke(prompt).content
    
    # Ekstrak sumber
    sources_dict = {}
    for doc, _score in relevant_results:
        source_id = doc.metadata.get("id", None)
        if source_id:
            parts = source_id.split(":")
            if len(parts) >= 2:
                filename = parts[0]
                page = parts[1]
                
                if filename not in sources_dict:
                    sources_dict[filename] = []
                sources_dict[filename].append(page)
    
    # Format dan print respons yang enhanced
    enhanced_output = format_enhanced_response(response_text, sources_dict, query_text)
    print(enhanced_output)
    
    return response_text

if __name__ == "__main__":
    main()