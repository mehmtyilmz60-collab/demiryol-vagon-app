from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Demiryol Vagon Mobil</title>
        <style>
            body { font-family: sans-serif; background: #eef2f5; text-align: center; padding: 20px; }
            .card { background: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); max-width: 400px; margin: 20px auto; }
            button { background: #0056b3; color: white; border: none; padding: 12px 20px; border-radius: 8px; font-size: 16px; width: 100%; cursor: pointer; }
            ul { text-align: left; padding-left: 20px; }
        </style>
    </head>
    <body>
        <h2>🚆 Demiryol Vagon Mobil Panel</h2>
        <div class="card">
            <h3>Saha & Atölye Takip</h3>
            <button onclick="verileriGetir()">Vagon Durumlarını Yükle</button>
            <div id="sonuc" style="margin-top:15px;"></div>
        </div>
        <script>
            async function verileriGetir() {
                let res = await fetch('/api/vagonlar');
                let data = await res.json();
                let html = '<ul>';
                data.forEach(item => {
                    html += `<li><b>${item.vagon_id}</b> - ${item.durum} (${item.lokasyon})</li>`;
                });
                html += '</ul>';
                document.getElementById('sonuc').innerHTML = html;
            }
        </script>
    </body>
    </html>
    """

@app.get("/api/vagonlar")
def vagon_listesi():
    return [
        {"vagon_id": "VAG-101", "durum": "Bakımda", "lokasyon": "Gebze Vagon Atölyesi"},
        {"vagon_id": "VAG-102", "durum": "Faal", "lokasyon": "Darıca Tesisleri"}
    ]