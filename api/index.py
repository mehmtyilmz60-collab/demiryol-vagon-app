from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

app = FastAPI()

vagonlar_db = [
    {
        "id": 1,
        "vagon_no": "8175 4569 872-9 Sgss-w R",
        "giris_tarihi": "17.10.2025 08:00",
        "bitis_tarihi": "-",
        "personel_sayisi": 3,
        "bekleme_suresi": "354 Gün",
        "durum": "Bakım devam ediyor",
        "aciklama": "Tekerlek takımı kontrol ediliyor."
    },
    {
        "id": 2,
        "vagon_no": "8175 4569 851-3 SGSS-w F",
        "giris_tarihi": "17.11.2025 08:00",
        "bitis_tarihi": "-",
        "personel_sayisi": 2,
        "bekleme_suresi": "323 Gün",
        "durum": "Bakım devam ediyor",
        "aciklama": "Rulman revizyonu."
    },
    {
        "id": 3,
        "vagon_no": "3175 4569 059-4 Sgss-w",
        "giris_tarihi": "15.02.2026 09:00",
        "bitis_tarihi": "-",
        "personel_sayisi": 2,
        "bekleme_suresi": "233 Gün",
        "durum": "Parça bekliyor",
        "aciklama": "Fren valfi bekleniyor."
    },
    {
        "id": 4,
        "vagon_no": "3175 3301 669-7 Ks-w*",
        "giris_tarihi": "16.12.2025 08:00",
        "bitis_tarihi": "22.01.2026 17:00",
        "personel_sayisi": 4,
        "bekleme_suresi": "37 Gün",
        "durum": "Tamamlandı",
        "aciklama": "Tamir tamamlandı, teslime hazır."
    }
]

