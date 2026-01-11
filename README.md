# 📄 SmartDoc - Akıllı Doküman Analiz ve Yönetim Platformu

![Python](https://img.shields.io/badge/Python-3.9-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.68-green?style=for-the-badge&logo=fastapi)
![Docker](https://img.shields.io/badge/Docker-Enabled-blue?style=for-the-badge&logo=docker)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-red?style=for-the-badge&logo=streamlit)

[cite_start]**Akıllı Doküman Analiz Platformu**, görüntü işleme (OpenCV), optik karakter tanıma (OCR) ve üretken yapay zeka (Google Gemini AI) teknolojilerini birleştiren bütünleşik bir doküman yönetim çözümüdür[cite: 289, 294].

[cite_start]Bu proje, fiziksel dokümanları (fatura, fiş, kimlik, ders notu vb.) sadece dijitalleştirmekle kalmaz; onları anlamlandırır, özetler ve aranabilir veri haline getirir[cite: 292, 295].

---

## 🚀 Özellikler

Proje, modern mikroservis mimarisine uygun olarak 4 ana modülden oluşur:

* [cite_start]**📷 Akıllı Tarayıcı (Scanner):** OpenCV kullanarak yamuk çekilmiş fotoğrafların perspektifini düzeltir, gürültüleri temizler ve tarayıcı kalitesine getirir[cite: 308].
* [cite_start]**📝 OCR (Metin Tanıma):** Tesseract-OCR motoru ile doküman üzerindeki Türkçe ve İngilizce metinleri %90+ doğrulukla dijital metne dönüştürür[cite: 309].
* **🧠 Yapay Zeka Analizi (Gemini AI):** Google Gemini 1.5 Flash modelini kullanarak belgenin türünü (Fatura, Reçete, Sözleşme vb.) tespit eder, içeriğini özetler ve kritik verileri (Tarih, Tutar) çıkarır.
* **🔲 QR Kod Yönetimi (Çift Yönlü):**
    * [cite_start]**Okuma:** Görseldeki QR kodları tespit eder ve içeriğini (URL, WiFi, vCard) analiz eder[cite: 310].
    * [cite_start]**Oluşturma:** İstediğiniz metin veya linkten anında QR kod üretir[cite: 299].
* [cite_start]**🐳 Dockerize Yapı:** Tüm bağımlılıklar (Tesseract, System Libraries) Docker konteyner yapısında paketlenmiştir, "her yerde çalışır" prensibine uygundur[cite: 312, 330].

---

## 🛠️ Teknolojiler

* [cite_start]**Backend:** Python, FastAPI, Uvicorn[cite: 311, 327].
* **Frontend:** Streamlit.
* [cite_start]**Görüntü İşleme:** OpenCV, NumPy, Pillow[cite: 319].
* [cite_start]**OCR:** Tesseract-OCR, Pytesseract[cite: 323].
* **Yapay Zeka:** Google Generative AI (Gemini 1.5 Flash).
* [cite_start]**QR İşlemleri:** Pyzbar, Qrcode[cite: 325].
* [cite_start]**Dağıtım:** Docker, Docker Compose[cite: 330].

---

## ⚙️ Kurulum ve Çalıştırma

Projeyi yerel makinenizde çalıştırmak için aşağıdaki adımları izleyin.

### 1. Ön Hazırlıklar
Bilgisayarınızda **Docker** ve **Git** kurulu olmalıdır.

### 2. Repoyu Klonlayın
```bash
git clone [https://github.com/KULLANICI_ADINIZ/SmartDocProject.git](https://github.com/KULLANICI_ADINIZ/SmartDocProject.git)
cd SmartDocProject
