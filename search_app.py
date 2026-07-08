from elasticsearch import Elasticsearch

es = Elasticsearch("http://127.0.0.1:9200")
index_name = "products"

def search_products(query_text, min_price=None, max_price=None):
    # Temel arama (must) ve filtreleme (filter) işlemlerini birleştiren bool sorgusu
    query = {
        "query": {
            "bool": {
                "must": [
                    {
                        "multi_match": {
                            "query": query_text,
                            "fields": ["product_name^2", "description", "category"],
                            "fuzziness": "AUTO"
                        }
                    }
                ],
                "filter": [] # Filtreleri buraya dinamik olarak ekleyeceğiz
            }
        }
    }

    # Eğer fiyat limitleri girilmişse, 'filter' listesine 'range' (aralık) sorgusu ekliyoruz
    if min_price is not None or max_price is not None:
        price_range = {"range": {"price": {}}}
        if min_price is not None:
            price_range["range"]["price"]["gte"] = min_price # gte: Greater Than or Equal To (Büyük veya Eşit)
        if max_price is not None:
            price_range["range"]["price"]["lte"] = max_price # lte: Less Than or Equal To (Küçük veya Eşit)
        
        query["query"]["bool"]["filter"].append(price_range)

    # Sorguyu çalıştır
    response = es.search(index=index_name, body=query, size=5)
    
    total_hits = response['hits']['total']['value']
    print(f"\n--- Sonuçlar ({total_hits} eşleşme) ---")
    
    for hit in response['hits']['hits']:
        score = hit['_score']
        source = hit['_source']
        print(f"[Skor: {score:.2f}] {source['product_name']} | {source['category']} | Stok: {source['stock']} | Fiyat: {source['price']} TL")

if __name__ == "__main__":
    print("E-Ticaret Gelişmiş Arama Motoru Başlatıldı.")
    while True:
        user_input = input("\nAramak istediğiniz kelime (Çıkmak için 'q' yazın): ")
        if user_input.lower() == 'q':
            print("Çıkış yapılıyor...")
            break
        
        # Kullanıcıdan opsiyonel olarak fiyat aralığı alma
        min_p = input("Minimum fiyat (Filtre yoksa sadece Enter'a basın): ")
        max_p = input("Maksimum fiyat (Filtre yoksa sadece Enter'a basın): ")
        
        # Girdileri ondalıklı sayıya (float) çevir veya boş bırakıldıysa None yap
        min_price = float(min_p) if min_p.strip() else None
        max_price = float(max_p) if max_p.strip() else None
        
        search_products(user_input, min_price, max_price)