class VagonModel(BaseModel):
    vagon_no: str
    giris_tarihi: str
    bitis_tarihi: Optional[str] = "-"
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
        <title>Vagon Bakım ve Takip Sistemi</title>
        <style>
            * { box-sizing: border-box; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
            body { margin: 0; padding: 0; background-color: #121212; color: #ffffff; display: flex; height: 100vh; overflow: hidden; }
            
            /* Sol Menü (Sidebar) */
            .sidebar { width: 260px; background-color: #1a1a1a; padding: 20px 15px; display: flex; flex-direction: column; justify-content: space-between; border-right: 1px solid #2a2a2a; }
            .logo-area { text-align: center; margin-bottom: 25px; }
            .logo-img { width: 140px; height: 140px; border-radius: 50%; border: 2px solid #b91c1c; box-shadow: 0 0 15px rgba(185, 28, 28, 0.4); object-fit: cover; }
            
            .nav-menu { display: flex; flex-direction: column; gap: 12px; }
            .nav-btn { background: transparent; color: #cccccc; border: none; padding: 12px 15px; border-radius: 6px; text-align: left; font-size: 14px; font-weight: bold; cursor: pointer; display: flex; align-items: center; gap: 10px; transition: 0.2s; }
            .nav-btn:hover { background-color: #2a2a2a; color: #fff; }
            .nav-btn.active { background-color: #1f538d; color: #fff; }
            
            .btn-excel-genel { background-color: #10b981; color: white; border: none; padding: 12px; border-radius: 6px; font-weight: bold; cursor: pointer; width: 100%; display: flex; align-items: center; justify-content: center; gap: 8px; }
            .btn-excel-genel:hover { background-color: #059669; }

            /* Sağ Ana İçerik */
            .main-content { flex: 1; padding: 25px 30px; display: flex; flex-direction: column; overflow-y: auto; background-color: #141414; }
            .top-bar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; flex-wrap: wrap; gap: 15px; }
            .top-title { font-size: 22px; font-weight: bold; margin: 0; color: #ffffff; }
            
            .actions-bar { display: flex; align-items: center; gap: 10px; }
            .search-input { background-color: #222; border: 1px solid #444; color: #fff; padding: 8px 12px; border-radius: 6px; font-size: 13px; width: 180px; }
            .select-filter { background-color: #222; border: 1px solid #444; color: #fff; padding: 8px 12px; border-radius: 6px; font-size: 13px; }
            
            .btn-action { border: none; padding: 8px 14px; border-radius: 6px; font-size: 13px; font-weight: bold; cursor: pointer; display: flex; align-items: center; gap: 5px; }
            .btn-add { background-color: #1f538d; color: white; }
            .btn-add:hover { background-color: #14375e; }
            .btn-edit { background-color: #2563eb; color: white; }
            .btn-delete { background-color: #ef4444; color: white; }
            
            /* Tablo */
            .table-container { border: 1px solid #333; border-radius: 8px; overflow: hidden; background-color: #1a1a1a; margin-top: 10px; }
            table { width: 100%; border-collapse: collapse; font-size: 13px; text-align: left; }
            th { background-color: #222; color: #ffffff; padding: 12px 15px; font-weight: bold; border-bottom: 1px solid #333; text-align: center; }
            td { padding: 12px 15px; border-bottom: 1px solid #282828; text-align: center; color: #dddddd; }
            tr:hover { background-color: #262626; cursor: pointer; }
            
            .summary-text { margin-top: 15px; color: #f97316; font-weight: bold; font-size: 14px; }

            /* Modal (Yeni Kayıt Penceresi) */
            .modal-overlay { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.7); justify-content: center; align-items: center; z-index: 1000; }
            .modal { background-color: #222; padding: 25px; border-radius: 10px; width: 400px; border: 1px solid #444; box-shadow: 0 5px 20px rgba(0,0,0,0.8); }
            .modal h3 { margin-top: 0; color: #fff; border-bottom: 1px solid #444; padding-bottom: 10px; }
            .form-group { margin-bottom: 12px; }
            .form-group label { display: block; font-size: 12px; color: #aaa; margin-bottom: 4px; }
            .form-group input, .form-group select { width: 100%; padding: 8px; border-radius: 5px; border: 1px solid #444; background-color: #111; color: #fff; font-size: 13px; }
            .modal-buttons { display: flex; gap: 10px; margin-top: 20px; }
        </style>
    </head>
    <body>

        <!-- Sol Yan Menü -->
        <div class="sidebar">
            <div>
                <div class="logo-area">
                    <!-- Vercel Public Klasöründeki Statik Logo -->
                    <img src="/logo.png" class="logo-img" alt="Gebze Vagon Bilim Kültür Kulübü">
                </div>
                
                <div class="nav-menu">
                    <button class="nav-btn active">📊 Vagon Takibi</button>
                    <button class="nav-btn">⚙️ Gönderilen Parçalar</button>
                    <button class="nav-btn">📋 Demirbaş Listesi</button>
                </div>
            </div>

            <button class="btn-excel-genel" onclick="alert('Genel Excel Raporu Hazırlanıyor...')">
                📊 Genel Excel Raporu
            </button>
        </div>

        <!-- Sağ İçerik Alanı -->
        <div class="main-content">
            <div class="top-bar">
                <h2 class="top-title">Vagon Bakım Listesi</h2>
                
                <div class="actions-bar">
                    <input type="text" id="searchInput" class="search-input" placeholder="Arama yapın..." onkeyup="aramaYap()">
                    <select class="select-filter">
                        <option>Tüm Zamanlar</option>
                        <option>Son 1 Ay</option>
                        <option>Son 1 Yıl</option>
                    </select>
                    
                    <button class="btn-action btn-add" onclick="modalAc()">+ Yeni Kayıt Ekle</button>
                    <button class="btn-action btn-edit" onclick="alert('Lütfen tablodan güncellenecek vagonu seçin.')">✏️ Güncelle</button>
                    <button class="btn-action btn-delete" onclick="alert('Lütfen silinecek vagonu seçin.')">🗑️ Sil</button>
                </div>
            </div>

            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>Vagon Numarası</th>
                            <th>Giriş Tarihi</th>
                            <th>Bitiş Tarihi</th>
                            <th>Bekleme Süresi / Adam-Saat</th>
                            <th>Durum</th>
                        </tr>
                    </thead>
                    <tbody id="vagonTableBody"></tbody>
                </table>
            </div>

            <div class="summary-text" id="toplamVagonText">Toplam vagon sayısı: 0</div>
        </div>

        <!-- Yeni Kayıt Ekle Pop-Up (Modal) -->
        <div class="modal-overlay" id="modalOverlay">
            <div class="modal">
                <h3>+ Yeni Vagon Kaydı Ekle</h3>
                <div class="form-group">
                    <label>Vagon Numarası</label>
                    <input type="text" id="m_vagon_no" placeholder="Örn: 8175 4569 872-9 Sgss-w">
                </div>
                <div class="form-group">
                    <label>Giriş Tarihi & Saati</label>
                    <input type="text" id="m_giris" value="06.10.2026 08:00">
                </div>
                <div class="form-group">
                    <label>Bitiş Tarihi (Varsa)</label>
                    <input type="text" id="m_bitis" placeholder="-">
                </div>
                <div class="form-group">
                    <label>Çalışan Personel Sayısı</label>
                    <input type="number" id="m_personel" value="2" min="1">
                </div>
                <div class="form-group">
                    <label>Bakım Durumu</label>
                    <select id="m_durum">
                        <option value="Bakım devam ediyor">Bakım devam ediyor</option>
                        <option value="Parça bekliyor">Parça bekliyor</option>
                        <option value="Tamamlandı">Tamamlandı</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Açıklama / Atölye Notu</label>
                    <input type="text" id="m_aciklama" placeholder="Not ekleyin...">
                </div>
                <div class="modal-buttons">
                    <button class="btn-action btn-add" style="flex:1;" onclick="vagonKaydet()">Kaydet</button>
                    <button class="btn-action btn-delete" style="flex:1;" onclick="modalKapat()">İptal</button>
                </div>
            </div>
        </div>

        <script>
            async function verileriYukle() {
                let res = await fetch('/api/vagonlar');
                let data = await res.json();
                renderTable(data);
            }

            function renderTable(data) {
                let html = '';
                data.forEach(item => {
                    html += `<tr onclick="alert('VAGON DETAYI:\\n' + '${item.vagon_no}' + '\\n' + '${item.aciklama}')">
                        <td><b>${item.vagon_no}</b></td>
                        <td>${item.giris_tarihi}</td>
                        <td>${item.bitis_tarihi || '-'}</td>
                        <td><span style="color:#38bdf8; font-weight:bold;">${item.bekleme_suresi || item.adam_saat + ' A/S'}</span></td>
                        <td>${item.durum}</td>
                    </tr>`;
                });
                document.getElementById('vagonTableBody').innerHTML = html;
                document.getElementById('toplamVagonText').innerText = "Toplam vagon sayısı: " + data.length;
            }

            function modalAc() { document.getElementById('modalOverlay').style.display = 'flex'; }
            function modalKapat() { document.getElementById('modalOverlay').style.display = 'none'; }

            async function vagonKaydet() {
                let vagon_no = document.getElementById('m_vagon_no').value;
                let giris_tarihi = document.getElementById('m_giris').value;
                let bitis_tarihi = document.getElementById('m_bitis').value;
                let personel_sayisi = parseInt(document.getElementById('m_personel').value) || 1;
                let durum = document.getElementById('m_durum').value;
                let aciklama = document.getElementById('m_aciklama').value;

                if(!vagon_no) { alert('Vagon No boş bırakılamaz.'); return; }

                let res = await fetch('/api/vagon-ekle', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({vagon_no, giris_tarihi, bitis_tarihi, personel_sayisi, durum, aciklama})
                });

                if(res.ok) {
                    modalKapat();
                    verileriYukle();
                }
            }

            function aramaYap() {
                let input = document.getElementById('searchInput').value.toLowerCase();
                let rows = document.querySelectorAll('#vagonTableBody tr');
                rows.forEach(row => {
                    let text = row.innerText.toLowerCase();
                    row.style.display = text.includes(input) ? '' : 'none';
                });
            }

            verileriYukle();
        </script>
    </body>
    </html>
    """

@app.get("/api/vagonlar")
def vagon_listesi():
    for vagon in vagonlar_db:
        if "bekleme_suresi" not in vagon:
            try:
                fmt = "%d.%m.%Y %H:%M"
                d1 = datetime.strptime(vagon["giris_tarihi"], fmt)
                d2 = datetime.strptime(vagon["bitis_tarihi"], fmt)
                saat_farki = (d2 - d1).total_seconds() / 3600
                vagon["bekleme_suresi"] = f"{round(saat_farki * vagon.get('personel_sayisi', 1), 1)} A/S"
            except Exception:
                vagon["bekleme_suresi"] = "Hesaplanıyor..."
    return vagonlar_db

@app.post("/api/vagon-ekle")
def vagon_ekle(vagon: VagonModel):
    yeni_id = len(vagonlar_db) + 1
    yeni_vagon = {
        "id": yeni_id,
        "vagon_no": vagon.vagon_no,
        "giris_tarihi": vagon.giris_tarihi,
        "bitis_tarihi": vagon.bitis_tarihi,
        "personel_sayisi": vagon.personel_sayisi,
        "durum": vagon.durum,
        "aciklama": vagon.aciklama,
        "bekleme_suresi": "Yeni Kayıt"
    }
    vagonlar_db.append(yeni_vagon)
    return {"status": "success", "vagon": yeni_vagon}
