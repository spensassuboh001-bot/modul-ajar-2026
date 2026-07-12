import streamlit as st
from groq import Groq

# 1. Konfigurasi Tampilan Web
st.set_page_config(page_title="AI Modul Ajar Kurikulum Merdeka", page_icon="📝", layout="centered")

st.title("📝 Generator Modul Ajar Kurikulum Merdeka")
st.write("Aplikasi pembantu guru menyusun modul ajar berbasis AI secara cepat dan gratis.")

# 2. Ambil API Key secara aman dari Hugging Face Secrets
# (Nanti kita akan masukkan API key ini di pengaturan Hugging Face)
if "GROQ_API_KEY" in st.secrets:
    api_key = st.secrets["GROQ_API_KEY"]
else:
    st.error("API Key Groq belum dikonfigurasi di Hugging Face Secrets!")
    st.stop()

client = Groq(api_key=api_key)

# 3. Form Input untuk Guru
st.subheader("📋 Informasi Modul Ajar")

mapel = st.text_input("Mata Pelajaran", placeholder="Contoh: Matematika, Bahasa Indonesia")

fase = st.selectbox("Fase / Kelas", [
    "Fase A (Kelas 1-2)", 
    "Fase B (Kelas 3-4)", 
    "Fase C (Kelas 5-6)", 
    "Fase D (Kelas 7-9)", 
    "Fase E (Kelas 10)", 
    "Fase F (Kelas 11-12)"
])

tp = st.text_area("Tujuan Pembelajaran (TP)", placeholder="Contoh: Peserta didik dapat mengidentifikasi pecahan senilai menggunakan benda konkret.")

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

# 4. Tombol Proses Generator
if st.button("🚀 Buat Modul Ajar Sekarang"):
    if not mapel or not tp:
        st.warning("Mohon isi Mata Pelajaran dan Tujuan Pembelajaran terlebih dahulu!")
    else:
        with st.spinner("AI sedang merumuskan modul ajar terbaik... Mohon tunggu..."):
            
            # Merangkai instruksi (Prompt) otomatis ke AI agar sesuai Kurikulum Merdeka
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
                # Mengirim perintah ke model Llama 3 milik Groq
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    model="llama-3.3-70b-versatile", # Model gratis, sangat cepat, dan pintar
                )
                
                hasil_modul = chat_completion.choices[0].message.content
                
                # Menampilkan Hasil di Layar Web
                st.success("✨ Modul Ajar Berhasil Dibuat!")
                st.markdown("---")
                st.markdown(hasil_modul)
                st.markdown("---")
                
                # Fitur Download sederhana (Teks format .txt / .doc bisa di-copy langsung oleh guru)
                st.download_button(
                    label="📥 Download Hasil Modul Ajar (Text)",
                    data=hasil_modul,
                    file_name=f"Modul_Ajar_{mapel.replace(' ', '_')}.txt",
                    mime="text/plain"
                )
                
            except Exception as e:
                st.error(f"Terjadi kesalahan saat menghubungi server AI: {e}")
                st.info("Tip: Ini bisa terjadi karena batasan akses bersamaan. Silakan klik tombol Generate kembali dalam beberapa detik.")
