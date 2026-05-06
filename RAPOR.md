# PROJE 6: Video Akışı ve İşleme Uygulaması Proje Raporu

**Öğrenci Adı/Soyadı:** Yağmur İNAN
**Öğrenci Numarası:** 23291519
**Ders:** Bulut Bilişim 

---

## 1. Projenin Amacı
Projenin temel amacı, Amazon Web Services (AWS) bulut altyapısı kullanılarak video dosyaları içerisindeki nesnelerin otomatik olarak tanınmasını (Computer Vision / Object Detection) sağlamaktır. Bu kapsamda, AWS S3 depolama servisi ve AWS Rekognition makine öğrenimi servisi entegre edilerek Python programlama diliyle modüler ve hataya dayanıklı bir uygulama geliştirilmiştir.

## 2. Kullanılan Teknolojiler
- **Python 3.x:** Uygulamanın temel geliştirme dili olarak kullanılmıştır.
- **Boto3 (AWS SDK for Python):** Python uygulamasının AWS servisleriyle (S3, Rekognition) API üzerinden güvenli bir şekilde iletişim kurmasını sağlayan resmi kütüphanedir.
- **AWS S3 (Simple Storage Service):** Analiz edilecek `.mp4` formatındaki büyük boyutlu video dosyalarının bulutta depolanması için kullanılmıştır.
- **AWS Rekognition:** Yüklenen video dosyasını asenkron olarak işleyip içerisindeki nesneleri, etiketleri ve bu nesnelere ait güven (confidence) oranlarını analiz eden derin öğrenme tabanlı AWS servisidir.

## 3. Sistem Mimarisi ve İş Akışı
Uygulama çalıştırıldığında sistem aşağıdaki iş akışını (workflow) izler:

1. **Veri Depolama:** Önceden analiz edilecek olan video (`cloud analiz.mp4`), AWS S3 bucket'ına (`cloud-video-analizi-euw1`) yüklenmiştir.
2. **Analizin Tetiklenmesi (`start_label_detection`):** Uygulama, `boto3` aracılığıyla AWS Rekognition API'sini çağırır ve nesne tanıma (Label Detection) işini başlatır. Rekognition bu işlemi arka planda asenkron yürüttüğü için uygulamaya bir `JobId` (Görev Kimliği) döndürür.
3. **Durum Kontrolü (Polling):** Uygulama, dönen `JobId` bilgisini kullanarak `get_label_detection` metodunu çağırır. Görev durumu `IN_PROGRESS` olduğu sürece 5 saniyede bir kontrol (polling) yapar. Durum `SUCCEEDED` (Başarılı) veya `FAILED` (Başarısız) olana kadar bekler.
4. **Sonuçların Alınması ve İşlenmesi:** İşlem başarıyla tamamlandığında (SUCCEEDED), uygulamanın `get_results` fonksiyonu çalışır. Tespit edilen nesnelerin isimleri, %70 ve üzeri güven oranları ve videonun hangi saniyesinde göründükleri (timestamp) düzenli bir formatta konsola yazdırılır.

## 4. Kodun Yapısı ve Yazılım Geliştirme Pratikleri
Geliştirilen uygulama (`main.py`), "Clean Code" prensiplerine ve Nesne Yönelimli Programlama (OOP) mantığına uygun tasarlanmıştır:

- **`VideoAnalyzer` Sınıfı:** Kod tekrarlarını önlemek ve farklı modüllerde kolayca kullanılabilmesi için tüm AWS Rekognition bağlantıları, başlatma ve sonuç getirme fonksiyonları tek bir sınıf (`Class`) altında kapsüllenmiştir (Encapsulation).
- **Hata Yönetimi (Exception Handling):** Ağ kopmaları, yetki eksikliği veya yanlış AWS konfigürasyonları gibi durumlara karşı `try-except` blokları eklenmiştir. Özellikle AWS'ye özel hataları yakalamak için `botocore.exceptions.ClientError` sınıfı kullanılarak sistemin aniden çökmesi engellenmiştir.
- **Loglama Mekanizması:** Konsola yazdırılacak bilgi, uyarı ve hata mesajları, Python'ın standart `logging` kütüphanesi kullanılarak zaman damgalı ve profesyonel bir formatta verilmiştir.

## 5. Karşılaşılan Zorluklar ve Geliştirilen Çözümler
Uygulama geliştirilirken karşılaşılan en büyük teknik zorluk ve çözümü şu şekildedir:

- **Zorluk - Bölge (Region) Uyumsuzluğu:** İlk aşamada AWS CLI varsayılan bölgesi `eu-north-1` (Stockholm) olarak ayarlıyken, bu bölgede AWS Rekognition servisinin tam destek sunmaması sebebiyle `EndpointConnectionError` alındı. Rekognition bölgesi `eu-west-1` (İrlanda) olarak düzeltildiğinde ise S3 bucket'ı (Stockholm'de kaldığı için) `InvalidS3ObjectException` hatası verdi. Çünkü AWS Rekognition, analiz edeceği S3 verisinin kendiyle **aynı bölgede** olmasını zorunlu kılmaktadır.
- **Çözüm:** AWS CLI kullanılarak `eu-west-1` bölgesinde `cloud-video-analizi-euw1` adında yeni bir S3 bucket oluşturuldu. Video bu bucket'a kopyalandı ve `main.py` üzerindeki konfigürasyon bu yeni mimariye göre güncellenerek senkronizasyon problemi giderildi.

## 6. Proje Çıktıları ve Sonuç
Proje başarıyla tamamlanmış, tüm hatalar giderilmiş ve modüler yapıya kavuşturulmuştur. Sistemin örnek çıktı formatı şu şekildedir:

```text
2026-05-07 00:12:40,825 - INFO - Analiz Başlatıldı. JobId: 91d1fa1a...
2026-05-07 00:12:45,991 - INFO - Analiz devam ediyor, lütfen bekleyin...
2026-05-07 00:12:56,199 - INFO - Analiz başarıyla tamamlandı!
2026-05-07 00:12:56,199 - INFO - Sonuçlar getiriliyor...

========================================
         ANALİZ SONUÇLARI
========================================
[0.00 sn] Nesne: Architecture    (Güven: %100.00)
[0.00 sn] Nesne: Building        (Güven: %100.00)
[0.00 sn] Nesne: Cityscape       (Güven: %100.00)
[0.50 sn] Nesne: Horizon         (Güven: %100.00)
========================================
```

Bu proje çalışması sayesinde, bulut bilişim hizmetlerinin (AWS) gerçek dünya senaryolarında (Görüntü İşleme / Computer Vision) nasıl entegre edileceği, arka plan süreçlerinin asenkron olarak nasıl yönetileceği ve temiz yazılım mimarisi oluşturma teknikleri uygulamalı olarak deneyimlenmiştir.
