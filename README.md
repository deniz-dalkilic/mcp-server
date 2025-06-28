# MCP Local Server

**MCP Local Server** — Model Context Protocol (MCP) standardına uygun, lokal Docker ortamında çalıştırılabilir bir JSON-RPC sunucusudur. Akademik makaleleri CrossRef üzerinden sorgulayan örnek `scholar.search_articles` aracını içerir.

---

## 🚀 Hızlı Başlangıç

1. **Klonlayın**

   ```bash
   git clone https://github.com/your-org/mcp-server.git
   cd mcp-server
   ```

2. **Bağımlılıkları yükleyin (opsiyonel)**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Docker Compose ile çalıştırın**

   ```bash
   docker compose up --build
   ```

4. **Sağlık kontrolü**

   * `GET http://localhost:8000/health`
   * Dönen: `{ "status": "ok" }`

5. **JSON-RPC ile makale arama**
   Postman koleksiyonumuzu import edin veya CURL ile test edin:

   ```bash
   curl -X POST http://localhost:8000/rpc \
     -H "Content-Type: application/json" \
     -d '{
       "jsonrpc": "2.0",
       "id": 1,
       "method": "scholar.search_articles",
       "params": {"query": "analytical chemistry", "max_results": 3}
     }'
   ```

---

## 📦 Proje Yapısı

```
mcp-server/
├── app/
│   ├── main.py          # FastAPI + JSON-RPC endpoint
│   └── tools/
│       └── scholar_tool.py  # CrossRef sorgu aracı
├── config/
│   └── tools.yaml       # Aktif araçlar ve konfigürasyon
├── tests/               # Birim ve entegrasyon testleri
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
├── LICENSE
└── .pre-commit-config.yaml
```

---

## 🛠️ Özellikler

* **JSON-RPC 2.0** uyumlu `/rpc` endpoint
* **FastAPI** altyapısı, asgari bağımlılıklar
* **CrossRef** REST API ile akademik makale arama
* **Modüler tasarım**: yeni araçlar kolayca eklenebilir
* **Docker & Docker Compose** desteği
* **Örnek Postman koleksiyonu** (README altında link verilmiş)

---

## 📋 Postman Kullanımı

1. `mcp-local-server.postman_collection.json` dosyasını indir.
2. Postman → **Import** → Dosyayı seçin.
3. İstekleri göndererek `/health` ve `/rpc` uç noktalarını deneyin.

---

## 📄 Lisans

Bu proje MIT Lisansı ile lisanslanmıştır. DETAYLAR için [LICENSE](./LICENSE) dosyasına bakın.
