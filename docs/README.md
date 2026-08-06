# 🎬 Clapperboard Digital (PWA)

Clapetă digitală pentru platoul de filmare — instalabilă pe telefon, funcționează offline, fără cont sau server.

**Live**: https://gordasgdc.github.io/clapperboard-digital/

---

## 📲 Instalare pe telefon

### iPhone (Safari)
1. Deschide https://gordasgdc.github.io/clapperboard-digital/
2. Apasă butonul de **Share** (pătrat cu săgeată în sus)
3. Alege **"Adaugă pe ecranul de pornire"**

### Android (Chrome)
1. Deschide linkul de mai sus
2. Apasă bannerul **"Instalează"** care apare automat, sau
3. Meniul ⋮ → **"Adaugă pe ecranul de pornire" / "Instalează aplicația"**

După instalare, aplicația se deschide instant, ca orice altă aplicație de pe telefon — inclusiv fără semnal.

## 🚀 Caracteristici

- **Câmpuri rapide** — Proiect, Scenă, Take, Regizor, Cameră, Notițe
- **Take +/−** — butoane mari, ușor de atins
- **CLAP** — un singur buton mare: înregistrează take-ul curent (cu sunet și vibrație), apoi avansează automat la următorul
- **Cod QR** — generat automat, cu toate informațiile filmării, actualizat live
- **Dată și oră live** — afișate în interfață, actualizate în fiecare secundă; incluse automat în codul QR și în fiecare intrare din istoric, pentru sincronizare precisă în montaj
- **Istoric** — toate take-urile înregistrate, salvate local pe telefon; atinge o intrare pentru a reîncărca acele informații
- **Contor Take X/Y** — arată take-ul curent față de totalul înregistrat pentru acel proiect/scenă
- **Ecran complet** — clapeta ocupă tot ecranul, gata de filmat
- **Scurtături tastatură** (utile la testare pe desktop): `+` / `-` pentru take, `spațiu` pentru CLAP, `f` pentru ecran complet, `h` pentru istoric, `Esc` pentru ieșire
- **Funcționează offline** — după prima încărcare, aplicația rulează fără internet
- **Salvare automată** — toate câmpurile și istoricul se păstrează între sesiuni, local pe dispozitiv
- **100% local** — nimic nu e trimis către niciun server; toate datele stau în `localStorage`, pe telefonul tău

## 🛠️ Tehnologii

- HTML + CSS + JavaScript vanilla — un singur fișier (`index.html`), fără framework
- [qrcode.js](https://github.com/soldair/node-qrcode) (CDN) pentru generarea codului QR
- `localStorage` pentru persistență (stare curentă + istoric)
- Web Audio API pentru sunetul de clapetă (sintetizat, fără fișier audio extern)
- Service Worker (`sw.js`) pentru funcționare offline
- Web App Manifest (`manifest.json`) pentru instalare ca aplicație nativă

## 📁 Structura

```
docs/
├── index.html      # aplicația completă (HTML + CSS + JS)
├── manifest.json    # configurație PWA (nume, iconițe, culori)
├── sw.js             # Service Worker (cache pentru offline)
├── icon-192.png     # iconiță PWA 192×192
└── icon-512.png     # iconiță PWA 512×512
```

Găzduită direct din folderul `docs/` al acestui repository, via GitHub Pages.

## 💻 Rulare locală (dezvoltare)

Orice server static funcționează — de exemplu:

```bash
cd docs
python3 -m http.server 8000
```

Apoi deschide `http://localhost:8000`. Service Worker-ul necesită HTTPS sau `localhost` ca să funcționeze (limitare standard de browser).

## ⚠️ Notă despre datele salvate

Istoricul și câmpurile curente sunt salvate în `localStorage`, **specific fiecărui browser și dispozitiv**. Ștergerea datelor de navigare sau dezinstalarea aplicației șterge și istoricul. Nu există sincronizare între dispozitive — dacă ai nevoie de asta, aplicația desktop **GDC Production Manager** oferă export/import de date.

## 👤 Autor

**Cristi Gordas (GDC)** — colorist și editor video

- [GitHub](https://github.com/gordasgdc)
- [Facebook](https://web.facebook.com/cristiGDC)
- [YouTube](https://www.youtube.com/@cristigordas)

## 📄 Licență

MIT — vezi [LICENSE](../LICENSE) din rădăcina repository-ului.
