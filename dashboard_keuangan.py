import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Pelacak Pengeluaran", page_icon="💰")

st.title("💰 Dashboard Pelacak Pengeluaran")
st.write("Pantau pengeluaran bulanan Anda secara interaktif.")

# --- SIDEBAR (INPUT DATA) ---
st.sidebar.header("🎛️ Pengaturan")

# Slider untuk Total Budget
budget_total = st.sidebar.slider(
    "Tentukan Budget Bulanan (Rp)", 
    min_value=500000, 
    max_value=20000000, 
    step=100000, 
    value=5000000
)

st.sidebar.subheader("Masukkan Pengeluaran:")
# Input untuk Kategori (menggunakan Slider agar interaktif sesuai permintaan)
makan = st.sidebar.slider("🍔 Makan", 0, budget_total, 1500000)
transport = st.sidebar.slider("🚌 Transport", 0, budget_total, 800000)
hobi = st.sidebar.slider("🎮 Hobi", 0, budget_total, 500000)

# --- LOGIKA PERHITUNGAN ---
total_pengeluaran = makan + transport + hobi
sisa_budget = budget_total - total_pengeluaran

# Membuat DataFrame untuk Grafik
data = pd.DataFrame({
    'Kategori': ['Makan', 'Transport', 'Hobi'],
    'Jumlah (Rp)': [makan, transport, hobi]
})

# --- TAMPILAN DASHBOARD (MAIN AREA) ---

# 1. Menampilkan Metrik Utama (Kartu Angka)
col1, col2, col3 = st.columns(3)
col1.metric("Total Budget", f"Rp {budget_total:,}")
col2.metric("Total Pengeluaran", f"Rp {total_pengeluaran:,}", delta_color="inverse")
col3.metric("Sisa Budget", f"Rp {sisa_budget:,}", delta=sisa_budget)

st.divider()

# 2. Visualisasi Grafik Batang
st.subheader("📊 Grafik Pengeluaran vs Kategori")

# Menggunakan Matplotlib agar lebih fleksibel (atau bisa pakai st.bar_chart bawaan)
fig, ax = plt.subplots(figsize=(8, 4))
colors = ['#FF9999', '#66B2FF', '#99FF99']
bars = ax.bar(data['Kategori'], data['Jumlah (Rp)'], color=colors)

# Menambahkan label angka di atas batang
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval + (budget_total*0.01), f'Rp {int(yval):,}', ha='center', va='bottom')

ax.set_ylabel('Jumlah (Rp)')
ax.set_ylim(0, budget_total * 1.1) # Batas atas grafik dinamis berdasarkan budget
ax.axhline(y=budget_total, color='r', linestyle='--', label='Batas Budget') # Garis batas budget
ax.legend()

# Menampilkan plot di Streamlit
st.pyplot(fig)

# 3. Peringatan / Status
st.subheader("💡 Status Keuangan")
if total_pengeluaran > budget_total:
    st.error(f"⚠️ PERINGATAN: Anda melebihi budget sebesar Rp {abs(sisa_budget):,}!")
elif sisa_budget < (budget_total * 0.2):
    st.warning("⚠️ Hati-hati: Sisa budget Anda menipis (di bawah 20%).")
else:
    st.success("✅ Aman: Keuangan Anda masih terkendali.")

# Menampilkan tabel data mentah (opsional)
with st.expander("Lihat Detail Data"):
    st.dataframe(data)