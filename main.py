import boto3

# Proje 6: Video Akışı ve İşleme Uygulaması [cite: 28]
# Kullanılan Teknolojiler: Python ve AWS Rekognition [cite: 29, 31, 33]

def video_analiz_baslat(bucket_name, video_file):
    # AWS Rekognition istemcisini başlatıyoruz [cite: 36]
    rekognition = boto3.client('rekognition')
    
    # Videodaki nesneleri tanıma işlemini başlatıyoruz [cite: 39]
    response = rekognition.start_label_detection(
        Video={'S3Object': {'Bucket': bucket_name, 'Name': video_file}}
    )
    
    print(f"Analiz Başlatıldı. JobId: {response['JobId']}")
    return response['JobId']

# S3 bilgilerini buraya gireceğiz
# BUCKET = "senin-bucket-ismin"
# VIDEO = "videonun-adi.mp4"