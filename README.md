# Proje 6: Video Akışı ve İşleme Uygulaması (AWS Rekognition)

Bu proje, AWS Rekognition kullanarak AWS S3'te bulunan videoların içerisindeki nesneleri tanıyan ve listeleyen modüler bir Python uygulamasıdır.

## Özellikler
- **AWS Rekognition Entegrasyonu:** `start_label_detection` ve `get_label_detection` API'leri ile video analizi.
- **Nesne Yönelimli Tasarım (OOP):** `VideoAnalyzer` sınıfı sayesinde yeniden kullanılabilir ve modüler kod yapısı.
- **Hata Yönetimi ve Loglama:** Olası hatalara karşı `try-except` yapıları ile donatılmış ve süreci adım adım terminale yazdıran loglama altyapısı.
- **Otomatik Sonuç Kontrolü:** İşlem tamamlanana kadar (status `SUCCEEDED` olana kadar) bekleyen ve tamamlandığında sonuçları formatlı şekilde ekrana basan algoritma.

## Gereksinimler
- Python 3.x
- AWS Hesabı ve yapılandırılmış AWS CLI (`aws configure`)
- Amazon S3 üzerinde bir bucket ve yüklenmiş bir video dosyası

Gerekli Python paketlerini kurmak için:
```bash
pip install -r requirements.txt
```

## Kullanım
`main.py` dosyası içindeki şu sabitleri kendi ortamınıza göre güncelleyin:
- `BUCKET`: Videonun bulunduğu S3 Bucket adı
- `VIDEO`: S3 Bucket içindeki video dosyasının tam adı (örn: `cloud analiz.mp4`)
- `REGION`: S3 Bucket'ının ve Rekognition'ın çalışacağı AWS bölgesi (örn: `eu-west-1`)

Daha sonra scripti çalıştırın:
```bash
python main.py
```
Uygulama, videodaki nesneleri algılayıp size güven oranı ve göründükleri zaman dilimiyle birlikte raporlayacaktır.