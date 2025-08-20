import sqlite3
import re

import re

def clean_label(text: str) -> str:
    if not text:
        return ""

    # 1. Buang tag HTML dulu
    text = re.sub(r"<[^>]+>", "", text)

    # 2. Baru buang awalan list: 1. / 1.2. / 5) / a.
    text = re.sub(r"^(?:[a-zA-Z]|\d+)(?:\.\d+)*[\.\)]\s*", "", text)

    # 3. Rapikan spasi
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def clean_wilayah(text: str) -> str:
    if not text:
        return ""

    text = text.lower().strip()
    text = text.replace("kab.", "kabupaten ")
    text = re.sub(r"\bkab\b", "kabupaten ", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()

# === CONNECT KE DB ===
conn = sqlite3.connect("bps_data.db")  # ubah jika nama db kamu beda
cur = conn.cursor()

# === CLEANING FIELDS ===
fields = [
    ("statistik_data", "vervar_label", clean_wilayah),
    ("statistik_data", "turvar_label", clean_label),
    ("statistik_data", "turtahun_label", clean_label),
    ("variabel_metadata", "unit", clean_label),
    ("variabel_metadata", "note", clean_label),
    ("variabel_metadata", "definisi", clean_label),
]

updated = 0

for table, column, cleaner in fields:
    try:
        cur.execute(f"SELECT id, {column} FROM {table}")
        for row_id, old in cur.fetchall():
            new = cleaner(old)
            if new != old:
                cur.execute(f"UPDATE {table} SET {column} = ? WHERE id = ?", (new, row_id))
                updated += 1
    except:
        continue

conn.commit()
conn.close()
print(f"✅ Data cleaned: {updated} baris diperbarui.")
