import streamlit as st
import pandas as pd

# Konfigurasi Halaman Utama
st.set_page_config(page_title="Kasir Kopeng", page_icon="🏪", layout="wide")

# ==================== KODE CSS UNTUK TAMPILAN PROFESIONAL ====================
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            
            .stButton>button {
                border-radius: 8px;
                background-color: #0078D7;
                color: white;
                font-weight: bold;
                transition: 0.3s;
            }
            .stButton>button:hover {
                background-color: #005A9E;
                color: white;
            }
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>🏪 Aplikasi Kasir Kopeng</h1>", unsafe_allow_html=True)
st.markdown("---")

# ==================== INISIALISASI DATA BARANG ====================
if 'inventory' not in st.session_state:
    st.session_state.inventory = [
        {"id": 1, "nama": "D'Jalu Kecil", "stok": 50, "harga_modal": 9300, "harga_jual": 11000},
        {"id": 2, "nama": "Sky", "stok": 50, "harga_modal": 15800, "harga_jual": 18000},
        {"id": 3, "nama": "Golden Bold", "stok": 50, "harga_modal": 9900, "harga_jual": 12000},
        {"id": 4, "nama": "Luffman", "stok": 50, "harga_modal": 7800, "harga_jual": 10000},
        {"id": 5, "nama": "Surya Kecil", "stok": 50, "harga_modal": 26000, "harga_jual": 28000},
        {"id": 6, "nama": "Sampoerna Kecil", "stok": 50, "harga_modal": 25200, "harga_jual": 27000},
        {"id": 7, "nama": "Sampoerna Besar", "stok": 50, "harga_modal": 35200, "harga_jual": 37000},
        {"id": 8, "nama": "HRZ", "stok": 50, "harga_modal": 9400, "harga_jual": 11000},
        {"id": 9, "nama": "F. Biru", "stok": 50, "harga_modal": 15300, "harga_jual": 17000},
        {"id": 10, "nama": "OK Bold", "stok": 50, "harga_modal": 8400, "harga_jual": 10000},
        {"id": 11, "nama": "HD Putih", "stok": 50, "harga_modal": 10000, "harga_jual": 12000},
        {"id": 12, "nama": "Dji Sam Soe", "stok": 50, "harga_modal": 26000, "harga_jual": 28000},
        {"id": 13, "nama": "MC Merah", "stok": 50, "harga_modal": 12500, "harga_jual": 14000},
        {"id": 14, "nama": "Feloz Sultan", "stok": 50, "harga_modal": 14500, "harga_jual": 16000},
        {"id": 15, "nama": "F. Mangga", "stok": 50, "harga_modal": 17300, "harga_jual": 19000},
        {"id": 16, "nama": "F. Bold", "stok": 50, "harga_modal": 15700, "harga_jual": 17000},
        {"id": 17, "nama": "MC Putih", "stok": 50, "harga_modal": 12500, "harga_jual": 14000},
        {"id": 18, "nama": "HD Mild", "stok": 50, "harga_modal": 13000, "harga_jual": 15000},
        {"id": 19, "nama": "TRI (5.5 / 3)", "stok": 999, "harga_modal": 12300, "harga_jual": 14000},
        {"id": 20, "nama": "TRI (7 / 12)", "stok": 999, "harga_modal": 10000, "harga_jual": 12000},
        {"id": 21, "nama": "Axis (5.5 / 3)", "stok": 999, "harga_modal": 11900, "harga_jual": 14000},
        {"id": 22, "nama": "Axis (5 / 5)", "stok": 999, "harga_modal": 13700, "harga_jual": 15000},
        {"id": 23, "nama": "Tsel (6 / 2)", "stok": 999, "harga_modal": 9800, "harga_jual": 12000},
        {"id": 24, "nama": "Tsel (5 / 3)", "stok": 999, "harga_modal": 13500, "harga_jual": 15000},
        {"id": 25, "nama": "Tsel (4 / 5)", "stok": 999, "harga_modal": 13500, "harga_jual": 15000},
        {"id": 26, "nama": "Axis (13 / 3)", "stok": 999, "harga_modal": 16500, "harga_jual": 18000},
        {"id": 27, "nama": "Axis (6 / 5)", "stok": 999, "harga_modal": 15500, "harga_jual": 17000},
        {"id": 28, "nama": "Top-Up Saldo DANA (Bebas Nominal)", "stok": 9999, "harga_modal": 0, "harga_jual": 0},
        {"id": 29, "nama": "Top-Up GoPay (Bebas Nominal)", "stok": 9999, "harga_modal": 0, "harga_jual": 0},
        {"id": 30, "nama": "Transfer BRI (Bebas Nominal)", "stok": 9999, "harga_modal": 0, "harga_jual": 0},
        {"id": 31, "nama": "Top-Up Saveplus (Bebas Nominal)", "stok": 9999, "harga_modal": 0, "harga_jual": 0},
    ]

if 'transactions' not in st.session_state:
    st.session_state.transactions = []

# ==================== SIDEBAR NAVIGASI ====================
st.sidebar.markdown("<h2 style='text-align: center;'>🧭 Navigasi</h2>", unsafe_allow_html=True)
menu = st.sidebar.radio("Pilih Menu:", ["🛒 Kasir (Transaksi)", "📦 Manajemen Gudang", "📈 Laporan Keuntungan"])

st.sidebar.markdown("---")
st.sidebar.markdown("### ⚠️ Notifikasi Gudang")

