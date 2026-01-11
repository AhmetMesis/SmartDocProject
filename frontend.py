import streamlit as st
import requests
from PIL import Image
import io

# Backend API Adresi (Docker çalışıyor olmalı)
API_URL = "http://localhost:8000"

st.set_page_config(page_title="Akıllı Doküman Analiz", page_icon="📄", layout="wide")

st.title("📄 Akıllı Doküman Analiz Platformu")
st.markdown("---")

# Yan Menü (Sidebar)
st.sidebar.header("İşlem Seçimi")
option = st.sidebar.radio(
    "Ne yapmak istiyorsunuz?", 
    ("Doküman Tarama & OCR", "QR Kod Analizi", "Yapay Zeka (AI) Analizi", "QR Kod Oluşturucu")
)

# --- MOD 1: QR KOD OLUŞTURUCU (Dosya Yükleme Gerektirmez) ---
if option == "QR Kod Oluşturucu":
    st.header("🔲 QR Kod Oluşturucu")
    st.info("İstediğiniz metni veya linki girin, anında QR kodunu indirin.")
    
    # Kullanıcıdan veri al
    qr_data = st.text_input("QR Kod İçeriği (Web Sitesi, WiFi Şifresi, Metin vb.):", placeholder="Örn: https://www.firat.edu.tr")
    
    if st.button("QR Kod Oluştur"):
        if qr_data:
            with st.spinner('QR Kod oluşturuluyor...'):
                try:
                    # Backend'e GET isteği atıyoruz
                    response = requests.get(f"{API_URL}/generate-qr", params={"data": qr_data})
                    
                    if response.status_code == 200:
                        # Gelen resim verisini işle
                        image = Image.open(io.BytesIO(response.content))
                        
                        col1, col2 = st.columns([1, 2])
                        with col1:
                            st.image(image, caption="Oluşturulan QR Kod", width=250)
                        
                        with col2:
                            st.success("Başarıyla oluşturuldu!")
                            # İndirme Butonu
                            st.download_button(
                                label="QR Kodu İndir (PNG)",
                                data=response.content,
                                file_name="generated_qr.png",
                                mime="image/png"
                            )
                    else:
                        st.error("Sunucu hatası oluştu.")
                except Exception as e:
                    st.error(f"Bağlantı Hatası: {e}. Backend (Docker) çalışıyor mu?")
        else:
            st.warning("Lütfen bir metin giriniz.")

# --- MOD 2: DOSYA ANALİZ İŞLEMLERİ (OCR, AI, QR OKUMA) ---
else:
    # Bu işlemler için dosya yükleme alanı gösterilir
    uploaded_file = st.file_uploader("İşlem yapmak için bir resim yükleyin...", type=["jpg", "png", "jpeg"])

    if uploaded_file is not None:
        # Resmi ekranda göster
        image = Image.open(uploaded_file)
        st.image(image, caption='Yüklenen Doküman', use_column_width=True)
        
        # Resmi byte formatına çevir
        img_bytes = uploaded_file.getvalue()
        files = {"file": (uploaded_file.name, img_bytes, uploaded_file.type)}

        # --- SEÇENEK: OCR ---
        if option == "Doküman Tarama & OCR":
            if st.button("Metni Oku (OCR)"):
                with st.spinner('Taranıyor ve okunuyor...'):
                    try:
                        response = requests.post(f"{API_URL}/scan-ocr", files=files)
                        if response.status_code == 200:
                            data = response.json()
                            st.success("İşlem Başarılı!")
                            st.subheader("Tespit Edilen Metin:")
                            st.text_area("", data.get("tespit_edilen_metin", ""), height=300)
                        else:
                            st.error("Hata oluştu.")
                    except Exception as e:
                        st.error(f"Bağlantı Hatası: {e}")

        # --- SEÇENEK: QR KOD ANALİZİ (OKUMA) ---
        elif option == "QR Kod Analizi":
            if st.button("QR Kodları Bul"):
                with st.spinner('Analiz ediliyor...'):
                    try:
                        response = requests.post(f"{API_URL}/analyze-qr", files=files)
                        if response.status_code == 200:
                            data = response.json()
                            results = data.get("bulunan_kodlar", [])
                            
                            if results:
                                st.success(f"{len(results)} adet kod bulundu.")
                                for i, res in enumerate(results):
                                    st.info(f"**Kod {i+1}:** {res['veri']} ({res['icerik']})")
                            else:
                                st.warning("Görselde QR kod bulunamadı.")
                        else:
                            st.error("Hata oluştu.")
                    except Exception as e:
                        st.error(f"Bağlantı Hatası: {e}")

        # --- SEÇENEK: YAPAY ZEKA (GEMINI) ---
        elif option == "Yapay Zeka (AI) Analizi":
            st.info("Bu işlem Google Gemini modelini kullanır.")
            if st.button("Yapay Zeka ile Analiz Et"):
                with st.spinner('Gemini belgeyi inceliyor...'):
                    try:
                        response = requests.post(f"{API_URL}/analyze-with-ai", files=files)
                        if response.status_code == 200:
                            data = response.json()
                            st.success("Analiz Tamamlandı!")
                            st.markdown(data.get("analiz_sonucu", "Sonuç yok."))
                            st.caption(f"Kullanılan Model: {data.get('kullanilan_model')}")
                        else:
                            st.error(f"API Hatası: {response.text}")
                    except Exception as e:
                        st.error(f"Bağlantı Hatası: {e}")

    else:
        st.info("Lütfen sol menüden bir işlem seçin ve dosya yükleyin (QR Oluşturma hariç).")