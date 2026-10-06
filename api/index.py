from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

app = FastAPI()

# Örnek Veritabanı Yapısı
vagonlar_db = [
    {
        "id": 1,
        "vagon_no": "VAG-101",
        "giris_tarihi": "01.10.2026 08:00",
        "kanal_tarihi": "02.10.2026 10:00",
        "bitis_tarihi": "05.10.2026 16:00",
        "personel_sayisi": 3,
        "durum": "Tamamlandı",
        "aciklama": "Gebze Vagon Atölyesi - Tekerlek takımı ve rulman değişimi yapıldı.",
        "gecmis": [
            "01.10.2026 08:00 - Atölyeye giriş yaptı.",
            "02.10.2026 10:00 - Kanala alındı.",
            "05.10.2026 16:00 - Bakım tamamlandı. (312 Adam-Saat)"
        ]
    },
    {
        "id": 2,
        "vagon_no": "VAG-102",
        "giris_tarihi": "03.10.2026 09:00",
        "kanal_tarihi": "03.10.2026 11:00",
        "bitis_tarihi": "-",
        "personel_sayisi": 2,
        "durum": "Bakım devam ediyor",
        "aciklama": "Fren donanımları ve hava hortumları kontrol ediliyor.",
        "gecmis": [
            "03.10.2026 09:00 - Atölyeye giriş yaptı.",
            "03.10.2026 11:00 - Kanala alındı. Bakım devam ediyor."
        ]
    }
]

