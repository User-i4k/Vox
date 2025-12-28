# =========================
#  VOX — Basit Recon Tool
#  Tam açıklamalı sürüm
# =========================

# OS işlemleri (klasör oluşturma, terminal temizleme vb.) için
import os

# Domain formatını doğrulamak için düzenli ifadeler
import re

# DNS çözümleme (domain → IP) işlemleri için
import socket

# Terminal üzerinden nmap çalıştırmak için
import subprocess

# Sistemde nmap var mı diye kontrol etmek için
import shutil

# Programı güvenli şekilde sonlandırmak için
import sys


# -----------------------------
#  EKRANI TEMİZLEME FONKSİYONU
# -----------------------------
def clear_screen():
    # Windows sistemlerde 'cls', Linux/macOS için 'clear' komutu kullanılır
    os.system("cls" if os.name == "nt" else "clear")


# -----------------------------
#  DOMAIN DOĞRULAMA FONKSİYONU
# -----------------------------
def validate_domain(domain):
    # Boş girilmişse geçersiz
    if not domain or not domain.strip():
        return False

    # Geçerli domain formatını kontrol eden regex
    regex = r"^(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$"

    # Format yanlışsa geçersiz
    if not re.match(regex, domain.strip()):
        return False

    # DNS çözümleme yapılabiliyor mu?
    try:
        socket.gethostbyname(domain)
        return True
    except:
        return False


# -----------------------------
#  KLASÖR OLUŞTURMA (VARSA DOKUNMA)
# -----------------------------
def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


# -----------------------------
#  SUBDOMAIN MENÜSÜ
# -----------------------------
def subdomain_menu(domain):

    # Ekranı temizle
    clear_screen()

    print(f"[+] Hedef: {domain}")
    print("\nSubdomain Tarama Yöntemi Seç:")
    print("1) Pasif (wordlist kullanma)")
    print("2) Wordlist ile brute-force")
    print("00) Geri dön\n")

    # Kullanıcı seçimi al
    choice = input("> ").strip()

    # Subdomain sonuçlarının tutulacağı klasör
    base = os.path.join("results", domain, "subdomain")

    # SADECE subdomain menüsü seçildiğinde klasörü oluştur
    ensure_dir(base)

    # Pasif tarama
    if choice == "1":
        out_file = os.path.join(base, f"{domain}_passive.txt")
        passive_subdomains(domain, out_file)

    # Wordlist taraması
    elif choice == "2":
        out_file = os.path.join(base, f"{domain}_wordlist.txt")
        brute_subdomains(domain, out_file)

    # Geri dön
    elif choice == "00":
        return

    # Hatalı seçim
    else:
        print("Geçersiz seçim!")
        input("Devam için Enter...")


# -----------------------------
#  PASİF SUBDOMAIN TARAMA
# -----------------------------
def passive_subdomains(domain, out_file):

    print("\n[+] Pasif tarama başlıyor...\n")

    # Bulunan subdomainleri tekrar etmeyecek şekilde saklamak için SET
    found = set()

    # Önce ana domaini çözmeyi dene
    try:
        main_ip = socket.gethostbyname(domain)
        found.add(domain)
        print(f"Bulundu: {domain} -> {main_ip}")
    except:
        pass

    # Yaygın kayıt isimleri
    common = ["www", "mail", "mx", "ns1", "ns2"]

    # Her biri için DNS çözümleme dene
    for c in common:
        sub = f"{c}.{domain}"
        try:
            ip = socket.gethostbyname(sub)
            print(f"Bulundu: {sub} -> {ip}")
            found.add(sub)
        except:
            pass

    # Dosyaya yaz
    with open(out_file, "w") as f:
        for s in sorted(found):
            f.write(s + "\n")

    print(f"\n[+] Kayıt tamamlandı: {out_file}")
    input("\nDevam için Enter...")


