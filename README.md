# AI Destekli Öğrenme Planlayıcı

Bu proje, kullanıcıların hedeflerine göre kişiselleştirilmiş haftalık öğrenme planları oluşturmalarını sağlar. Yapay zekâ (Gemini) ile desteklenen sistem, her hedef için detaylı alt başlıklar ve tahmini süreler üretir, ayrıca grafikle görselleştirir.

## Özellikler

- Kullanıcı kayıt/giriş sistemi (şifreler hash'li)
- Gemini ile plan üretimi
- Grafik destekli zaman çizelgesi
- Hedef bazlı plan kaydı
- Planları görüntüleme ve silme
- FastAPI + SQLite + Jinja2

## Kurulum

```bash
git clone https://github.com/kullaniciadi/proje-adi.git
cd proje-adi
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Ortam Dosyası

`.env.example` dosyasını `.env` olarak kopyalayın ve kendi API anahtarınızı girin:

```bash
cp .env.example .env
```

## Uygulamayı Başlat

```bash
uvicorn main:app --reload
```

## Lisans

MIT Lisansı