class VagonModel(BaseModel):
    vagon_no: str
    giris_tarihi: str
    kanal_tarihi: Optional[str] = ""
    bitis_tarihi: Optional[str] = ""
    personel_sayisi: Optional[int] = 1
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
        <title>Demiryol Vagon Takip & Adam-Saat</title>
        <style>
            /* CustomTkinter Dark-Blue Teması */
            body { 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                background-color: #1a1a1a; 
                color: #ffffff; 
                margin: 0; 
                padding: 15px; 
            }
            .header { 
                display: flex; 
                align-items: center; 
                justify-content: center; 
                gap: 15px; 
                margin-bottom: 20px; 
            }
            .logo-img { 
                height: 55px; 
                width: auto; 
                border-radius: 6px; 
                object-fit: contain;
            }
            .main-layout { 
                display: flex; 
                flex-wrap: wrap; 
                gap: 15px; 
                max-width: 1200px; 
                margin: 0 auto; 
            }
            .left-panel, .right-panel { 
                background-color: #2b2b2b; 
                padding: 15px; 
                border-radius: 10px; 
                box-shadow: 0 4px 10px rgba(0,0,0,0.5); 
            }
            .left-panel { flex: 1; min-width: 300px; }
            .right-panel { flex: 2; min-width: 320px; }
            h2, h3 { color: #ffffff; margin-top: 0; }
            label { display: block; font-weight: bold; margin-top: 8px; margin-bottom: 3px; font-size: 12px; color: #cccccc; }
            input, select, textarea { 
                width: 100%; 
                padding: 8px; 
                border-radius: 6px; 
                border: 1px solid #444; 
                background-color: #1e1e1e; 
                color: #fff; 
                box-sizing: border-box; 
                font-size: 13px; 
            }
            textarea { height: 60px; resize: vertical; }
            button { 
                background-color: #1f538d; 
                color: white; 
                border: none; 
                padding: 10px; 
                border-radius: 6px; 
                font-size: 14px; 
                font-weight: bold; 
                width: 100%; 
                cursor: pointer; 
                margin-top: 10px; 
                transition: 0.2s;
            }
            button:hover { background-color: #14375e; }
            .btn-excel { background-color: #2e7d32; }
            .btn-excel:hover { background-color: #1b5e20; }
            table { width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 12px; }
            th { background-color: #242424; color: #ffffff; padding: 8px; text-align: center; border-bottom: 2px solid #3a3a3a; }
            td { padding: 8px; text-align: center; border-bottom: 1px solid #333; }
            tr:nth-child(even) { background-color: #242424; }
            tr:hover { background-color: #333; cursor: pointer; }
            .badge { padding: 3px 6px; border-radius: 4px; font-weight: bold; font-size: 10px; display: inline-block; }
            .status-bekliyor { background: #d97706; color: white; }
            .status-parca { background: #dc2626; color: white; }
            .status-bakim { background: #2563eb; color: white; }
            .status-tamam { background: #16a34a; color: white; }
            .adam-saat { color: #38bdf8; font-weight: bold; }
        </style>
    </head>
    <body>
        <div class="header">
            <!-- GitHub Raw Üzerinden Doğrudan Okunan logo.png -->
            <img src="https://raw.githubusercontent.com/mehmtyilmz60-collab/demiryol-vagon-app/main/logo.png" 
                 class="logo-img" 
                 alt="Logo"
                 onerror="this.src='https://raw.githubusercontent.com/mehmtyilmz60-collab/demiryol-vagon-app/main/Logo.jpg'">
            <h2>Demiryol Vagon Bakım & Adam-Saat Takip</h2>
        </div>
        
        <div class="main-layout">
            <!-- Sol Panel: Form -->
            <div class="left-panel">
                <h3>➕ Vagon Kayıt / Güncelleme</h3>
                
                <label>Vagon No</label>
                <input type="text" id="vagon_no" placeholder="Örn: VAG-103">

                <label>Atölye Giriş Tarihi / Saati</label>
                <input type="text" id="giris_tarihi" value="06.10.2026 08:00">

                <label>Kanala Alınma Tarihi / Saati</label>
                <input type="text" id="kanal_tarihi" placeholder="Örn: 06.10.2026 10:00">

                <label>İş Bitiş Tarihi / Saati</label>
                <input type="text" id="bitis_tarihi" placeholder="Örn: 08.10.2026 17:00">

                <label>Çalışan Personel Sayısı (Adam-Saat İçin)</label>
                <input type="number" id="personel_sayisi" value="2" min="1">

                <label>Durum</label>
                <select id="durum">
                    <option value="Bekliyor">Bekliyor</option>
                    <option value="Parça bekliyor">Parça bekliyor</option>
                    <option value="Bakım devam ediyor">Bakım devam ediyor</option>
                    <option value="Tamamlandı">Tamamlandı</option>
                </select>

                <label>Açıklama / Fabrika & Atölye Notu</label>
                <textarea id="aciklama" placeholder="Gelen/giden parça detayları ve atölye notları..."></textarea>

                <button onclick="kaydet()">💾 Kaydet & Geçmişe İşle</button>
            </div>

            <!-- Sağ Panel: Tablo -->
            <div class="right-panel">
                <div style="display:flex; gap:10px;">
                    <button onclick="verileriYukle()">🔄 Yenile</button>
                    <button class="btn-excel" onclick="alert('Excel Adam-Saat Raporu indiriliyor...')">📊 Excel Rapor</button>
                </div>

                <div style="overflow-x:auto;">
                    <table>
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Vagon</th>
                                <th>Giriş</th>
                                <th>Bitiş</th>
                                <th>Adam-Saat</th>
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

                    bodyHtml += `<tr onclick="gecmisGoster('${item.vagon_no}', '${item.aciklama}', '${encodeURIComponent(JSON.stringify(item.gecmis || []))}')">
                        <td>${item.id}</td>
                        <td><b>${item.vagon_no}</b></td>
                        <td>${item.giris_tarihi || '-'}</td>
                        <td>${item.bitis_tarihi || '-'}</td>
                        <td class="adam-saat">${item.adam_saat || 0} A/S</td>
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
                let personel_sayisi = parseInt(document.getElementById('personel_sayisi').value) || 1;
                let durum = document.getElementById('durum').value;
                let