# -----------------------------
#  WORDLIST İLE SUBDOMAIN TARAMA
# -----------------------------
def brute_subdomains(domain, out_file):

    print("\n[!] Wordlist yolunu gir (örn: wordlist/subs.txt)")
    wl = input("> ").strip()

    # Wordlist var mı kontrol et
    if not os.path.exists(wl):
        print("Wordlist bulunamadı!")
        input("Devam için Enter...")
        return

    print("\n[+] Wordlist taraması başlıyor...\n")

    found = set()   # bulunan subdomainler
    total = 0       # kaç deneme yapıldı sayacı

    # Wordlist’i oku
    with open(wl) as f:
        words = [w.strip() for w in f if w.strip()]

    # Her kelime için subdomain oluştur
    for w in words:
        total += 1
        sub = f"{w}.{domain}"

        # Kullanıcıya ilerleme göstermek için aynı satırda yaz
        print(f"Deniyor: {sub}", end="\r")

        # DNS çözümleme dene
        try:
            socket.gethostbyname(sub)
            print(f"\nBulundu: {sub}")
            found.add(sub)
        except:
            pass

    # Sonuçları yaz
    with open(out_file, "w") as f:
        for s in sorted(found):
            f.write(s + "\n")

    print(f"\n[+] Toplam deneme: {total}")
    print(f"[+] Kayıt tamamlandı: {out_file}")
    input("\nDevam için Enter...")


# -----------------------------
#  NMAP MENÜSÜ
# -----------------------------
def nmap_menu(domain):

    # Ekranı temizle
    clear_screen()

    # Sistemde nmap var mı kontrol et
    if shutil.which("nmap") is None:
        print("HATA: nmap yüklü değil veya PATH'te değil.")
        input("Devam için Enter...")
        return

    print(f"[+] Hedef: {domain}")
    print("\nNmap Tarama Seç:")
    print("1) Temel tarama (nmap {TARGET})")
    print("2) Servis taraması (nmap -sV -T4 {TARGET})")
    print("00) Geri dön\n")

    choice = input("> ").strip()

    # Sonuç klasörü
    base = os.path.join("results", domain, "nmap")

    # SADECE nmap seçilince klasör oluştur
    ensure_dir(base)

    if choice == "1":
        out_file = os.path.join(base, f"{domain}_basic.txt")
        run_nmap(domain, ["nmap", domain], out_file)

    elif choice == "2":
        out_file = os.path.join(base, f"{domain}_service.txt")
        run_nmap(domain, ["nmap", "-sV", "-T4", domain], out_file)

    elif choice == "00":
        return

    else:
        print("Geçersiz seçim!")
        input("Devam için Enter...")


# -----------------------------
#  NMAP ÇALIŞTIRMA
# -----------------------------
def run_nmap(domain, cmd, out_file):

    print(f"\n[+] Çalıştırılıyor: {' '.join(cmd)}\n")

    # nmap komutunu terminalde çalıştır
    # capture_output=True → çıktıyı yakalar
    result = subprocess.run(cmd, capture_output=True, text=True)

    # Çıktıyı dosyaya yaz
    with open(out_file, "w") as f:
        f.write(result.stdout)

    print(f"[+] Kayıt tamamlandı: {out_file}")
    input("\nDevam için Enter...")


# -----------------------------
#  ANA PROGRAM
# -----------------------------
def main():

    clear_screen()

    print("=== VOX Recon Tool ===\n")

    # Kullanıcıdan domain al
    domain = input("Hedef domain: ").strip()

    # Geçersizse programdan çık
    if not validate_domain(domain):
        print("\nHATA: Domain geçersiz veya çözümlenemedi.")
        sys.exit(1)

    # Sonsuz döngü — kullanıcı çık diyene kadar
    while True:

        clear_screen()

        print(f"[+] Hedef: {domain}\n")
        print("01) Subdomain taraması")
        print("02) Nmap port taraması")
        print("00) Çıkış\n")

        choice = input("> ").strip()

        # Kullanıcı seçimine göre menü aç
        if choice == "01":
            subdomain_menu(domain)

        elif choice == "02":
            nmap_menu(domain)

        elif choice == "00":
            print("\nÇıkılıyor...")
            break

        else:
            print("Geçersiz seçim!")
            input("Devam için Enter...")


# -----------------------------
#  PROGRAM BAŞLANGIÇ NOKTASI
# -----------------------------
if __name__ == "__main__":
    main()
