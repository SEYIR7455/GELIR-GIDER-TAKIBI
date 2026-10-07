import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys
import random
import glob

# ============================================================
# YOL YÖNETİMİ (EXE ve normal çalışma için dinamik)
# ============================================================
def program_klasoru():
    """
    EXE olarak çalışıyorsa EXE'nin bulunduğu klasörü,
    Python ile çalışıyorsa script'in bulunduğu klasörü döner.
    """
    if getattr(sys, 'frozen', False):
        # PyInstaller ile paketlenmişse
        return os.path.dirname(sys.executable)
    else:
        # Normal Python
        return os.path.dirname(os.path.abspath(__file__))


# Kayıt klasörü: masaüstü/gelirgider
def kayit_klasoru():
    klasor = os.path.join(program_klasoru(), "gelirgider")
    if not os.path.exists(klasor):
        try:
            os.makedirs(klasor)
        except Exception:
            klasor = program_klasoru()
    return klasor


KLASOR = kayit_klasoru()
KAYIT_DOSYASI = os.path.join(KLASOR, "kayitlar.txt")
HAVUZ_DOSYASI = os.path.join(KLASOR, "havuz.txt")
AYAR_DOSYASI = os.path.join(KLASOR, "ayarlar.txt")
IKON_KLASORU = os.path.join(KLASOR, "icons")


def rastgele_ikon():
    """icons/ klasöründen rastgele bir .ico dosyası seçer."""
    if not os.path.exists(IKON_KLASORU):
        try:
            os.makedirs(IKON_KLASORU)
        except Exception:
            pass
        return None
    ikonlar = glob.glob(os.path.join(IKON_KLASORU, "*.ico"))
    if not ikonlar:
        return None
    return random.choice(ikonlar)


# ============================================================
# GÜVENLİ MATEMATİK PARSER (4 işlem + parantez + ondalık)
# ============================================================
def guvenli_hesapla(ifade):
    if not ifade or not ifade.strip():
        raise ValueError("Boş ifade")

    izinli = set("0123456789.+-*/() ")
    for ch in ifade:
        if ch not in izinli:
            raise ValueError(f"Geçersiz karakter: {ch}")

    s = ifade.replace(" ", "")
    if not s:
        raise ValueError("Boş ifade")

    i = [0]

    def peak():
        return s[i[0]] if i[0] < len(s) else None

    def ilerle():
        i[0] += 1

    def sayi_oku():
        baslangic = i[0]
        nokta = 0
        while i[0] < len(s) and (s[i[0]].isdigit() or s[i[0]] == '.'):
            if s[i[0]] == '.':
                nokta += 1
                if nokta > 1:
                    raise ValueError("Birden fazla nokta")
            i[0] += 1
        if baslangic == i[0]:
            raise ValueError("Sayı bekleniyordu")
        return float(s[baslangic:i[0]])

    def ifade_oku():
        sonuc = terim_oku()
        while peak() in ('+', '-'):
            op = peak()
            ilerle()
            sag = terim_oku()
            sonuc = sonuc + sag if op == '+' else sonuc - sag
        return sonuc

    def terim_oku():
        sonuc = faktor_oku()
        while peak() in ('*', '/'):
            op = peak()
            ilerle()
            sag = faktor_oku()
            if op == '*':
                sonuc *= sag
            else:
                if sag == 0:
                    raise ValueError("Sıfıra bölme hatası")
                sonuc /= sag
        return sonuc

    def faktor_oku():
        ch = peak()
        if ch == '-':
            ilerle()
            return -faktor_oku()
        if ch == '+':
            ilerle()
            return faktor_oku()
        if ch == '(':
            ilerle()
            sonuc = ifade_oku()
            if peak() != ')':
                raise ValueError("Kapanmayan parantez")
            ilerle()
            return sonuc
        if ch is None:
            raise ValueError("Beklenmeyen son")
        return sayi_oku()

    sonuc = ifade_oku()
    if i[0] != len(s):
        raise ValueError("Fazla karakter")
    return sonuc


