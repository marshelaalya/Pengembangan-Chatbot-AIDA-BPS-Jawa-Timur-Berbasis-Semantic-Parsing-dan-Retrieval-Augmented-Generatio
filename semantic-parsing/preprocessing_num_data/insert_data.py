import os
import json
import sqlite3
from tqdm import tqdm
from itertools import product

# === KONFIGURASI ===
DB_PATH = "bps_data.db"
DATA_FOLDER = "data_json"
LIMIT_DOMAIN = "3500"

# === KONEKSI DB ===
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

sukses, gagal = 0, 0

# === LOOP FILE JSON ===
files = sorted(f for f in os.listdir(DATA_FOLDER) if f.endswith(".json"))
for filename in tqdm(files, desc="📥 Memasukkan JSON"):
    try:
        domain_code, var_id_str = filename.replace(".json", "").split("_")
    except ValueError:
        print(f"⚠️ Format nama file tidak sesuai: {filename}")
        continue

    if LIMIT_DOMAIN and domain_code != LIMIT_DOMAIN:
        continue

    var_id = int(var_id_str)
    filepath = os.path.join(DATA_FOLDER, filename)

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not data.get("datacontent"):
            continue

        # === METADATA VARIABEL ===
        var_info = data.get("var", [])[0]
        var_label = var_info.get("label", "")
        labelvervar = data.get("labelvervar", "")
        subject_info = data.get("subject", [{}])[0]

        domain_mapping = {"3500": "Prov. Jawa Timur"}
        wilayah = domain_mapping.get(domain_code, "Tidak diketahui")

        cur.execute("""
            INSERT OR IGNORE INTO variabel_metadata (
                domain, var_id, var_name, unit, subj, definisi,
                decimal, note, subject_label, last_update, data_availability,
                labelvervar
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            domain_code, var_id, var_label, var_info.get("unit", ""),
            var_info.get("subj", ""), var_info.get("def", ""), var_info.get("decimal"),
            var_info.get("note", ""), subject_info.get("label", ""),
            data.get("last_update", ""), data.get("data-availability", ""),
            labelvervar
        ))

        # === AMBIL NILAI ===
        vervar_vals = [str(v["val"]) for v in data.get("vervar", [])]
        turvar_vals = [str(v["val"]) for v in data.get("turvar", [])]
        tahun_vals = [str(v["val"]) for v in data.get("tahun", [])]
        turtahun_vals = [str(v["val"]) for v in data.get("turtahun", [])]

        key_map = {}
        for v, t, y, ty in product(vervar_vals, turvar_vals, tahun_vals, turtahun_vals):
            k = f"{v}{var_id}{t}{y}{ty}"
            key_map[k] = {
                "vervar_val": int(v), "turvar_val": int(t),
                "tahun_val": int(y), "turtahun_val": int(ty)
            }

        # === LABELS ===
        vervar = {str(i["val"]): i["label"] for i in data.get("vervar", [])}
        turvar = {str(i["val"]): i["label"] for i in data.get("turvar", [])}
        tahun = {str(i["val"]): int(i["label"]) if str(i["label"]).isdigit() else None for i in data.get("tahun", [])}
        turtahun = {str(i["val"]): i["label"] for i in data.get("turtahun", [])}

        # === ISI DATA ===
        for key, value in data["datacontent"].items():
            if key not in key_map:
                print(f"⚠️ KEY TIDAK DITEMUKAN DI KOMBINASI: {key}")
                gagal += 1
                continue

            parsed = key_map[key]

            cur.execute("""
                INSERT OR IGNORE INTO statistik_data (
                    domain, wilayah, var_id, var_label, labelvervar,
                    vervar_val, vervar_label,
                    turvar_val, turvar_label,
                    tahun_val, tahun_label,
                    turtahun_val, turtahun_label,
                    nilai
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                domain_code, wilayah, var_id, var_label, labelvervar,
                parsed["vervar_val"], vervar.get(str(parsed["vervar_val"]), ""),
                parsed["turvar_val"], turvar.get(str(parsed["turvar_val"]), ""),
                parsed["tahun_val"], tahun.get(str(parsed["tahun_val"]), None),
                parsed["turtahun_val"], turtahun.get(str(parsed["turtahun_val"]), ""),
                value
            ))
            sukses += 1

    except Exception as e:
        print(f"⚠️ ERROR file {filename}: {e}")
        gagal += 1

conn.commit()
conn.close()

print(f"\n✅ SELESAI: {sukses} baris berhasil, {gagal} gagal.")
