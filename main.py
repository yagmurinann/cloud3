import boto3
import time
import logging
from botocore.exceptions import ClientError

# Log ayarları
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class VideoAnalyzer:
    """
    AWS Rekognition kullanarak video analiz işlemlerini yürüten modüler sınıf.
    """
    def __init__(self, region_name='eu-west-1'):
        try:
            self.rekognition = boto3.client('rekognition', region_name=region_name)
            logging.info(f"Rekognition istemcisi başlatıldı. Bölge: {region_name}")
        except Exception as e:
            logging.error(f"Rekognition istemcisi başlatılamadı: {e}")
            raise

    def start_label_detection(self, bucket_name, video_file):
        """
        Videodaki nesneleri tanıma işlemini başlatır ve JobId döndürür.
        """
        try:
            response = self.rekognition.start_label_detection(
                Video={'S3Object': {'Bucket': bucket_name, 'Name': video_file}},
                MinConfidence=70 # %70 ve üzeri güvenilirlikteki nesneleri getir
            )
            job_id = response['JobId']
            logging.info(f"Analiz Başlatıldı. JobId: {job_id}")
            return job_id
        except ClientError as e:
            logging.error(f"Analiz başlatılırken AWS hatası oluştu: {e}")
            return None
        except Exception as e:
            logging.error(f"Beklenmeyen bir hata oluştu: {e}")
            return None

    def wait_for_completion(self, job_id, check_interval=5):
        """
        Analiz işleminin tamamlanmasını bekler. Durum 'SUCCEEDED' olana kadar döngüde kalır.
        """
        logging.info(f"İşlemin tamamlanması bekleniyor... JobId: {job_id}")
        while True:
            try:
                response = self.rekognition.get_label_detection(JobId=job_id, MaxResults=1)
                status = response['JobStatus']
                
                if status == 'IN_PROGRESS':
                    logging.info("Analiz devam ediyor, lütfen bekleyin...")
                    time.sleep(check_interval)
                elif status == 'SUCCEEDED':
                    logging.info("Analiz başarıyla tamamlandı!")
                    return True
                elif status == 'FAILED':
                    error_message = response.get('StatusMessage', 'Bilinmeyen Hata')
                    logging.error(f"Analiz başarısız oldu. Neden: {error_message}")
                    return False
            except ClientError as e:
                logging.error(f"Durum kontrolü sırasında AWS hatası: {e}")
                return False

    def get_results(self, job_id, max_results=10):
        """
        Tamamlanmış analizin sonuçlarını alır ve ekrana okunabilir formatta yazdırır.
        """
        logging.info("Sonuçlar getiriliyor...")
        try:
            response = self.rekognition.get_label_detection(
                JobId=job_id, 
                MaxResults=max_results, 
                SortBy='TIMESTAMP' # Zamana göre sırala
            )
            
            labels = response.get('Labels', [])
            if not labels:
                logging.info("Videoda herhangi bir etiket (nesne) bulunamadı.")
                return

            print("\n" + "="*40)
            print("         ANALİZ SONUÇLARI")
            print("="*40)
            for label in labels:
                name = label['Label']['Name']
                confidence = label['Label']['Confidence']
                timestamp = label['Timestamp']
                
                # Saniye cinsinden zaman damgası
                seconds = timestamp / 1000.0 
                
                print(f"[{seconds:.2f} sn] Nesne: {name:<15} (Güven: %{confidence:.2f})")
            print("="*40 + "\n")
            
        except ClientError as e:
            logging.error(f"Sonuçlar alınırken hata oluştu: {e}")


def main():
    # Proje ayarları
    BUCKET = "cloud-video-analizi-euw1"
    VIDEO = "cloud analiz.mp4"
    REGION = "eu-west-1"

    # 1. Modüler yapıyı (sınıfı) kullanarak nesne oluşturuyoruz
    analyzer = VideoAnalyzer(region_name=REGION)

    # 2. Analizi Başlat
    job_id = analyzer.start_label_detection(BUCKET, VIDEO)
    if not job_id:
        logging.error("JobId alınamadığı için işlem sonlandırılıyor.")
        return

    # 3. Analizin bitmesini bekle
    is_success = analyzer.wait_for_completion(job_id, check_interval=5)
    
    # 4. Başarılıysa sonuçları ekrana bas
    if is_success:
        analyzer.get_results(job_id, max_results=15)

if __name__ == "__main__":
    main()