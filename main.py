import os
import subprocess
import time

selam = ["selam", "merhaba", "vox", "selamlar", "slm", "mrb"]
hal_sorma = ["nasılsın", "naber", "ne haber"]
cikis = ["çık", "exit", "quit", "görüşürüz", "bye", "hoşça kal", "güle güle", "bay bay"]
iyi_hal = ["iyiyim", "harikayım", "mükemmelim", "süperim", "fena değilim"]
spotify_komutlari = ["spoti", "spotify", "spotify aç", "spotify başlat", "müzik", "müzik aç", "müzik başlat", "şarkı", "şarkı çal",
                    "şarkı aç"]
brawlhalla_komutlari = ["brawlhalla", "brawlhalla aç", "brawlhalla başlat", "brawl", "brawl aç", "brawl başlat"]
discord_komutlari = ["discord", "discord aç", "discord başlat"]

# WARP bağlantı durumunu kontrol etme fonksiyonu

def warp_bagli_mi():
    sonuc = subprocess.run(
        ["warp-cli", "status"],
        capture_output=True,
        text=True
    )
    return "Connected" in sonuc.stdout

while True:
    print()
    m = input("Sen: ")
    mesaj = m.lower()
    kelimeler = mesaj.split()

    # Durum değişkenleri
    selam_var = False
    hal_sorma_var = False
    cikis_var = False
    iyi_hal_var = False
    spotify_var = False
    brawlhalla_var = False
    discord_var = False

    # Kelimeleri kontrol et
    for kelime in kelimeler:
        if kelime in selam:
            selam_var = True
        if kelime in hal_sorma:
            hal_sorma_var = True
        if kelime in cikis:
            cikis_var = True
        if kelime in iyi_hal:
            iyi_hal_var = True
        if kelime in spotify_komutlari:
            spotify_var = True
        if kelime in brawlhalla_komutlari:
            brawlhalla_var = True
        if kelime in discord_komutlari:
            discord_var = True

    # Yanıt verme
    if selam_var and hal_sorma_var:
        print("-Vox: Selam! İyiyim, teşekkürler. Sen nasılsın?")
    
    elif iyi_hal_var and hal_sorma_var:
        print("-Vox: Bende iyiyim, teşekkürler! Sana nasıl yardımcı olabilirim?")
    
    elif selam_var:
        print("-Vox: Selam! Nasılsın?")

    elif hal_sorma_var:
        print("Vox: İyiyim, teşekkürler. Sen nasılsın?")
    
    elif iyi_hal_var:
        print("-Vox: Bunu duyduğuma sevindim! Sana nasıl yardımcı olabilirim?")

    # Uygulamaları açma komutları

    elif spotify_var and brawlhalla_var and discord_var:
        print("-Vox: Spotify, Brawlhalla ve Discord açılıyor... 🎧⚔️💬")
        os.system("spotify.exe")
        os.startfile("steam://rungameid/291550")
        if warp_bagli_mi():
            print("-Vox: Discord açılıyor... 💬")
            os.startfile(r"C:\Users\Msi-nb\AppData\Local\Discord\Update.exe", arguments="--processStart Discord.exe")
        else:
            print("-Vox: Warp bağlı değil. Bağlanıyorum... 🌐")
            os.system("warp-cli connect")
            time.sleep(3)
            print("-Vox: Discord açılıyor... 💬")
            os.startfile(r"C:\Users\Msi-nb\AppData\Local\Discord\Update.exe", arguments="--processStart Discord.exe")

    elif brawlhalla_var and discord_var:
        print("-Vox: Brawlhalla ve Discord açılıyor... ⚔️💬")
        os.startfile("steam://rungameid/291550")
        if warp_bagli_mi():
            print("-Vox: Discord açılıyor... 💬")
            os.startfile(r"C:\Users\Msi-nb\AppData\Local\Discord\Update.exe", arguments="--processStart Discord.exe")
        else:
            print("-Vox: Warp bağlı değil. Bağlanıyorum... 🌐")
            os.system("warp-cli connect")
            time.sleep(3)
            print("-Vox: Discord açılıyor... 💬")
            os.startfile(r"C:\Users\Msi-nb\AppData\Local\Discord\Update.exe", arguments="--processStart Discord.exe")

    elif spotify_var and discord_var:
        print("-Vox: Spotify ve Discord açılıyor... 🎧💬")
        os.system("spotify.exe")
        if warp_bagli_mi():
            print("-Vox: Discord açılıyor... 💬")
            os.startfile(r"C:\Users\Msi-nb\AppData\Local\Discord\Update.exe", arguments="--processStart Discord.exe")
        else:
            print("-Vox: Warp bağlı değil. Bağlanıyorum... 🌐")
            os.system("warp-cli connect")
            time.sleep(3)
            print("-Vox: Discord açılıyor... 💬")
            os.startfile(r"C:\Users\Msi-nb\AppData\Local\Discord\Update.exe", arguments="--processStart Discord.exe")

    elif spotify_var and brawlhalla_var:
        print("-Vox: Spotify ve Brawlhalla açılıyor... 🎧⚔️")
        os.system("spotify.exe")
        os.startfile("steam://rungameid/291550")

    elif spotify_var:
        print("-Vox: Spotify açılıyor... 🎧")
        os.system("spotify.exe")

    elif brawlhalla_var:
        print("-Vox: Brawlhalla açılıyor... ⚔️")
        os.startfile("steam://rungameid/291550")

    elif discord_var:
        if warp_bagli_mi():
            print("-Vox: Discord açılıyor... 💬")
            os.startfile(r"C:\Users\Msi-nb\AppData\Local\Discord\Update.exe", arguments="--processStart Discord.exe")
        else:
            print("-Vox: Warp bağlı değil. Bağlanıyorum... 🌐")
            os.system("warp-cli connect")
            time.sleep(3)
            print("-Vox: Discord açılıyor... 💬")
            os.startfile(r"C:\Users\Msi-nb\AppData\Local\Discord\Update.exe", arguments="--processStart Discord.exe")

    # Çıkış komutları
    elif cikis_var:
        print("-Vox: Görüşürüz 👋")
        break

    # Temizleme komutu
    elif mesaj in ["clean", "temizle", "clear", "cls"]:
        os.system("cls")
        continue

    # Diğer durumlar
    else:
        print("-Vox: Üzgünüm, bunu cevaplayamıyorum.")
