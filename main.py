from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

# Geçici veri depolama (Mobil ve Masaüstü ortak görür)
vagon_listesi_db = [
    {"id": 1, "vagon_no": "VAG-101", "giris": "01.10.2026", "kanal": "02.10.2026", "bitis": "-", "durum": "Bakımda", "aciklama": "Tekerlek değişimi"},
    {"id": 2, "vagon_no": "VAG-102", "giris": "03.10.2026", "kanal": "03.10.2026", "bitis": "05.10.2026", "durum": "Tamamlandı", "aciklama": "Fren testi yapıldı"}
]

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Demiryol Vagon Takip Sistemi</title>
        <style>
            body { font-family: sans-serif; background: #1e1e1e; color: white; text-align: center; padding: 15px; margin: 0; }
            .card { background: #2a2a2a; padding: 15px; border-radius: 12px; max-width: 500px; margin: 15px auto; box-shadow: 0 4px 10px rgba(0,0,0,0.5); }
            button { background: #0056b3; color: white; border: none; padding: 12px; border-radius: 8px; font-size: 16px; width: 100%; cursor: pointer; font-weight: bold; }
            table { width: 100%; border-collapse: collapse; margin-top: 15px; text-align: left; font-size: 14px; }
            th, td { padding: 10px; border-bottom: 1px solid #444; }
            th { background-color: #333; }
            .status { font-weight: bold; color: #4caf50; }
        </style>
    </head>
    <body>
        <h2>🚆 Demiryol Vagon Takip Sistemi</h2>
        <div class="card">
            <button onclick="verileriGetir()">🔄 Vagon Listesini Yenile</button>
            <div id="sonuc"></div>
        </div>
        <script>
            async function verileriGetir() {
                let res = await fetch('/api/vagonlar');
                let data = await res.json();
                let html = '<table><tr><th>Vagon No</th><th>Giriş</th><th>Durum</th></tr>';
                data.forEach(item => {
                    html += `<tr><td><b>${item.vagon_no}</b></td><td>${item.giris}</td><td class="status">${item.durum}</td></tr>`;
                });
                html += '</table>';
                document.getElementById('sonuc').innerHTML = html;
            }
            verileriGetir();
        </script>
    </body>
    </html>
    """

@app.get("/api/vagonlar")
def vagon_listesi():
    return vagon_listesi_db
