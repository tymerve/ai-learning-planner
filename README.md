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

pip install -r requirements.txt

## Ortam Dosyası

`.env.example` dosyasını `.env` olarak kopyalayın ve kendi API anahtarınızı girin



## Uygulamayı Başlat

```bash
uvicorn main:app --reload
```

## Lisans

MIT Lisansı
