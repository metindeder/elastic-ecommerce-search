# Elastic E-Commerce Search

Bu proje, **Elasticsearch** ve **FastAPI** kullanarak geliştirilmiş bir e-ticaret arama motoru uygulamasıdır. 

Uygulama, ürünlerin hızlı ve etkili bir şekilde aranabilmesi için Elasticsearch altyapısını kullanır ve sistemin kolayca ayağa kaldırılabilmesi için Docker ile yapılandırılmıştır.

## 🚀 Kullanılan Teknolojiler

<p align="left">
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker Logo" />
  <img src="https://img.shields.io/badge/Elasticsearch-005571?style=for-the-badge&logo=elasticsearch&logoColor=white" alt="Elasticsearch Logo" />
  <img src="https://img.shields.io/badge/Anaconda-44A833?style=for-the-badge&logo=anaconda&logoColor=white" alt="Anaconda Logo" />
</p>

### Projede Yer Alan Diğer Araçlar:
* **FastAPI:** Yüksek performanslı Python web framework'ü.
* **Python 3.10:** Arka uç geliştirme dili.

## 🛠️ Kurulum ve Çalıştırma

Projeyi yerel ortamınızda çalıştırmak için aşağıdaki adımları izleyebilirsiniz:

1. Projeyi bilgisayarınıza indirin ve terminal ile proje dizinine gidin.
2. Aşağıdaki komutu kullanarak konteynerleri oluşturup başlatın:

```bash
docker-compose up --build -d
```

Bu komut çalıştırıldıktan sonra:
* **Elasticsearch** veritabanı servisi `9200` portunda ayağa kalkacaktır.
* **FastAPI** uygulaması `8000` portunda yayına girecektir.

## 🔗 Erişim

Servisler başladıktan sonra aşağıdaki bağlantılardan erişebilirsiniz:

- **API Dokümantasyonu (Swagger UI):** [http://localhost:8000/docs](http://localhost:8000/docs)
- **Elasticsearch Durum Kontrolü:** [http://localhost:9200](http://localhost:9200)