# ============================================================
# AÇILIŞ ANİMASYONU
# ============================================================
class AcilisAnimasyonu:
    def __init__(self, root, bitince_cagir):
        self.root = root
        self.bitince = bitince_cagir
        self.pencere = tk.Toplevel(root)
        self.pencere.title("Yükleniyor...")
        self.pencere.geometry("520x280")
        self.pencere.configure(bg="#0a0a1a")
        self.pencere.resizable(False, False)
        self.pencere.overrideredirect(True)

        # Ekran ortasına konumla
        self.pencere.update_idletasks()
        eg = self.pencere.winfo_screenwidth()
        ey = self.pencere.winfo_screenheight()
        x = (eg - 520) // 2
        y = (ey - 280) // 2
        self.pencere.geometry(f"520x280+{x}+{y}")

        # İkon varsa uygula
        ikon = rastgele_ikon()
        if ikon:
            try:
                self.pencere.iconbitmap(ikon)
            except Exception:
                pass

        # Çerçeve efekti
        cerceve = tk.Frame(self.pencere, bg="#00e5ff", bd=0)
        cerceve.place(x=0, y=0, width=520, height=280)

        ic = tk.Frame(self.pencere, bg="#0a0a1a", bd=0)
        ic.place(x=3, y=3, width=514, height=274)

        # Üst başlık
        tk.Label(ic, text="SEYİR 7", font=("Segoe UI", 32, "bold"),
                 bg="#0a0a1a", fg="#00e5ff").pack(pady=(30, 0))
        tk.Label(ic, text="ENTEGRE SİSTEMLER", font=("Segoe UI", 14),
                 bg="#0a0a1a", fg="#a0a0b0").pack()

        # Alt başlık
        tk.Label(ic, text="GELİR GİDER TAKİBİ", font=("Segoe UI", 20, "bold"),
                 bg="#0a0a1a", fg="#ffffff").pack(pady=(20, 5))

        # Yükleme çubuğu (canvas)
        self.bar_canvas = tk.Canvas(ic, width=400, height=8, bg="#1a1a2e",
                                     highlightthickness=0)
        self.bar_canvas.pack(pady=15)
        self.bar = self.bar_canvas.create_rectangle(0, 0, 0, 8, fill="#00e5ff", outline="")

        # Yüzde
        self.yuzde_label = tk.Label(ic, text="%0", font=("Consolas", 11),
                                     bg="#0a0a1a", fg="#00e5ff")
        self.yuzde_label.pack()

        # Alt bilgi
        self.durum_label = tk.Label(ic, text="Başlatılıyor...",
                                     font=("Segoe UI", 9, "italic"),
                                     bg="#0a0a1a", fg="#666680")
        self.durum_label.pack(side="bottom", pady=10)

        self.yuzde = 0
        self.animasyon_adim()

    def animasyon_adim(self):
        self.yuzde += random.randint(3, 9)
        if self.yuzde >= 100:
            self.yuzde = 100
            self.bar_canvas.coords(self.bar, 0, 0, 400, 8)
            self.yuzde_label.config(text="%100")
            self.durum_label.config(text="Hazır!")
            self.pencere.after(350, self._bitir)
            return

        self.bar_canvas.coords(self.bar, 0, 0, 400 * self.yuzde / 100, 8)
        self.yuzde_label.config(text=f"%{self.yuzde}")

        mesajlar = [
            "Sistem başlatılıyor...",
            "Veritabanı yükleniyor...",
            "Kayıtlar okunuyor...",
            "Arayüz hazırlanıyor...",
            "Neredeyse hazır...",
        ]
        self.durum_label.config(text=random.choice(mesajlar))
        self.pencere.after(random.randint(40, 110), self.animasyon_adim)

    def _bitir(self):
        self.pencere.destroy()
        self.bitince()


