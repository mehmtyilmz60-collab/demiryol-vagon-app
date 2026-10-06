from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# Geçici Veritabanı
vagon_listesi_db = [
    {"id": 1, "vagon_no": "VAG-101", "giris": "01.10.2026", "kanal": "02.10.2026", "bitis": "-", "durum": "Bakımda", "aciklama": "Tekerlek değişimi"},
    {"id": 2, "vagon_no": "VAG-102", "giris": "03.10.2026", "kanal": "03.10.2026", "bitis": "05.10.2026", "durum": "Tamamlandı", "aciklama": "Fren testi yapıldı"}
]

class VagonModel(BaseModel):
    vagon_no: str
    giris: str
    kanal: Optional[str] = ""
    bitis: Optional[str] = ""
    durum: str
    aciklama: Optional[str] = ""

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
            button { background: #0056b3; color: white; border: none; padding: 12px; border-radius: 8px; font-size: 15px; width: 100%; cursor: pointer; font-weight: bold; margin-bottom: 10px; }
            input, select, textarea { width: 95%; padding: 10px; margin: 5px 0; border-radius: 6px; border: 1px solid #444; background: #333; color: white; font-size: 14px; }
            table { width: 100%; border-collapse: collapse; margin-top: 15px; text-align: left; font-size: 14px; }
            th, td { padding: 10px; border-bottom: 1px solid #444; }
            th { background-color: #333; }
            .status { font-weight: bold; color: #4caf50; }
        </style>
    </head>
    <body>
        <h2>🚆 Demiryol Vagon Takip Sistemi</h2>
        <div class="card">
            <h3>➕ Yeni Vagon Kaydı</h3>
            <input type="text" id="vagon_no" placeholder="Vagon No (Örn: VAG-103)">
            <input type="text" id="giris" placeholder="Giriş Tarihi (Örn: 06.10.2026)">
            <select id="durum">
                <option value="Bekliyor">Bekliyor</option>
                <option value="Bakımda">Bakımda</option>
                <option value="Parça bekliyor">Parça bekliyor</option>
                <option value="Tamamlandı">Tamamlandı</option>
            </select>
            <textarea id="aciklama" placeholder="Açıklama / Bakım Detayı"></textarea>
            <button onclick="vagonEkle()">Kaydet & Ekle</button>
        </div>

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

            async function vagonEkle() {
                let vagon_no = document.getElementById('vagon_no').value;
                let giris = document.getElementById('giris').value;
                let durum = document.getElementById('durum').value;
                let aciklama = document.getElementById('aciklama').value;

                if(!vagon_no || !giris) { alert('Vagon No ve Giriş Tarihi alanlarını doldurun!'); return; }

                let res = await fetch('/api/vagon-ekle', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({vagon_no, giris, durum, aciklama})
                });

                if(res.ok) {
                    alert('Vagon başarıyla eklendi!');
                    document.getElementById('vagon_no').value = '';
                    document.getElementById('aciklama').value = '';
                    verileriGetir();
                }
            }
            verileriGetir();
        </script>
    </body>
    </html>
    """

@app.get("/api/vagonlar")
def vagon_listesi():
    return vagon_listesi_db

@app.post("/api/vagon-ekle")
def vagon_ekle(vagon: VagonModel):
    yeni_id = len(vagon_listesi_db) + 1
    yeni_vagon = {
        "id": yeni_id,
        "vagon_no": vagon.vagon_no,
        "giris": vagon.giris,
        "kanal": vagon.kanal,
        "bitis": vagon.bitis,
        "durum": vagon.durum,
        "aciklama": vagon.aciklama
    }
    vagon_listesi_db.append(yeni_vagon)
    return {"status": "success", "vagon": yeni_vagon}
