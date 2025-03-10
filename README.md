# Sistem Informasi Magang Kominfo Kabupaten Karo 2025

![Magang Kominfo Karo Banner](https://img.shields.io/badge/Magang%20Kominfo-Kabupaten%20Karo%202025-6c5ce7)
<!-- ![Odoo Version](https://img.shields.io/badge/Odoo-17.0-3498db) -->
![License](https://img.shields.io/badge/License-LGPL--3-28a745)

Sistem pengelolaan peserta magang di Dinas Komunikasi dan Informatika Kabupaten Karo oleh Mahasiswa Methodist Indonesia

## Fitur Utama

- 📊 **Dashboard Monitoring** - Tampilan statistik realtime peserta magang dan progres mereka
- 👥 **Manajemen Peserta** - Pengelolaan data peserta dan status magang
- 📝 **Tracking Progres** - Pencatatan dan persetujuan laporan progres kegiatan
- 📅 **Kalender Kegiatan** - Visualisasi kegiatan dalam bentuk kalender
- 📊 **Statistik Divisi** - Analisis peserta magang berdasarkan divisi (Programmer, Designer, Humas)

## Setup dan Instalasi

### 1. Prasyarat

- Python 3.10+
- PostgreSQL 12+
- Git

### 2. Instalasi Odoo 17

```bash
# Clone repository Odoo 17
git clone https://github.com/odoo/odoo.git --depth 1 --branch 17.0 odoo17

# Install dependencies
cd odoo17
pip install -r requirements.txt

# Create PostgreSQL user and database
sudo -u postgres createuser -s odoo
sudo -u postgres createdb odoo17_magang
```

### 3. Konfigurasi

Buat file konfigurasi `odoo.conf`:

```
[options]
addons_path = /path/to/odoo17/addons,/path/to/odoo17/custom_addons
admin_passwd = admin
db_host = localhost
db_port = 5432
db_user = odoo
db_password = password
db_name = odoo17_magang
http_port = 8069
```

### 4. Setup Custom Addon

```bash
# Buat direktori custom_addons
mkdir -p /path/to/odoo17/custom_addons
cd /path/to/odoo17/custom_addons

# Clone repository addon magang
git clone https://github.com/FransHutagalung/MagangKominfoKaro2025.git
```

### 5. Jalankan Odoo

```bash
cd /path/to/odoo17
python3 odoo-bin -c odoo.conf
```

Buka browser dan akses `http://localhost:8069`

### 6. Instalasi Modul

1. Aktifkan mode developer: Settings > Developer Tools > Activate developer mode
2. Pergi ke Apps > Update Apps List
3. Cari "Magang Kominfo" dan klik Install

## Struktur Proyek

```
magang_kominfo_2025/
├── controllers/
├── models/
│   ├── magang.py    # Model peserta magang
│   ├── progress.py  # Model progress magang
│   └── dashboard.py # Model dashboard
├── security/
│   └── ir.model.access.csv # Hak akses
├── static/
│   └── description/
│       └── karo.png        # Logo dan aset
├── views/
│   ├── action_views.xml # Action View
│   ├── dashboard_action.xml # Action dashboard
│   ├── dashboard_form_views.xml # Form dashboard
│   ├── dashboard_init.xml # Init dashboard
│   ├── futuristik_dashboard.xml # Upgrade dashboard UI
│   ├── magang_kanban_views.xml    # Kanban View
│   ├── magang_views.xml    # View peserta
│   ├── menu_dahboard.xml    # Dashboard Menu
│   └── menu_views.xml      # Menu Views
│   ├── progress_views.xml  # View progress
└── __manifest__.py         # Definisi modul
```

## Kontribusi

Silakan buat fork dan pull request untuk kontribusi pada proyek ini.

## Lisensi

LGPL-3

## Kontak

Dinas Komunikasi dan Informatika Kabupaten Karo - kominfo@karokab.go.id