# ============================================================
# ANA UYGULAMA
# ============================================================
class GelirGiderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SEYİR 7 - Gelir Gider Takibi")
        self.root.geometry("600x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#1e1e2e")

        # İkon (rastgele)
        ikon = rastgele_ikon()
        if ikon:
            try:
                self.root.iconbitmap(ikon)
            except Exception:
                pass

        self.kayitlar = []
        self.havuz_baslangic = 0.0

        self._dosyadan_yukle()
        self._ayarlari_yukle()

        # Notebook
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=5, pady=5)

        self.tab1 = tk.Frame(self.notebook, bg="#1e1e2e")
        self.tab2 = tk.Frame(self.notebook, bg="#1e1e2e")
        self.tab3 = tk.Frame(self.notebook, bg="#1e1e2e")
        self.tab4 = tk.Frame(self.notebook, bg="#1e1e2e")

        self.notebook.add(self.tab1, text="Gelir / Gider")
        self.notebook.add(self.tab2, text="Kayıtlar")
        self.notebook.add(self.tab3, text="Havuz")
        self.notebook.add(self.tab4, text="🧮 Hesap Makinesi")

        self._sekme1_olustur()
        self._sekme2_olustur()
        self._sekme3_olustur()
        self._sekme4_olustur()

        # Sağ tık menüsü
        self.sag_menu = tk.Menu(self.root, tearoff=0, bg="#2a2a3e", fg="white",
                                activebackground="#4caf50", activeforeground="white")
        self.sag_menu.add_command(label="✏️ Düzenle", command=self._kayit_duzenle)
        self.sag_menu.add_command(label="🗑️ Sil", command=self._kayit_sil)

        self.root.protocol("WM_DELETE_WINDOW", self._kapat)

    # ========================================================
    # SEKME 1
    # ========================================================
    def _sekme1_olustur(self):
        tk.Label(self.tab1, text="💰 Gelir / Gider Ekle",
                 font=("Segoe UI", 18, "bold"),
                 bg="#1e1e2e", fg="#ffffff").pack(pady=15)

        tk.Label(self.tab1,
                 text="Negatif (-) = GİDER, Pozitif = GELİR\nOndalık: '.' — İşlem yazabilirsin (44+330)",
                 font=("Segoe UI", 10),
                 bg="#1e1e2e", fg="#a0a0b0", justify="center").pack(pady=5)

        kutu = tk.Frame(self.tab1, bg="#2a2a3e")
        kutu.pack(pady=15, padx=40, fill="x")

        tk.Label(kutu, text="Tarih:", font=("Segoe UI", 11, "bold"),
                 bg="#2a2a3e", fg="#ffffff").grid(row=0, column=0, padx=10, pady=8, sticky="w")
        self.tarih_entry = tk.Entry(kutu, font=("Segoe UI", 11), width=25)
        self.tarih_entry.grid(row=0, column=1, padx=10, pady=8)
        self.tarih_entry.insert(0, "06.10.2026")

        tk.Label(kutu, text="Miktar:", font=("Segoe UI", 11, "bold"),
                 bg="#2a2a3e", fg="#ffffff").grid(row=1, column=0, padx=10, pady=8, sticky="w")
        self.miktar_entry = tk.Entry(kutu, font=("Segoe UI", 11), width=25)
        self.miktar_entry.grid(row=1, column=1, padx=10, pady=8)
        self.miktar_entry.insert(0, "0.00")

        tk.Label(kutu, text="Kaynak:", font=("Segoe UI", 11, "bold"),
                 bg="#2a2a3e", fg="#ffffff").grid(row=2, column=0, padx=10, pady=8, sticky="w")
        self.kaynak_entry = tk.Entry(kutu, font=("Segoe UI", 11), width=25)
        self.kaynak_entry.grid(row=2, column=1, padx=10, pady=8)

        tk.Label(kutu, text="Açıklama:", font=("Segoe UI", 11, "bold"),
                 bg="#2a2a3e", fg="#ffffff").grid(row=3, column=0, padx=10, pady=8, sticky="w")
        self.aciklama_entry = tk.Entry(kutu, font=("Segoe UI", 11), width=25)
        self.aciklama_entry.grid(row=3, column=1, padx=10, pady=8)

        tk.Button(self.tab1, text="➕ Ekle",
                  font=("Segoe UI", 12, "bold"),
                  bg="#4caf50", fg="white",
                  activebackground="#388e3c", activeforeground="white",
                  relief="flat", padx=30, pady=10, cursor="hand2",
                  command=self._kayit_ekle).pack(pady=15)

        self.durum_label = tk.Label(self.tab1, text="",
                                     font=("Segoe UI", 10, "italic"),
                                     bg="#1e1e2e", fg="#ffd700")
        self.durum_label.pack(pady=5)

    # ========================================================
    # SEKME 2
    # ========================================================
    def _sekme2_olustur(self):
        tk.Label(self.tab2, text="📋 Tüm Kayıtlar",
                 font=("Segoe UI", 16, "bold"),
                 bg="#1e1e2e", fg="#ffffff").pack(pady=8)

        tk.Label(self.tab2,
                 text="💡 Sağ tık → Düzenle / Sil     |     Çift tık → Düzenle",
                 font=("Segoe UI", 9, "italic"),
                 bg="#1e1e2e", fg="#8888a0").pack(pady=2)

        cerceve = tk.Frame(self.tab2, bg="#1e1e2e")
        cerceve.pack(fill="both", expand=True, padx=10, pady=5)

        sutunlar = ("tarih", "miktar", "kaynak", "aciklama", "tip")
        self.tree = ttk.Treeview(cerceve, columns=sutunlar, show="headings", height=14)

        self.tree.heading("tarih", text="Tarih")
        self.tree.heading("miktar", text="Miktar")
        self.tree.heading("kaynak", text="Kaynak")
        self.tree.heading("aciklama", text="Açıklama")
        self.tree.heading("tip", text="Tür")

        self.tree.column("tarih", width=90, anchor="center")
        self.tree.column("miktar", width=90, anchor="e")
        self.tree.column("kaynak", width=110, anchor="w")
        self.tree.column("aciklama", width=130, anchor="w")
        self.tree.column("tip", width=70, anchor="center")

        self.tree.tag_configure("gelir", background="#1b3a1b", foreground="#a5ffa5")
        self.tree.tag_configure("gider", background="#3a1b1b", foreground="#ffa5a5")

        scroll = ttk.Scrollbar(cerceve, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        self.tree.bind("<Button-3>", self._sag_tik_goster)
        self.tree.bind("<Double-1>", lambda e: self._kayit_duzenle())

        buton_cerceve = tk.Frame(self.tab2, bg="#1e1e2e")
        buton_cerceve.pack(pady=8)

        tk.Button(buton_cerceve, text="✏️ Düzenle",
                  font=("Segoe UI", 10, "bold"),
                  bg="#2196f3", fg="white", relief="flat",
                  padx=15, pady=8, cursor="hand2",
                  command=self._kayit_duzenle).pack(side="left", padx=5)

        tk.Button(buton_cerceve, text="🗑️ Sil",
                  font=("Segoe UI", 10, "bold"),
                  bg="#e53935", fg="white", relief="flat",
                  padx=15, pady=8, cursor="hand2",
                  command=self._kayit_sil).pack(side="left", padx=5)

        tk.Button(buton_cerceve, text="🧹 Tümünü Temizle",
                  font=("Segoe UI", 10, "bold"),
                  bg="#ff9800", fg="white", relief="flat",
                  padx=15, pady=8, cursor="hand2",
                  command=self._hepsini_temizle).pack(side="left", padx=5)

        self._listeyi_yenile()

    # ========================================================
    # SEKME 3
    # ========================================================
    def _sekme3_olustur(self):
        tk.Label(self.tab3, text="🏦 Havuzdaki Para",
                 font=("Segoe UI", 18, "bold"),
                 bg="#1e1e2e", fg="#ffffff").pack(pady=15)

        self.havuz_label = tk.Label(self.tab3, text="0.00",
                                     font=("Segoe UI", 44, "bold"),
                                     bg="#1e1e2e", fg="#00e5ff")
        self.havuz_label.pack(pady=10)

        self.havuz_aciklama = tk.Label(self.tab3, text="Bakiye",
                                        font=("Segoe UI", 14),
                                        bg="#1e1e2e", fg="#a0a0b0")
        self.havuz_aciklama.pack()

        detay_kutu = tk.Frame(self.tab3, bg="#2a2a3e")
        detay_kutu.pack(pady=15, padx=40, fill="x")

        tk.Label(detay_kutu, text="Başlangıç (Elle):", font=("Segoe UI", 11, "bold"),
                 bg="#2a2a3e", fg="#ffd700").grid(row=0, column=0, padx=15, pady=6, sticky="w")
        self.baslangic_label = tk.Label(detay_kutu, text="0.00",
                                         font=("Segoe UI", 11, "bold"),
                                         bg="#2a2a3e", fg="#ffd700")
        self.baslangic_label.grid(row=0, column=1, padx=15, pady=6, sticky="e")

        tk.Label(detay_kutu, text="Toplam Gelir:", font=("Segoe UI", 11, "bold"),
                 bg="#2a2a3e", fg="#a5ffa5").grid(row=1, column=0, padx=15, pady=6, sticky="w")
        self.gelir_label = tk.Label(detay_kutu, text="0.00",
                                     font=("Segoe UI", 11, "bold"),
                                     bg="#2a2a3e", fg="#a5ffa5")
        self.gelir_label.grid(row=1, column=1, padx=15, pady=6, sticky="e")

        tk.Label(detay_kutu, text="Toplam Gider:", font=("Segoe UI", 11, "bold"),
                 bg="#2a2a3e", fg="#ffa5a5").grid(row=2, column=0, padx=15, pady=6, sticky="w")
        self.gider_label = tk.Label(detay_kutu, text="0.00",
                                     font=("Segoe UI", 11, "bold"),
                                     bg="#2a2a3e", fg="#ffa5a5")
        self.gider_label.grid(row=2, column=1, padx=15, pady=6, sticky="e")

        tk.Label(detay_kutu, text="Kayıt Sayısı:", font=("Segoe UI", 11, "bold"),
                 bg="#2a2a3e", fg="#ffffff").grid(row=3, column=0, padx=15, pady=6, sticky="w")
        self.sayi_label = tk.Label(detay_kutu, text="0",
                                    font=("Segoe UI", 11, "bold"),
                                    bg="#2a2a3e", fg="#ffffff")
        self.sayi_label.grid(row=3, column=1, padx=15, pady=6, sticky="e")

        buton_cerceve = tk.Frame(self.tab3, bg="#1e1e2e")
        buton_cerceve.pack(pady=10)

        tk.Button(buton_cerceve, text="✏️ Havuzu Elle Güncelle",
                  font=("Segoe UI", 11, "bold"),
                  bg="#9c27b0", fg="white", relief="flat",
                  padx=20, pady=10, cursor="hand2",
                  command=self._havuz_elle_guncelle).pack(side="left", padx=5)

        tk.Button(buton_cerceve, text="🔄 Yenile",
                  font=("Segoe UI", 11, "bold"),
                  bg="#2196f3", fg="white", relief="flat",
                  padx=20, pady=10, cursor="hand2",
                  command=self._havuz_guncelle).pack(side="left", padx=5)

        self._havuz_guncelle()

    # ========================================================
    # SEKME 4: HESAP MAKİNESİ
    # ========================================================
    def _sekme4_olustur(self):
        tk.Label(self.tab4, text="🧮 Hesap Makinesi",
                 font=("Segoe UI", 18, "bold"),
                 bg="#1e1e2e", fg="#ffffff").pack(pady=15)

        tk.Label(self.tab4,
                 text="4 işlem (+ - * /) ve parantez ( ) destekler\nOndalık: '.' — Örnek: 44+330 veya (12.5*3)/2",
                 font=("Segoe UI", 10),
                 bg="#1e1e2e", fg="#a0a0b0", justify="center").pack(pady=5)

        cerceve = tk.Frame(self.tab4, bg="#1e1e2e")
        cerceve.pack(pady=15, padx=20, fill="x")

        tk.Label(cerceve, text="İşlem:", font=("Segoe UI", 11, "bold"),
                 bg="#1e1e2e", fg="#ffffff").pack(anchor="w", padx=5)

        self.hesap_entry = tk.Entry(cerceve, font=("Consolas", 16), justify="right",
                                     bg="#2a2a3e", fg="#ffffff",
                                     insertbackground="white",
                                     relief="flat", bd=0)
        self.hesap_entry.pack(fill="x", ipady=12, pady=5)
        self.hesap_entry.bind("<KeyRelease>", self._anlik_hesapla)
        self.hesap_entry.bind("<Return>", lambda e: self._hesapla_ve_aktar())

        tk.Label(self.tab4, text="Sonuç:", font=("Segoe UI", 11, "bold"),
                 bg="#1e1e2e", fg="#ffffff").pack(anchor="w", padx=25)

        self.sonuc_label = tk.Label(self.tab4, text="0",
                                     font=("Consolas", 28, "bold"),
                                     bg="#1e1e2e", fg="#00e5ff")
        self.sonuc_label.pack(pady=8)

        tus_kutu = tk.Frame(self.tab4, bg="#1e1e2e")
        tus_kutu.pack(pady=5)

        tuslar = [
            ["7", "8", "9", "/", "("],
            ["4", "5", "6", "*", ")"],
            ["1", "2", "3", "-", "C"],
            ["0", ".", "=", "+", "←"],
        ]

        for satir in tuslar:
            sf = tk.Frame(tus_kutu, bg="#1e1e2e")
            sf.pack(pady=2)
            for tus in satir:
                renk = "#2a2a3e"
                fg = "#ffffff"
                if tus in ("+", "-", "*", "/", "(", ")"):
                    renk = "#455a64"
                elif tus == "=":
                    renk = "#4caf50"
                elif tus == "C":
                    renk = "#e53935"
                elif tus == "←":
                    renk = "#ff9800"

                tk.Button(sf, text=tus, font=("Segoe UI", 12, "bold"),
                          bg=renk, fg=fg, relief="flat",
                          width=4, height=2, cursor="hand2",
                          activebackground="#555555", activeforeground="white",
                          command=lambda t=tus: self._tus_bas(t)).pack(side="left", padx=2)

        tk.Label(self.tab4, text="Sonucu kullan:",
                 font=("Segoe UI", 10, "italic"),
                 bg="#1e1e2e", fg="#a0a0b0").pack(pady=(15, 5))

        kullan_kutu = tk.Frame(self.tab4, bg="#1e1e2e")
        kullan_kutu.pack()

        tk.Button(kullan_kutu, text="➡️ Gelir/Gider'e Aktar",
                  font=("Segoe UI", 10, "bold"),
                  bg="#2196f3", fg="white", relief="flat",
                  padx=15, pady=8, cursor="hand2",
                  command=self._hesapla_ve_aktar).pack(side="left", padx=5)

        tk.Button(kullan_kutu, text="🗑️ Temizle",
                  font=("Segoe UI", 10, "bold"),
                  bg="#9e9e9e", fg="white", relief="flat",
                  padx=15, pady=8, cursor="hand2",
                  command=self._hesap_temizle).pack(side="left", padx=5)

    def _tus_bas(self, tus):
        if tus == "C":
            self.hesap_entry.delete(0, tk.END)
            self.sonuc_label.config(text="0", fg="#00e5ff")
        elif tus == "=":
            self._hesapla_ve_aktar()
        elif tus == "←":
            mevcut = self.hesap_entry.get()
            self.hesap_entry.delete(0, tk.END)
            self.hesap_entry.insert(0, mevcut[:-1])
            self._anlik_hesapla()
        else:
            self.hesap_entry.insert(tk.END, tus)
            self._anlik_hesapla()

    def _anlik_hesapla(self, event=None):
        ifade = self.hesap_entry.get().strip()
        if not ifade:
            self.sonuc_label.config(text="0", fg="#00e5ff")
            return
        try:
            sonuc = guvenli_hesapla(ifade)
            if sonuc == int(sonuc):
                self.sonuc_label.config(text=f"{int(sonuc)}", fg="#00e5ff")
            else:
                self.sonuc_label.config(text=f"{sonuc:.6f}".rstrip('0').rstrip('.'), fg="#00e5ff")
        except Exception:
            self.sonuc_label.config(text="...", fg="#ffa500")

    def _hesapla_ve_aktar(self):
        ifade = self.hesap_entry.get().strip()
        if not ifade:
            return
        try:
            sonuc = guvenli_hesapla(ifade)
        except Exception as e:
            messagebox.showerror("Hata", f"Geçersiz işlem:\n{e}")
            return

        self.miktar_entry.delete(0, tk.END)
        if sonuc == int(sonuc):
            self.miktar_entry.insert(0, f"{int(sonuc)}")
        else:
            self.miktar_entry.insert(0, f"{sonuc:.6f}".rstrip('0').rstrip('.'))

        self.durum_label.config(text=f"🧮 Hesap sonucu aktarıldı: {sonuc:.2f}", fg="#00e5ff")
        self.notebook.select(self.tab1)

    def _hesap_temizle(self):
        self.hesap_entry.delete(0, tk.END)
        self.sonuc_label.config(text="0", fg="#00e5ff")

    # ========================================================
    # HAVUZ ELLE
    # ========================================================
    def _havuz_elle_guncelle(self):
        pencere = tk.Toplevel(self.root)
        pencere.title("Havuzu Elle Güncelle")
        pencere.geometry("320x180+500+300")
        pencere.configure(bg="#1e1e2e")
        pencere.resizable(False, False)

        tk.Label(pencere, text="Başlangıç Tutarı (Elle):",
                 font=("Segoe UI", 11, "bold"),
                 bg="#1e1e2e", fg="#ffffff").pack(pady=10)

        tk.Label(pencere,
                 text="(Bu tutar, kayıtların üzerine eklenir.\nNegatif değer = borç)",
                 font=("Segoe UI", 9, "italic"),
                 bg="#1e1e2e", fg="#a0a0b0").pack(pady=2)

        entry = tk.Entry(pencere, font=("Segoe UI", 12), width=20, justify="center")
        entry.pack(pady=10)
        entry.insert(0, f"{self.havuz_baslangic:.2f}")
        entry.focus()

        def kaydet():
            try:
                deger = float(entry.get().strip().replace(",", "."))
            except ValueError:
                messagebox.showerror("Hata", "Geçerli bir sayı gir!")
                return
            self.havuz_baslangic = deger
            self._havuz_dosyaya_kaydet()
            self._havuz_guncelle()
            pencere.destroy()

        bf = tk.Frame(pencere, bg="#1e1e2e")
        bf.pack(pady=5)

        tk.Button(bf, text="💾 Kaydet", font=("Segoe UI", 10, "bold"),
                  bg="#4caf50", fg="white", relief="flat", padx=15, pady=6,
                  cursor="hand2", command=kaydet).pack(side="left", padx=5)

        tk.Button(bf, text="❌ İptal", font=("Segoe UI", 10, "bold"),
                  bg="#9e9e9e", fg="white", relief="flat", padx=15, pady=6,
                  cursor="hand2", command=pencere.destroy).pack(side="left", padx=5)

        entry.bind("<Return>", lambda e: kaydet())

    # ========================================================
    # KAYIT İŞLEMLERİ
    # ========================================================
    def _kayit_ekle(self):
        tarih = self.tarih_entry.get().strip()
        miktar_str = self.miktar_entry.get().strip().replace(",", ".")
        kaynak = self.kaynak_entry.get().strip()
        aciklama = self.aciklama_entry.get().strip()

        if not tarih:
            messagebox.showerror("Hata", "Tarih boş olamaz!")
            return

        try:
            miktar = float(miktar_str)
        except ValueError:
            try:
                miktar = guvenli_hesapla(miktar_str)
            except Exception:
                messagebox.showerror("Hata", "Miktar geçerli bir sayı veya işlem olmalı!")
                return

        if miktar == 0:
            messagebox.showerror("Hata", "Miktar 0 olamaz!")
            return
        if not kaynak:
            messagebox.showerror("Hata", "Kaynak boş olamaz!")
            return

        tip = "gider" if miktar < 0 else "gelir"
        self.kayitlar.append((tarih, miktar, kaynak, aciklama, tip))
        self._dosyaya_kaydet()
        self._listeyi_yenile()
        self._havuz_guncelle()

        self.miktar_entry.delete(0, tk.END)
        self.miktar_entry.insert(0, "0.00")
        self.aciklama_entry.delete(0, tk.END)

        if tip == "gelir":
            self.durum_label.config(text=f"✅ Gelir eklendi: +{miktar:.2f}", fg="#a5ffa5")
        else:
            self.durum_label.config(text=f"✅ Gider eklendi: {miktar:.2f}", fg="#ffa5a5")

    def _sag_tik_goster(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.sag_menu.tk_popup(event.x_root, event.y_root)

    def _kayit_sil(self):
        secili = self.tree.selection()
        if not secili:
            messagebox.showwarning("Uyarı", "Silmek için bir kayıt seç!")
            return
        if not messagebox.askyesno("Onay", "Seçili kaydı silmek istediğine emin misin?"):
            return
        index = self.tree.index(secili[0])
        gi = len(self.kayitlar) - 1 - index
        if 0 <= gi < len(self.kayitlar):
            del self.kayitlar[gi]
        self._dosyaya_kaydet()
        self._listeyi_yenile()
        self._havuz_guncelle()

    def _kayit_duzenle(self):
        secili = self.tree.selection()
        if not secili:
            messagebox.showwarning("Uyarı", "Düzenlemek için bir kayıt seç!")
            return
        index = self.tree.index(secili[0])
        gi = len(self.kayitlar) - 1 - index
        if not (0 <= gi < len(self.kayitlar)):
            return

        tarih, miktar, kaynak, aciklama, tip = self.kayitlar[gi]

        pencere = tk.Toplevel(self.root)
        pencere.title("Kaydı Düzenle")
        pencere.geometry("360x360+480+220")
        pencere.configure(bg="#1e1e2e")
        pencere.resizable(False, False)

        tk.Label(pencere, text="✏️ Kaydı Düzenle",
                 font=("Segoe UI", 14, "bold"),
                 bg="#1e1e2e", fg="#ffffff").pack(pady=12)

        kutu = tk.Frame(pencere, bg="#2a2a3e")
        kutu.pack(padx=30, pady=5, fill="x")

        tk.Label(kutu, text="Tarih:", font=("Segoe UI", 10, "bold"),
                 bg="#2a2a3e", fg="#ffffff").grid(row=0, column=0, padx=10, pady=8, sticky="w")
        e_tarih = tk.Entry(kutu, font=("Segoe UI", 10), width=22)
        e_tarih.grid(row=0, column=1, padx=10, pady=8)
        e_tarih.insert(0, tarih)

        tk.Label(kutu, text="Miktar:", font=("Segoe UI", 10, "bold"),
                 bg="#2a2a3e", fg="#ffffff").grid(row=1, column=0, padx=10, pady=8, sticky="w")
        e_miktar = tk.Entry(kutu, font=("Segoe UI", 10), width=22)
        e_miktar.grid(row=1, column=1, padx=10, pady=8)
        e_miktar.insert(0, f"{miktar:.2f}")

        tk.Label(kutu, text="Kaynak:", font=("Segoe UI", 10, "bold"),
                 bg="#2a2a3e", fg="#ffffff").grid(row=2, column=0, padx=10, pady=8, sticky="w")
        e_kaynak = tk.Entry(kutu, font=("Segoe UI", 10), width=22)
        e_kaynak.grid(row=2, column=1, padx=10, pady=8)
        e_kaynak.insert(0, kaynak)

        tk.Label(kutu, text="Açıklama:", font=("Segoe UI", 10, "bold"),
                 bg="#2a2a3e", fg="#ffffff").grid(row=3, column=0, padx=10, pady=8, sticky="w")
        e_aciklama = tk.Entry(kutu, font=("Segoe UI", 10), width=22)
        e_aciklama.grid(row=3, column=1, padx=10, pady=8)
        e_aciklama.insert(0, aciklama)

        def kaydet():
            y_tarih = e_tarih.get().strip()
            y_miktar_str = e_miktar.get().strip().replace(",", ".")
            y_kaynak = e_kaynak.get().strip()
            y_aciklama = e_aciklama.get().strip()

            if not y_tarih or not y_kaynak:
                messagebox.showerror("Hata", "Tarih ve Kaynak boş olamaz!")
                return
            try:
                y_miktar = float(y_miktar_str)
            except ValueError:
                try:
                    y_miktar = guvenli_hesapla(y_miktar_str)
                except Exception:
                    messagebox.showerror("Hata", "Miktar geçerli bir sayı olmalı!")
                    return
            if y_miktar == 0:
                messagebox.showerror("Hata", "Miktar 0 olamaz!")
                return

            y_tip = "gider" if y_miktar < 0 else "gelir"
            self.kayitlar[gi] = (y_tarih, y_miktar, y_kaynak, y_aciklama, y_tip)
            self._dosyaya_kaydet()
            self._listeyi_yenile()
            self._havuz_guncelle()
            pencere.destroy()
            self.durum_label.config(text="✅ Kayıt güncellendi!", fg="#ffd700")

        bf = tk.Frame(pencere, bg="#1e1e2e")
        bf.pack(pady=15)

        tk.Button(bf, text="💾 Kaydet", font=("Segoe UI", 10, "bold"),
                  bg="#4caf50", fg="white", relief="flat", padx=20, pady=8,
                  cursor="hand2", command=kaydet).pack(side="left", padx=5)

        tk.Button(bf, text="❌ İptal", font=("Segoe UI", 10, "bold"),
                  bg="#9e9e9e", fg="white", relief="flat", padx=20, pady=8,
                  cursor="hand2", command=pencere.destroy).pack(side="left", padx=5)

    def _hepsini_temizle(self):
        if not self.kayitlar:
            return
        if messagebox.askyesno("Onay", "Tüm kayıtlar silinecek. Emin misin?"):
            self.kayitlar = []
            self._dosyaya_kaydet()
            self._listeyi_yenile()
            self._havuz_guncelle()

    # ========================================================
    # LİSTE / HAVUZ
    # ========================================================
    def _listeyi_yenile(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for kayit in reversed(self.kayitlar):
            tarih, miktar, kaynak, aciklama, tip = kayit
            etiket = "gelir" if tip == "gelir" else "gider"
            miktar_str = f"+{miktar:.2f}" if miktar > 0 else f"{miktar:.2f}"
            tip_str = "GELİR" if tip == "gelir" else "GİDER"
            self.tree.insert("", "end",
                             values=(tarih, miktar_str, kaynak, aciklama, tip_str),
                             tags=(etiket,))

    def _havuz_guncelle(self):
        toplam_islem = sum(k[1] for k in self.kayitlar)
        gelir = sum(k[1] for k in self.kayitlar if k[1] > 0)
        gider = sum(k[1] for k in self.kayitlar if k[1] < 0)
        toplam_havuz = self.havuz_baslangic + toplam_islem

        if toplam_havuz < 0:
            self.havuz_label.config(text=f"{toplam_havuz:.2f}", fg="#ff5252")
            self.havuz_aciklama.config(text="⚠️ BORÇ VAR", fg="#ff5252")
        else:
            self.havuz_label.config(text=f"{toplam_havuz:.2f}", fg="#00e5ff")
            self.havuz_aciklama.config(text="✅ Bakiye", fg="#a0a0b0")

        self.baslangic_label.config(text=f"{self.havuz_baslangic:+.2f}")
        self.gelir_label.config(text=f"+{gelir:.2f}")
        self.gider_label.config(text=f"{gider:.2f}")
        self.sayi_label.config(text=f"{len(self.kayitlar)}")

    # ========================================================
    # DOSYA İŞLEMLERİ
    # ========================================================
    def _dosyaya_kaydet(self):
        try:
            with open(KAYIT_DOSYASI, "w", encoding="utf-8") as f:
                for tarih, miktar, kaynak, aciklama, tip in self.kayitlar:
                    f.write(f"{tarih}|{miktar}|{kaynak}|{aciklama}|{tip}\n")
        except Exception as e:
            print("Kaydetme hatası:", e)

    def _dosyadan_yukle(self):
        if os.path.exists(KAYIT_DOSYASI):
            try:
                with open(KAYIT_DOSYASI, "r", encoding="utf-8") as f:
                    for satir in f:
                        satir = satir.strip()
                        if not satir:
                            continue
                        parcalar = satir.split("|")
                        if len(parcalar) == 5:
                            tarih, miktar_str, kaynak, aciklama, tip = parcalar
                            try:
                                miktar = float(miktar_str)
                                self.kayitlar.append((tarih, miktar, kaynak, aciklama, tip))
                            except ValueError:
                                continue
            except Exception as e:
                print("Yükleme hatası:", e)

        if os.path.exists(HAVUZ_DOSYASI):
            try:
                with open(HAVUZ_DOSYASI, "r", encoding="utf-8") as f:
                    icerik = f.read().strip()
                    if icerik:
                        self.havuz_baslangic = float(icerik)
            except Exception as e:
                print("Havuz yükleme hatası:", e)

    def _havuz_dosyaya_kaydet(self):
        try:
            with open(HAVUZ_DOSYASI, "w", encoding="utf-8") as f:
                f.write(f"{self.havuz_baslangic}")
        except Exception as e:
            print("Havuz kaydetme hatası:", e)

    def _ayarlari_yukle(self):
        # Şimdilik boş, ileride kullanılabilir
        pass

    def _kapat(self):
        self._dosyaya_kaydet()
        self._havuz_dosyaya_kaydet()
        self.root.destroy()


# ============================================================
# BAŞLAT
# ============================================================
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()   # ana pencere gizli başlasın

    def basla():
        root.deiconify()
        GelirGiderApp(root)

    AcilisAnimasyonu(root, basla)
    root.mainloop()