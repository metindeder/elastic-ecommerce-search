import os
from fastapi import FastAPI, Query
from elasticsearch import Elasticsearch
from typing import Optional

app = FastAPI(
    title="Gelişmiş E-Ticaret Arama API", 
    description="Gruplama, Sıralama ve Sayfalama destekli Elasticsearch Mikroservisi"
)

# Docker compose ağında çalışırken servis adına (http://elasticsearch:9200) bağlanacağız.
# Eğer lokalde çalıştırırsak otomatik olarak http://127.0.0.1:9200 adresine düşecek.
ES_HOST = os.getenv("ELASTICSEARCH_HOST", "http://127.0.0.1:9200")
es = Elasticsearch(ES_HOST)
index_name = "products"

@app.get("/search")
def search_products(
    q: Optional[str] = Query(None, description="Aranacak kelime"),
    category: Optional[str] = Query(None, description="Kategori filtresi (Tam eşleşme)"),
    min_price: Optional[float] = Query(None, description="Minimum fiyat"),
    max_price: Optional[float] = Query(None, description="Maksimum fiyat"),
    sort_by: Optional[str] = Query("score", description="Sıralama kriteri: score, price_asc, price_desc"),
    page: int = Query(1, ge=1, description="Sayfa numarası"),
    size: int = Query(10, ge=1, le=50, description="Sayfa başına ürün sayısı")
):
    # Sayfalama hesabı (Elasticsearch 'from' parametresi sıfırdan başlar)
    from_offset = (page - 1) * size

    # Temel bool sorgu yapısı
    query = {
        "query": {
            "bool": {
                "must": [],
                "filter": []
            }
        },
        # Kümeleme (Aggregations): Sonuçlardaki ürünlerin kategorilerine göre dağılım sayısını verir
        "aggs": {
            "categories_count": {
                "terms": {
                    "field": "category.keyword" # Metin alanlarında gruplama için .keyword kullanılır
                }
            }
        },
        "from": from_offset,
        "size": size
    }

    # Kelime araması varsa ekle, yoksa tüm ürünleri getir (match_all)
    if q:
        query["query"]["bool"]["must"].append({
            "multi_match": {
                "query": q,
                "fields": ["product_name^2", "description", "category"],
                "fuzziness": "AUTO"
            }
        })
    else:
        query["query"]["bool"]["must"].append({"match_all": {}})

    # Kategori filtresi (Tam Eşleşme)
    if category:
        query["query"]["bool"]["filter"].append({"term": {"category.keyword": category}})

    # Fiyat Aralığı Filtresi
    if min_price is not None or max_price is not None:
        price_range = {"range": {"price": {}}}
        if min_price is not None:
            price_range["range"]["price"]["gte"] = min_price
        if max_price is not None:
            price_range["range"]["price"]["lte"] = max_price
        query["query"]["bool"]["filter"].append(price_range)

    # Sıralama Mantığı
    if sort_by == "price_asc":
        query["sort"] = [{"price": {"order": "asc"}}]
    elif sort_by == "price_desc":
        query["sort"] = [{"price": {"order": "desc"}}]
    else:
        query["sort"] = [{"_score": {"order": "desc"}}] # Varsayılan: Alaka düzeyine göre en yüksekten en düşüğe

    # Elasticsearch sorgusunu çalıştır
    response = es.search(index=index_name, body=query)

    # Sonuçları ayrıştır
    results = [{"score": hit["_score"], "product": hit["_source"]} for hit in response["hits"]["hits"]]
    
    # Gruplama istatistiklerini ayrıştır (Sol menü filtre sayıları)
    category_buckets = response["aggregations"]["categories_count"]["buckets"]
    aggregations = {bucket["key"]: bucket["doc_count"] for bucket in category_buckets}

    return {
        "total_hits": response["hits"]["total"]["value"],
        "current_page": page,
        "size": size,
        "aggregations": aggregations,
        "results": results
    }