stok_menipis = [item for item in st.session_state.inventory if item['stok'] <= 5]
if stok_menipis:
    for item in stok_menipis:
        st.sidebar.error(f"🚨 **{item['nama']}** sisa: **{item['stok']}**!")
else:
    st.sidebar.success("✅ Stok aman terkendali.")

# ==================== HALAMAN 1: KASIR ====================
if menu == "🛒 Kasir (Transaksi)":
    st.markdown("### 🛒 Sistem Point of Sale (POS)")
    
    barang_tersedia = [item['nama'] for item in st.session_state.inventory if item['stok'] > 0]
    
    if not barang_tersedia:
        st.error("❌ Stok gudang kosong!")
    else:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            pilihan_barang = st.selectbox("Cari & Pilih Item:", barang_tersedia)
            detail_barang = next(item for item in st.session_state.inventory if item['nama'] == pilihan_barang)
            jumlah_beli = st.number_input("Jumlah:", min_value=1, max_value=detail_barang['stok'], value=1, step=1)
            
            # --- LOGIKA KHUSUS UNTUK SALDO BEBAS NOMINAL ---
            kata_kunci_digital = ["DANA", "GOPAY", "BRI", "SAVEPLUS"]
            is_digital_bebas = any(kunci in pilihan_barang.upper() for kunci in kata_kunci_digital)
            
            if is_digital_bebas:
                st.warning(f"💡 Khusus {detail_barang['nama']}, atur nominal modal dan harga jual di bawah:")
                harga_modal_custom = st.number_input("Input Harga Modal (Rp):", min_value=0, value=0, step=1000)
                harga_jual_custom = st.number_input("Input Harga Jual (Rp):", min_value=0, value=0, step=1000)
                
                total_modal = harga_modal_custom * jumlah_beli
                total_bayar = harga_jual_custom * jumlah_beli
            else:
                total_modal = detail_barang['harga_modal'] * jumlah_beli
                total_bayar = detail_barang['harga_jual'] * jumlah_beli
                
        with col2:
            if not is_digital_bebas:
                st.info(f"**Info Item:**\n\nHarga Jual: Rp {detail_barang['harga_jual']:,}\n\nSisa Stok: {detail_barang['stok']}")
            else:
                st.info("**Info Item:**\n\nProduk Digital/Saldo/Transfer\n\nNominal Bebas")
        
        keuntungan_transaksi = total_bayar - total_modal
        st.markdown(f"<h3 style='color: #2E7D32;'>Total Tagihan: Rp {total_bayar:,}</h3>", unsafe_allow_html=True)
        
        if st.button("🟢 Proses Transaksi", use_container_width=True):
            detail_barang['stok'] -= jumlah_beli
            st.session_state.transactions.append({
                "Barang": detail_barang['nama'],
                "Jumlah": jumlah_beli,
                "Total Bayar": total_bayar,
                "Keuntungan": keuntungan_transaksi
            })
            st.success(f"✔️ Transaksi {detail_barang['nama']} berhasil dicatat!")

# ==================== HALAMAN 2: MANAJEMEN GUDANG ====================
elif menu == "📦 Manajemen Gudang":
    st.markdown("### 📦 Kelola Inventaris & Edit Harga")
    
    df_gudang = pd.DataFrame(st.session_state.inventory)
    df_gudang_tampil = df_gudang.copy()
    df_gudang_tampil['harga_modal'] = df_gudang_tampil['harga_modal'].apply(lambda x: f"Rp {x:,}")
    df_gudang_tampil['harga_jual'] = df_gudang_tampil['harga_jual'].apply(lambda x: f"Rp {x:,}")
    
    st.dataframe(df_gudang_tampil.set_index('id'), use_container_width=True)
    
    with st.expander("➕ Klik di sini untuk Tambah Item Baru"):
        with st.form("form_gudang", clear_on_submit=True):
            nama_baru = st.text_input("Nama Produk/Layanan:")
            col1, col2, col3 = st.columns(3)
            with col1:
                stok_awal = st.number_input("Stok Awal:", min_value=1, value=10)
            with col2:
                harga_modal_baru = st.number_input("Modal (Rp):", min_value=0, value=10000, step=500)
            with col3:
                harga_jual_baru = st.number_input("Harga Jual (Rp):", min_value=0, value=12000, step=500)
            
            submit_gudang = st.form_submit_button("Simpan Item", use_container_width=True)
            
            if submit_gudang:
                next_id = max([item['id'] for item in st.session_state.inventory]) + 1 if st.session_state.inventory else 1
                st.session_state.inventory.append({
                    "id": next_id, "nama": nama_baru, "stok": stok_awal,
                    "harga_modal": harga_modal_baru, "harga_jual": harga_jual_baru
                })
                st.rerun()

# ==================== HALAMAN 3: LAPORAN KEUNTUNGAN ====================
elif menu == "📈 Laporan Keuntungan":
    st.markdown("### 📈 Ringkasan Finansial")
    
    if not st.session_state.transactions:
        st.info("Belum ada transaksi terekam.")
    else:
        df_transaksi = pd.DataFrame(st.session_state.transactions)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="💰 Omset Kotor (Pemasukan)", value=f"Rp {df_transaksi['Total Bayar'].sum():,}")
        with col2:
            st.metric(label="✅ Laba Bersih (Keuntungan)", value=f"Rp {df_transaksi['Keuntungan'].sum():,}")
            
        st.markdown("**Detail Riwayat**")
        st.dataframe(df_transaksi, use_container_width=True)
