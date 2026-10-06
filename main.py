import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(1)

import customtkinter as ctk
from tkinter import ttk, messagebox, filedialog
import sqlite3
from datetime import datetime
from openpyxl import Workbook

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# ================== DB ==================
conn = sqlite3.connect("vagonlar.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS vagonlar (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vagon_no TEXT,
    giris_tarihi TEXT,
    kanal_tarihi TEXT,
    bitis_tarihi TEXT,
    durum TEXT,
    aciklama TEXT
)
""")
conn.commit()

# ================== HELPERS ==================
def bugun():
    return datetime.now().strftime("%d.%m.%Y")

# ================== FUNCTIONS ==================
def verileri_yukle():
    tree.delete(*tree.get_children())
    cursor.execute("SELECT id,vagon_no,giris_tarihi,kanal_tarihi,bitis_tarihi,durum FROM vagonlar")
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)

def temizle():
    entry_vagon.delete(0,"end")
    entry_giris.delete(0,"end")
    entry_kanal.delete(0,"end")
    entry_bitis.delete(0,"end")
    entry_giris.insert(0, bugun())
    combo_durum.set("Bekliyor")
    text_aciklama.delete("1.0","end")

def form_ac(mod):
    global form_modu
    form_modu = mod
    menu_frame.pack_forget()
    form_frame.pack(fill="both")
    if mod == "ekle":
        temizle()

def form_kapat():
    form_frame.pack_forget()
    menu_frame.pack(fill="both")

def kaydet():
    if not entry_vagon.get():
        messagebox.showwarning("Uyarı","Vagon no boş olamaz!")
        return

    if form_modu == "ekle":
        cursor.execute("""
        INSERT INTO vagonlar (vagon_no,giris_tarihi,kanal_tarihi,bitis_tarihi,durum,aciklama)
        VALUES (?,?,?,?,?,?)
        """,(entry_vagon.get(),entry_giris.get(),entry_kanal.get(),entry_bitis.get(),
              combo_durum.get(),text_aciklama.get("1.0","end").strip()))
    else:
        cursor.execute("""
        UPDATE vagonlar SET vagon_no=?,giris_tarihi=?,kanal_tarihi=?,bitis_tarihi=?,
        durum=?,aciklama=? WHERE id=?
        """,(entry_vagon.get(),entry_giris.get(),entry_kanal.get(),entry_bitis.get(),
             combo_durum.get(),text_aciklama.get("1.0","end").strip(),secili_id))

    conn.commit()
    verileri_yukle()
    form_kapat()

def secili_getir(event):
    global secili_id
    secili = tree.focus()
    if not secili: return
    secili_id = tree.item(secili)["values"][0]

def detay_pencere(event):
    secili = tree.focus()
    if not secili: return

    vagon_id = tree.item(secili)["values"][0]
    cursor.execute("SELECT * FROM vagonlar WHERE id=?", (vagon_id,))
    row = cursor.fetchone()

    detay = ctk.CTkToplevel(app)
    detay.title("Vagon Detay Bilgileri")
    detay.geometry("480x500")
    detay.grab_set()

    frame = ctk.CTkFrame(detay)
    frame.pack(expand=True, fill="both", padx=15, pady=15)

    alanlar = [
        ("Vagon No", row[1]),
        ("Atölye Giriş", row[2]),
        ("Kanala Alınma", row[3]),
        ("İş Bitiş", row[4]),
        ("Durum", row[5]),
        ("Açıklama", row[6])
    ]

    for baslik, deger in alanlar:
        ctk.CTkLabel(frame, text=baslik, font=("Segoe UI",12,"bold")).pack(anchor="w", pady=(8,2))
        box = ctk.CTkTextbox(frame, height=36 if baslik!="Açıklama" else 140)
        box.insert("1.0", deger)
        box.configure(state="disabled")
        box.pack(fill="x")

# ================== EXCEL ==================
def excel_rapor():
    dosya = filedialog.asksaveasfilename(
        defaultextension=".xlsx",
        filetypes=[("Excel Dosyası","*.xlsx")]
    )
    if not dosya:
        return

    wb = Workbook()
    ws = wb.active
    ws.title = "Vagon Bakım Raporu"

    kolonlar = ("ID","Vagon","Giriş","Kanal","Bitiş","Durum","Açıklama")
    ws.append(kolonlar)

    cursor.execute("SELECT * FROM vagonlar")
    for row in cursor.fetchall():
        ws.append(row)

    for col in ws.columns:
        max_len = 0
        col_letter = col[0].column_letter
        for cell in col:
            if cell.value:
                max_len = max(max_len, len(str(cell.value)))
        ws.column_dimensions[col_letter].width = max_len + 4

    wb.save(dosya)
    messagebox.showinfo("Başarılı","Excel raporu oluşturuldu!")

# ================== UI ==================
app = ctk.CTk()
app.title("Vagon Bakım Takip Sistemi")
app.geometry("1350x750")

# ---- STYLE ----
style = ttk.Style(app)
style.theme_use("clam")
style.configure("Treeview",
    background="#1e1e1e",
    foreground="white",
    rowheight=36,
    fieldbackground="#1e1e1e",
    font=("Segoe UI",12)
)
style.configure("Treeview.Heading",
    background="#2a2a2a",
    foreground="white",
    font=("Segoe UI",13,"bold")
)
style.map("Treeview", background=[("selected","#2a72d4")])

# -------- LEFT PANEL --------
sol = ctk.CTkFrame(app, width=280)
sol.pack(side="left", fill="y", padx=10, pady=10)
sol.pack_propagate(False)

menu_frame = ctk.CTkFrame(sol)
menu_frame.pack(fill="both", expand=True)

form_frame = ctk.CTkFrame(sol)

ctk.CTkLabel(menu_frame, text="İşlemler", font=("Segoe UI",20,"bold")).pack(pady=12)

ctk.CTkButton(menu_frame, text="➕ Yeni Vagon Ekle", height=46, command=lambda:form_ac("ekle")).pack(fill="x", padx=10, pady=8)
ctk.CTkButton(menu_frame, text="✏ Vagon Güncelle", height=46, command=lambda:form_ac("guncelle")).pack(fill="x", padx=10, pady=8)
ctk.CTkButton(menu_frame, text="📊 Excel Rapor", height=46, command=excel_rapor).pack(fill="x", padx=10, pady=8)

def label(txt):
    ctk.CTkLabel(form_frame,text=txt,anchor="w",font=("Segoe UI",12,"bold")).pack(fill="x", padx=10, pady=(6,2))

label("Vagon No")
entry_vagon = ctk.CTkEntry(form_frame,height=38)
entry_vagon.pack(fill="x", padx=10)

label("Atölye Giriş")
entry_giris = ctk.CTkEntry(form_frame,height=38)
entry_giris.insert(0, bugun())
entry_giris.pack(fill="x", padx=10)

label("Kanala Alınma")
entry_kanal = ctk.CTkEntry(form_frame,height=38)
entry_kanal.pack(fill="x", padx=10)

label("İş Bitiş")
entry_bitis = ctk.CTkEntry(form_frame,height=38)
entry_bitis.pack(fill="x", padx=10)

label("Durum")
combo_durum = ctk.CTkComboBox(form_frame, values=["Bekliyor","Parça bekliyor","Bakım devam ediyor","Tamamlandı"])
combo_durum.pack(fill="x", padx=10)

label("Açıklama")
text_aciklama = ctk.CTkTextbox(form_frame, height=120)
text_aciklama.pack(fill="x", padx=10)

ctk.CTkButton(form_frame, text="💾 Kaydet", height=44, command=kaydet).pack(fill="x", padx=10, pady=8)
ctk.CTkButton(form_frame, text="🔙 Geri Dön", height=44, fg_color="#444", command=form_kapat).pack(fill="x", padx=10, pady=8)

# -------- TABLE --------
sag = ctk.CTkFrame(app)
sag.pack(side="right", expand=True, fill="both", padx=10, pady=10)

columns = ("ID","Vagon","Giriş","Kanal","Bitiş","Durum")
tree = ttk.Treeview(sag, columns=columns, show="headings")

gen = [60,140,150,160,160,160]
for c,w in zip(columns,gen):
    tree.heading(c,text=c)
    tree.column(c,width=w,minwidth=w,stretch=False,anchor="center")

tree.pack(expand=True, fill="both")
tree.bind("<<TreeviewSelect>>", secili_getir)
tree.bind("<Double-1>", detay_pencere)

verileri_yukle()
app.mainloop()

