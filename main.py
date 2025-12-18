selam = ["selam", "merhaba"]
hal = ["nasılsın", "naber", "ne", "haber"]

while True:
    m = input("Sen: ")
    mesaj = m.lower()
    kelimeler = mesaj.split()

    selam_var = False
    hal_var = False

    for kelime in kelimeler:
        if kelime in selam:
            selam_var = True
        if kelime in hal:
            hal_var = True

    if selam_var and hal_var:
        print("Vox: Selam! İyiyim, teşekkürler. Sen nasılsın?")
    elif selam_var:
        print("Vox: Selam! Nasılsın?")
    elif hal_var:
        print("Vox: İyiyim, teşekkürler. Sen nasılsın?")
    elif mesaj in ["çık", "exit", "quit"]:
        print("Vox: Görüşürüz 👋")
        break
    else:
        print("Vox: Anlamadım, lütfen tekrar eder misin?")
