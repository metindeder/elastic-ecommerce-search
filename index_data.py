from elasticsearch import Elasticsearch, helpers
from faker import Faker
import random

# localhost yerine 127.0.0.1 kullanmak Windows DNS çakışmalarını (IPv6) önler
es = Elasticsearch("http://127.0.0.1:9200")
fake = Faker('tr_TR')  

index_name = "products"

print("Elasticsearch bağlantısı kontrol ediliyor...")
# Bağlantının başarılı olduğunu görmek için sunucu bilgisini ekrana yazdırıyoruz
print(es.info()) 

# exists() metodunun HEAD isteği hatasını bypass etmek için:
# İndeksi silmeyi dene, indeks yoksa (404) veya 400 hatası verirse yoksay
es.options(ignore_status=[400, 404]).indices.delete(index=index_name)

# İndeksi oluştur
es.indices.create(index=index_name)

categories = ["Elektronik", "Giyim", "Ev & Yaşam", "Kitap", "Spor", "Kozmetik"]

print(f"'{index_name}' indeksi oluşturuldu. Sentetik veriler üretiliyor ve indeksleniyor...")

def generate_data():
    for i in range(1, 101): # 100 adet ürün
        yield {
            "_index": index_name,
            "_id": i,
            "_source": {
                "product_name": fake.word().capitalize() + " " + fake.word().capitalize(),
                "category": random.choice(categories),
                "price": round(random.uniform(50.0, 5000.0), 2),
                "description": fake.text(max_nb_chars=200),
                "stock": random.randint(0, 100)
            }
        }

# Verileri Elasticsearch'e toplu olarak gönder
helpers.bulk(es, generate_data())

print(f"Başarıyla 100 adet ürün '{index_name}' indeksine eklendi!")