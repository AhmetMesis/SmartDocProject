from fastapi import FastAPI, File, UploadFile, HTTPException, Response
import cv2
import numpy as np
import pytesseract
from pyzbar.pyzbar import decode
import qrcode
import io
import google.generativeai as genai
import os
from PIL import Image
from dotenv import load_dotenv  # YENİ EKLENDİ

# --- AYARLAR ---
app = FastAPI(title="Akıllı Doküman Analiz API", version="1.0.0")

# --- GÜVENLİK VE AI AYARLARI ---
# .env dosyasını yükle
load_dotenv()

# API Anahtarını gizli dosyadan (.env) çek
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Anahtar kontrolü (Hata ayıklamak için)
if not GEMINI_API_KEY:
    print("UYARI: GEMINI_API_KEY bulunamadı! Lütfen .env dosyasını oluşturun.")
else:
    genai.configure(api_key=GEMINI_API_KEY)

# --- 1. GÖRÜNTÜ İŞLEME & PERSPEKTİF DÜZELTME ---
def process_image(image_bytes):
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return img, thresh

# --- 2. API ENDPOINTLERİ ---

@app.get("/")
def read_root():
    return {"Durum": "Aktif", "Proje": "Akıllı Doküman Analiz Platformu"}

@app.post("/scan-ocr")
async def scan_and_extract_text(file: UploadFile = File(...)):
    contents = await file.read()
    original_img, processed_img = process_image(contents)
    
    try:
        text = pytesseract.image_to_string(processed_img, lang='tur+eng')
    except Exception as e:
        return {"Hata": "OCR motoru bulunamadı.", "Detay": str(e)}

    return {
        "dosya_adi": file.filename,
        "tespit_edilen_metin": text.strip(),
        "islem_basarisi": True
    }

@app.post("/analyze-qr")
async def analyze_qr_code(file: UploadFile = File(...)):
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    decoded_objects = decode(img)
    results = []
    
    for obj in decoded_objects:
        qr_data = obj.data.decode('utf-8')
        content_type = "Metin"
        if "http" in qr_data: content_type = "URL/Web Sitesi"
        elif "BEGIN:VCARD" in qr_data: content_type = "Kartvizit"
        elif "WIFI:" in qr_data: content_type = "WiFi"
            
        results.append({"veri": qr_data, "tip": obj.type, "icerik": content_type})
        
    return {"bulunan_kodlar": results}

@app.get("/generate-qr")
def generate_qr_code(data: str):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    
    # Resmi belleğe (RAM) kaydet
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    
    # Byte verisini al ve Response olarak döndür
    return Response(content=buf.getvalue(), media_type="image/png")

# --- GEMINI ENDPOINT (AKILLI MODEL SEÇİMİ) ---
@app.post("/analyze-with-ai")
async def analyze_document_type(file: UploadFile = File(...)):
    """
    Belgeyi Gemini AI ile analiz eder.
    Otomatik model seçimi özelliği eklenmiştir.
    """
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))

        # 1. ADIM: Önce Flash modelini standart ismiyle dene
        target_model = 'gemini-1.5-flash'
        
        try:
            model = genai.GenerativeModel(target_model)
            prompt = "Bu belgeyi Türkçe analiz et: Türü, Özeti ve Tarih/Tutar bilgileri."
            response = model.generate_content([prompt, image])
            final_result = response.text
            used_model = target_model

        except Exception as first_error:
            # 2. ADIM: Hata alırsak, mevcut modelleri listele ve çalışan bir tane seç
            print(f"İlk deneme başarısız ({first_error}). Çalışan model aranıyor...")
            
            available_models = []
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    available_models.append(m.name)
            
            # Listede 'flash' veya 'pro' geçen ilk modeli bul
            fallback_model_name = next((m for m in available_models if 'flash' in m), None)
            if not fallback_model_name:
                fallback_model_name = next((m for m in available_models if 'gemini-pro-vision' in m), None)
            
            if not fallback_model_name:
                return {"Hata": "Hiçbir uygun model bulunamadı.", "Liste": available_models}

            print(f"Yedek model devreye girdi: {fallback_model_name}")
            model = genai.GenerativeModel(fallback_model_name)
            response = model.generate_content(["Bu belgeyi analiz et.", image])
            final_result = response.text
            used_model = fallback_model_name

        return {
            "analiz_sonucu": final_result,
            "kullanilan_model": used_model
        }

    except Exception as e:
        return {"Hata": "AI Analizi Kritik Hata", "Detay": str(e)}

# --- BAŞLATMA KODU EN SONDA OLMALI ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)