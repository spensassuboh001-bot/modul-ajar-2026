import streamlit as st
from groq import Groq

# 1. Mengubah Layout Menjadi Penuh (Wide) & Desain Modern
st.set_page_config(
    page_title="AI Generator Modul Ajar Kurikulum Merdeka", 
    page_icon="📝", 
    layout="wide"  # <--- Ini yang membuat tampilan penuh satu browser
)

# Styling Tambahan dengan CSS agar visual lebih modern dan bersih
st.markdown("""
    <style>
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    h1 {
        color: #1E3A8A; /* Warna Biru Gelap Modern */
        font-weight: 800;
    }
    .stButton>button {
        background-color: #2563EB; /* Tombol Biru Cerah */
        color: white;
        border-radius: 8px;
        font-weight: bold;
        width: 100%;
        padding: 0.5rem;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #1D4ED8;
        border-color: #1D4ED8;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Cek API Key
if "GROQ_API_KEY" in st.secrets:
    api_key = st.secrets["GROQ_API_KEY"]
else:
    st.error("API Key Groq belum dikonfigurasi di Secrets!")
    st.stop()

client = Groq(api_key=api_key)

# 3. Header Aplikasi
st.title("📝 AI Generator Modul Ajar")
st.subheader("Kurikulum Merdeka — Edisi Profesional & Cepat")
st.markdown("---")

# 4. Membagi Layar Menjadi 2 Kolom (Kiri untuk Input, Kanan untuk Hasil)
# Ini memanfaatkan ruang layar browser yang sudah penuh/lebar
kolom_input, kolom_hasil = st.columns([1, 1.5], gap="large")

with kolom_input:
    st.markdown("### 📋 Pengaturan Modul")
    
    mapel = st.text_input("Mata Pelajaran", placeholder="Contoh: Matematika, IPAS, Bahasa Inggris")
    
    fase = st.selectbox("Fase / Kelas", [
        "Fase A (Kelas 1-2)", 
        "Fase B (Kelas 3-4)", 
        "Fase C (Kelas 5-6)", 
        "Fase D (Kelas 7-9)", 
        "Fase E (Kelas 10)", 
        "Fase F (Kelas 11-12)"
    ])
    
    model_pembelajaran = st.selectbox("Model Pembelajaran Terbaru", [
        "Problem-Based Learning (PBL)",
        "Project-Based Learning (PjBL)",
        "Discovery Learning",
        "Inquiry Learning",
        "Cooperative Learning"
    ])
    
    p3 = st.multiselect("Dimensi Profil Pelajar Pancasila (P3)", [
        "Beriman, bertakwa kepada Tuhan YME, dan berakhlak mulia",
        "Berkebinekaan global",
        "Bergotong royong",
        "Mandiri",
        "Bernalar kritis",
        "Kreatif"
    ])
    
    tp = st.text_area("Tujuan Pembelajaran (TP)", placeholder="Contoh: Peserta didik dapat menganalisis hubungan antara makhluk hidup dan lingkungannya.", height=120)
    
    # Tombol ditaruh di kolom kiri
    tombol_proses = st.button("🚀 Buat Modul Ajar")

# 5. Proses Penampilan Hasil di Kolom Kanan
with kolom_hasil:
    st.markdown("### ✨ Hasil Generasi AI")
    
    if tombol_proses:
        if not mapel or not tp:
            st.warning("⚠️ Mohon lengkapi Mata Pelajaran dan Tujuan Pembelajaran!")
        else:
            with st.spinner("AI sedang merumuskan modul ajar terbaik... Mohon tunggu..."):
                p3_string = ", ".join(p3)
                prompt = f"""
                Bertindaklah sebagai Konsultan Kurikulum dan Ahli Pendidikan Indonesia. 
                Buatlah sebuah Modul Ajar Kurikulum Merdeka yang lengkap, sistematis, dan siap pakai berdasarkan data berikut:
                
                - Mata Pelajaran: {mapel}
                - {fase}
                - Tujuan Pembelajaran (TP): {tp}
                - Model Pembelajaran: {model_pembelajaran}
                - Profil Pelajar Pancasila (P3): {p3_string}
                
                Struktur modul harus memiliki komponen wajib berikut secara mendetail:
                1. INFORMASI UMUM (Identitas, Kompetensi Awal, P3, Sarana Prasarana, Target Peserta Didik)
                2. KOMPONEN INTI (Tujuan Pembelajaran, Pemahaman Bermakna, Pertanyaan Pemantik, Kegiatan Pembelajaran Lengkap berbasis model {model_pembelajaran} yang dipilih dari Pendahuluan, Inti, hingga Penutup)
                3. ASESMEN (Asesmen Diagnostik, Formatif, dan Sumatif)
                4. LAMPIRAN (Lembar Kerja Peserta Didik / LKPD sederhana, Bahan Bacaan Guru & Siswa, Glosarium, Daftar Pustaka)
                
                Tulis dalam Bahasa Indonesia yang formal, ramah, dan profesional. Jangan dipotong, berikan hasil yang lengkap dan detail.
                """
                
                try:
                    # Menggunakan model terbaru yang stabil dan pintar
                    chat_completion = client.chat.completions.create(
                        messages=[{"role": "user", "content": prompt}],
                        model="llama-3.3-70b-versatile",
                    )
                    
                    hasil_modul = chat_completion.choices[0].message.content
                    
                    # Menampilkan hasil di kotak teks khsusus yang rapi
                    st.success("Modul berhasil dibuat!")
                    st.markdown(hasil_modul)
                    
                    st.download_button(
                        label="📥 Download Modul (Teks)",
                        data=hasil_modul,
                        file_name=f"Modul_Ajar_{mapel.replace(' ', '_')}.txt",
                        mime="text/plain"
                    )
                    
                except Exception as e:
                    st.error(f"Terjadi kesalahan: {e}")
                    st.info("Tip: Jika server sibuk karena diakses bersamaan, silakan klik tombol sekali lagi.")
    else:
        st.info("Silakan isi data di kolom sebelah kiri dan klik 'Buat Modul Ajar' untuk melihat hasil di sini.")
