import sqlite3

# Connect ke file DB (kalau belum ada, akan dibuat)
conn = sqlite3.connect("bps_data.db")
cur = conn.cursor()

# Tabel untuk metadata variabel
cur.execute("""
CREATE TABLE IF NOT EXISTS variabel_metadata (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    domain TEXT,
    var_id INTEGER,
    var_name TEXT,
    unit TEXT,
    subj TEXT,
    definisi TEXT,
    decimal INTEGER,
    note TEXT,
    subject_label TEXT,
    last_update TEXT,
    data_availability TEXT,
    labelvervar TEXT,
    UNIQUE(domain, var_id)
)
""")

# Tabel untuk data statistik numerik
cur.execute("""
CREATE TABLE IF NOT EXISTS statistik_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    domain TEXT,
    wilayah TEXT,
    var_id INTEGER,
    var_label TEXT,
    labelvervar TEXT,
    vervar_val INTEGER,
    vervar_label TEXT,
    turvar_val INTEGER,
    turvar_label TEXT,
    tahun_val INTEGER,
    tahun_label INTEGER,
    turtahun_val INTEGER,
    turtahun_label TEXT,
    nilai REAL,
    UNIQUE(domain, var_id, vervar_val, turvar_val, tahun_val, turtahun_val)
)
""")

# Simpan & tutup koneksi
conn.commit()
conn.close()
