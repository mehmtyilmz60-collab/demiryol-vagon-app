from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# Masaüstü SQLite yapınızla birebir aynı veritabanı modeli
vagonlar_db = [
    {
        "id": 1,
        "vagon_no": "VAG-101",
        "giris_tarihi": "01.10.2026",
        "kanal_tarihi": "02.10.2026",
        "bitis_tarihi": "-",
        "durum": "Bakım devam ediyor",
        "aciklama": "Tekerlek takımı ve rulman değişimi yapılıyor."
    },
    {
        "id": 2,
        "vagon_no": "VAG-102",
        "giris_tarihi": "03.10.2026",
        "kanal_tarihi": "03.10.2026",
        "bitis_tarihi": "05.10.2026",
        "durum": "Tamamlandı",
        "aciklama": "Fren testleri tamamlandı, teslime hazır."
    }
]

class VagonModel(BaseModel):
    vagon_no: str
    giris_tarihi: str
    kanal_tarihi: Optional[str] = ""
    bitis_tarihi: Optional[str] = ""
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
        <title>Vagon Bakım Takip Sistemi</title>
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #1e1e1e; color: #ffffff; margin: 0; padding: 15px; }
            h2 { text-align: center; color: #ffffff; margin-bottom: 20px; }
            .container { max-width: 600px; margin: 0 auto; background: #2a2a2a; padding: 20px; border-radius: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.4); }
            label { display: block; font-weight: bold; margin-top: 10px; margin-bottom: 4px; font-size: 13px; color: #dddddd; }
            input, select, textarea { width: 100%; padding: 10px; border-radius: 6px; border: 1px solid #444; background-color: #1e1e1e; color: #fff; box-sizing: border-box; font-size: 14px; }
            textarea { height: 80px; resize: vertical; }
            button { background-color: #2a72d4; color: white; border: none; padding: 12px; border-radius: 6px; font-size: 15px; font-weight: bold; width: 100%; cursor: pointer; margin-top: 15px; }
            button:hover { background-color: #1b5bb8; }
            .btn-refresh { background-color: #444444; margin-bottom: 15px; }
            .btn-refresh:hover { background-color: #555555; }
            table { width: 100%; border-collapse: collapse; margin-top: 15px; font-size: 13px; }
            th { background-color: #2a2a2a; color: #ffffff; padding: 10px; text-align: center; border-bottom: 2px solid #444; }
            td { padding: 10px; text-align: center; border-bottom: 1px solid #333; }
            tr:nth-child(even) { background-color: #242424; }
            .badge { padding: 4px 8px; border-radius: 4px; font-weight: bold; font-size: 11px; }
            .status-bekliyor { background: #d97706; color: white; }
            .status-parca { background: #dc2626; color: white; }
            .status-bakim { background: #2563eb; color: white; }
            .status-tamam { background: #16a34a; color: white; }
        </style>
    </head>
    <body>
        <h2>🚆 Vagon Bakım Takip Sistemi</h2>
        
        <div class="container">
            <h3>➕ Yeni Vagon Ekle</h3>
            
            <label>Vagon No</label>
            <input type="text" id="vagon_no" placeholder="Örn: VAG-103">

            <label>Atölye Giriş</label>
            <input type="text" id="giris_tarihi" value="06.10.2026">

            <label>Kanala Alınma</label>
            <input type="text" id="kanal_tarihi" placeholder="Örn: 06.10.2026">

            <label>İş Bitiş</label>
            <input type="text" id="bitis_tarihi" placeholder="Örn: 08.10.2026">

            <label>Durum</label>
            <select id="durum">
                <option value="Bekliyor">Bekliyor</option>
                <option value="Parça bekliyor">Parça bekliyor</option>
                <option value="Bakım devam ediyor">Bakım devam ediyor</option>
                <option value="Tamamlandı">Tamamlandı</option>
            </select>

            <label>Açıklama</label>
            <textarea id="aciklama" placeholder="Bakım ve arıza detaylarını giriniz..."></textarea>

            <button onclick="kaydet()">💾 Kaydet</button>
        </div>

        <br>

        <div class="container">
            <button class="btn-refresh" onclick="verileriYukle()">🔄 Listeyi Yenile</button>
            <div style="overflow-x:auto;">
                <table id="vagonTable">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Vagon</th>
                            <th>Giriş</th>
                            <th>Kanal</th>
                            <th>Bitiş</th>
                            <th>Durum</th>
                        </tr>
                    </thead>
                    <tbody id="vagonBody"></tbody>
                </table>
            </div>
        </div>

        <script>
            async function verileriYukle() {
                let res = await fetch('/api/vagonlar');
                let data = await res.json();
                let bodyHtml = '';
                
                data.forEach(item => {
                    let badgeClass = 'status-bekliyor';
                    if(item.durum === 'Parça bekliyor') badgeClass = 'status-parca';
                    if(item.durum === 'Bakım devam ediyor') badgeClass = 'status-bakim';
                    if(item.durum === 'Tamamlandı') badgeClass = 'status-tamam';

                    bodyHtml += `<tr>
                        <td>${item.id}</td>
                        <td><b>${item.vagon_no}</b></td>
                        <td>${item.giris_tarihi || '-'}</td>
                        <td>${item.kanal_tarihi || '-'}</td>
                        <td>${item.bitis_tarihi || '-'}</td>
                        <td><span class="badge ${badgeClass}">${item.durum}</span></td>
                    </tr>`;
                });
                document.getElementById('vagonBody').innerHTML = bodyHtml;
            }

            async function kaydet() {
                let vagon_no = document.getElementById('vagon_no').value;
                let giris_tarihi = document.getElementById('giris_tarihi').value;
                let kanal_tarihi = document.getElementById('kanal_tarihi').value;
                let bitis_tarihi = document.getElementById('bitis_tarihi').value;
                let durum = document.getElementById('durum').value;
                let aciklama = document.getElementById('aciklama').value;

                if(!vagon_no) { alert('Vagon No boş bırakılamaz!'); return; }

                let res = await fetch('/api/vagon-ekle', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({vagon_no, giris_tarihi, kanal_tarihi, bitis_tarihi, durum, aciklama})
                });

                if(res.ok) {
                    alert('Vagon başarıyla kaydedildi!');
                    document.getElementById('vagon_no').value = '';
                    document.getElementById('aciklama').value = '';
                    verileriYukle();
                }
            }

            verileriYukle();
        </script>
    </body>
    </html>
    """

@app.get("/api/vagonlar")
def vagon_listesi():
    return vagonlar_db

@app.post("/api/vagon-ekle")
def vagon_ekle(vagon: VagonModel):
    yeni_id = len(vagonlar_db) + 1
    yeni_vagon = {
        "id": yeni_id,
        "vagon_no": vagon.vagon_no,
        "giris_tarihi": vagon.giris_tarihi,
        "kanal_tarihi": vagon.kanal_tarihi,
        "bitis_tarihi": vagon.bitis_tarihi,
        "durum": vagon.durum,
        "aciklama": vagon.aciklama
    }
    vagonlar_db.append(yeni_vagon)
    return {"status": "success", "vagon": yeni_vagon}
