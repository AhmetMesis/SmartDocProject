@echo off
TITLE Akilli Dokuman Projesi Yoneticisi
color 0A

echo ========================================================
echo  SMART DOC PROJECT - BASLATILIYOR
echo ========================================================

echo.
echo [ADIM 1] Backend API (Docker) Baslatiliyor...
echo Lutfen acilan diger pencereyi KAPATMAYIN.
echo.

:: Docker'ı .env dosyasıyla başlatır. 
:: --env-file .env komutu sayesinde API anahtarın güvenle içeri aktarılır.
start "Backend API - Docker" cmd /k "docker run --env-file .env -p 8000:8000 smart-doc-api"

echo Backend'in hazir olmasi icin 5 saniye bekleniyor...
timeout /t 5 /nobreak >nul

echo.
echo [ADIM 2] Frontend Arayuz (Streamlit) Baslatiliyor...
echo.

:: Streamlit arayüzünü başlatır.
start "Frontend UI - Streamlit" cmd /k "streamlit run frontend.py"

echo.
echo ========================================================
echo  ISLEM TAMAM!
echo  Tarayiciniz otomatik olarak acilacaktir: http://localhost:8501
echo ========================================================
pause