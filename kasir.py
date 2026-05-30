import streamlit as st
import pandas as pd

# Konfigurasi Halaman Utama
st.set_page_config(page_title="Kasir Kopeng", page_icon="🏪", layout="wide")
st.title("🏪 Aplikasi Kasir Kopeng")

# Inisialisasi data (menggunakan Session State agar data tidak hilang saat halaman di-refresh)
if 'inventory' not in st.session_state:
    st.session_state.inventory = [
        {"id": 1, "nama": "Beras Premium 5kg", "stok": 12, "harga_modal": 60000, "harga_jual": 72000},
        {"id": 2, "nama": "Minyak Goreng 2L", "stok": 3, "harga_modal": 28000, "harga_jual": 34000},
        {"id": 3, "nama": "Gula Pasir 1kg", "stok": 15, "harga_modal": 12000, "harga_jual": 15000},
        {"id": 4, "nama": "Mie Instan (Kardus)", "stok": 4, "harga_modal": 102000, "harga_jual": 115000},
    ]

if 'transactions' not in st.session_state:
    st.session_state.transactions = []

# ==================== SIDEBAR & NOTIFIKASI STOK MENIPIS ====================
st.sidebar.header("🧭 Menu Navigasi")
menu = st.sidebar.selectbox("Pilih Halaman:", ["Kasir (Transaksi)", "Manajemen Gudang", "Laporan Keuntungan"])

st.sidebar.markdown("---")
st.sidebar.subheader("⚠️ Notifikasi Gudang")

# Logika deteksi stok menipis (misal: stok kurang dari atau sama dengan 5)
stok_menipis = [item for item in st.session_state.inventory if item['stok'] <= 5]

if stok_menipis:
    for item in stok_menipis:
        st.sidebar.warning(f"**{item['nama']}** hampir habis! Sisa stok: **{item['stok']}** pcs.")
else:
    st.sidebar.success("✅ Semua stok di gudang aman!")


# ==================== HALAMAN 1: KASIR (TRANSAKSI) ====================
if menu == "Kasir (Transaksi)":
    st.header("🛒 Menu Kasir")
    
    # Filter hanya barang yang stoknya lebih dari 0
    barang_tersedia = [item['nama'] for item in st.session_state.inventory if item['stok'] > 0]
    
    if not barang_tersedia:
        st.error("❌ Stok semua barang di gudang kosong! Silakan isi kembali di Manajemen Gudang.")
    else:
        # Pilih Barang
        pilihan_barang = st.selectbox("Pilih Barang yang Dibeli:", barang_tersedia)
        
        # Ambil data detail barang yang dipilih
        detail_barang = next(item for item in st.session_state.inventory if item['nama'] == pilihan_barang)
        
        st.info(f"💵 Harga Jual: Rp {detail_barang['harga_jual']:,} | 📦 Stok Gudang: {detail_barang['stok']} pcs")
        
        # Input Jumlah Beli
        jumlah_beli = st.number_input("Jumlah Barang:", min_value=1, max_value=detail_barang['stok'], value=1, step=1)
        
        # Kalkulasi Transaksi & Keuntungan
        total_bayar = detail_barang['harga_jual'] * jumlah_beli
        total_modal = detail_barang['harga_modal'] * jumlah_beli
        keuntungan_transaksi = total_bayar - total_modal
        
        st.markdown(f"### Total yang Harus Dibayar: **Rp {total_bayar:,}**")
        st.caption(f"(Estimasi keuntungan dari transaksi ini: Rp {keuntungan_transaksi:,})")
        
        # Tombol Bayar
        if st.button("🟢 Proses & Cetak Transaksi", use_container_width=True):
            # Potong stok di gudang
            detail_barang['stok'] -= jumlah_beli
            
            # Catat ke riwayat transaksi
            st.session_state.transactions.append({
                "Barang": detail_barang['nama'],
                "Jumlah": jumlah_beli,
                "Total Bayar": total_bayar,
                "Keuntungan": keuntungan_transaksi
            })
            
            st.success(f"🎉 Transaksi Sukses! Stok {detail_barang['nama']} telah diperbarui.")
            st.balloons()


# ==================== HALAMAN 2: MANAJEMEN GUDANG ====================
elif menu == "Manajemen Gudang":
    st.header("📦 Manajemen Gudang & Stok")
    
    # Tampilkan Tabel Barang Saat Ini
    df_gudang = pd.DataFrame(st.session_state.inventory)
    # Format angka agar lebih rapi
    df_gudang_tampil = df_gudang.copy()
    df_gudang_tampil['harga_modal'] = df_gudang_tampil['harga_modal'].apply(lambda x: f"Rp {x:,}")
    df_gudang_tampil['harga_jual'] = df_gudang_tampil['harga_jual'].apply(lambda x: f"Rp {x:,}")
    
    st.subheader("📋 Daftar Stok dan Harga Barang")
    st.dataframe(df_gudang_tampil.set_index('id'), use_container_width=True)
    
    # Form Tambah/Update Barang Baru
    st.markdown("---")
    st.subheader("➕ Tambah Barang Baru ke Gudang")
    
    with st.form("form_gudang", clear_on_submit=True):
        nama_baru = st.text_input("Nama Barang Baru:")
        stok_awal = st.number_input("Jumlah Stok Awal:", min_value=1, value=10)
        harga_modal_baru = st.number_input("Harga Modal (Rp):", min_value=0, value=10000, step=500)
        harga_jual_baru = st.number_input("Harga Jual ke Konsumen (Rp):", min_value=0, value=12000, step=500)
        
        submit_gudang = st.form_submit_button("Simpan ke Gudang")
        
        if submit_gudang:
            if nama_baru.strip() == "":
                st.error("Nama barang tidak boleh kosong!")
            elif harga_jual_baru < harga_modal_baru:
                st.warning("Peringatan: Harga jual lebih rendah daripada harga modal! Anda bisa rugi.")
            else:
                next_id = max([item['id'] for item in st.session_state.inventory]) + 1 if st.session_state.inventory else 1
                st.session_state.inventory.append({
                    "id": next_id,
                    "nama": nama_baru,
                    "stok": stok_awal,
                    "harga_modal": harga_modal_baru,
                    "harga_jual": harga_jual_baru
                })
                st.success(f"✔️ Berhasil menambahkan {nama_baru} ke dalam gudang!")
                st.rerun()


# ==================== HALAMAN 3: LAPORAN KEUNTUNGAN ====================
elif menu == "Laporan Keuntungan":
    st.header("📈 Laporan Keuntungan Transaksi")
    
    if not st.session_state.transactions:
        st.info("Belum ada transaksi yang tercatat untuk hari ini.")
    else:
        df_transaksi = pd.DataFrame(st.session_state.transactions)
        
        # Tampilkan Tabel Riwayat Transaksi
        st.subheader("📜 Riwayat Transaksi Masuk")
        st.dataframe(df_transaksi, use_container_width=True)
        
        # Hitung Total Omset dan Keuntungan Bersih
        total_omset = df_transaksi["Total Bayar"].sum()
        total_keuntungan = df_transaksi["Keuntungan"].sum()
        
        st.markdown("---")
        # Menampilkan Ringkasan Finansial dalam bentuk Kartu (Metrics)
        kolom1, kolom2 = st.columns(2)
        with kolom1:
            st.metric(label="💰 Total Omset (Penjualan Kross)", value=f"Rp {total_omset:,}")
        with kolom2:
            st.metric(label="📈 Total Keuntungan Bersih (Profit)", value=f"Rp {total_keuntungan:,}")