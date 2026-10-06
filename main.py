from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# Birebir masaüstü veritabanı yapınız
vagonlar_db = [
    {
        "id": 1,
        "vagon_no": "VAG-101",
        "giris_tarihi": "01.10.2026",
        "kanal_tarihi": "02.10.2026",
        "bitis_tarihi": "-",
        "durum": "Bakım devam ediyor",
        "aciklama": "Gebze Vagon Atölyesi - Tekerlek takımı ve rulman değişimi yapılıyor."
    },
    {
        "id": 2,
        "vagon_no": "VAG-102",
        "giris_tarihi": "03.10.2026",
        "kanal_tarihi": "03.10.2026",
        "bitis_tarihi": "05.10.2026",
        "durum": "Tamamlandı",
        "aciklama": "Fren testleri başarıyla tamamlandı, fabrikaya teslime hazır."
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
            /* CustomTkinter Dark Blue Teması */
            body { 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                background-color: #1a1a1a; 
                color: #ffffff; 
                margin: 0; 
                padding: 15px; 
            }
            .main-layout { 
                display: flex; 
                flex-wrap: wrap; 
                gap: 15px; 
                max-width: 1200px; 
                margin: 0 auto; 
            }
            /* Sol Panel - İşlemler & Form */
            .left-panel { 
                flex: 1; 
                min-width: 300px; 
                background-color: #2b2b2b; 
                padding: 15px; 
                border-radius: 10px; 
                box-shadow: 0 4px 10px rgba(0,0,0,0.5); 
            }
            /* Sağ Panel - Tablo */
            .right-panel { 
                flex: 2; 
                min-width: 320px; 
                background-color: #2b2b2b; 
                padding: 15px; 
                border-radius: 10px; 
                box-shadow: 0 4px 10px rgba(0,0,0,0.5); 
            }
            h2, h3 { color: #ffffff; margin-top: 0; }
            label { display: block; font-weight: bold; margin-top: 10px; margin-bottom: 3px; font-size: 12px; color: #cccccc; }
            input, select, textarea { 
                width: 100%; 
                padding: 9px; 
                border-radius: 6px; 
                border: 1px solid #444444; 
                background-color: #1e1e1e; 
                color: #ffffff; 
                box-sizing: border-box; 
                font-size: 13px; 
            }
            textarea { height: 70px; resize: vertical; }
            button { 
                background-color: #1f538d; 
                color: white; 
                border: none; 
                padding: 11px; 
                border-radius: 6px; 
                font-size: 14px; 
                font-weight: bold; 
                width: 100%; 
                cursor: pointer; 
                margin-top: 12px; 
                transition: 0.2s;
            }
            button:hover { background-color: #14375e; }
            .btn-excel { background-color: #2e7d32; }
            .btn-excel:hover { background-color: #1b5e20; }
            /* Treeview / Tablo Stili */
            table { width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 13px; }
            th { background-color: #242424; color: #ffffff; padding: 10px; text-align: center; border-bottom: 2px solid #3a3a3a; }
            td { padding: 10px; text-align: center; border-bottom: 1px solid #333333; }
            tr:nth-child(even) { background-color: #242424; }
            tr:hover { background-color: #333333; cursor: pointer; }
            /* Durum Rozetleri */
            .badge { padding: 4px 8px; border-radius: 4px; font-weight: bold; font-size: 11px; display: inline-block; }
            .status-bekliyor { background: #d97706; color: white; }
            .status-parca { background: #dc2626; color: white; }
            .status-bakim { background: #2563eb; color: white; }
            .status-tamam { background: #16a34a; color: white; }
        </style>
    </head>
    <body>
        <h2 style="text-align:center;">🚆 Vagon Bakım Takip Sistemi</h2>
        
        <div class="main-layout">
            <!-- Sol Panel (İşlemler & Form) -->
            <div class="left-panel">
                <h3>İşlemler</h3>
                
                <label>Vagon No</label>
                <input type="text" id="vagon_no" placeholder="Örn: VAG-103">

                <label>Atölye Giriş</label>
                <input type="text" id="giris_tarihi" value="06.10.2026">

                <label>Kanala Alınma</label>
                <input type="text" id="kanal_tarihi" placeholder="Örn: 06.10.2026">

                <label>İş Bitiş / Fabrika Sevk</label>
                <input type="text" id="bitis_tarihi" placeholder="Örn: 08.10.2026">

                <label>Durum</label>
                <select id="durum">
                    <option value="Bekliyor">Bekliyor</option>
                    <option value="Parça bekliyor">Parça bekliyor</option>
                    <option value="Bakım devam ediyor">Bakım devam ediyor</option>
                    <option value="Tamamlandı">Tamamlandı</option>
                </select>

                <label>Açıklama / Fabrika & Atölye Notu</label>
                <textarea id="aciklama" placeholder="Gelen/giden fabrika bilgileri, parça durumu ve bakım detayları..."></textarea>

                <button onclick="kaydet()">💾 Kaydet</button>
            </div>

            <!-- Sağ Panel (Tablo & Liste) -->
            <div class="right-panel">
                <div style="display:flex; gap:10px;">
                    <button onclick="verileriYukle()">🔄 Listeyi Yenile</button>
                    <button class="btn-excel" onclick="alert('Excel raporu indiriliyor...')">📊 Excel Rapor</button>
                </div>

                <div style="overflow-x:auto;">
                    <table>
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

                    bodyHtml += `<tr onclick="detayGoster('${item.vagon_no}', '${item.aciklama}')">
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
                    alert('Vagon kaydı ve fabrika bilgisi kaydedildi!');
                    document.getElementById('vagon_no').value = '';
                    document.getElementById('aciklama').value = '';
                    verileriYukle();
                }
            }

            function detayGoster(vagonNo, aciklama) {
                alert("🚆 Vagon No: " + vagonNo + "\\n\\n📝 Fabrika & Açıklama Notu:\\n" + aciklama);
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
