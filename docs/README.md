# 🎬 Clapperboard Digital (PWA)

Clachetă digitală pentru platoul de filmare — instalabilă pe telefon, funcționează offline, fără cont sau server. Ecranul principal **este** clacheta: timecode mare, proiect, scenă, take, cameră, dată și oră — gata de filmat.

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

Instalată, aplicația se deschide fără bara de browser (mod `standalone`) — cel mai apropiat lucru de "ecran complet automat" pe care browserele îl permit fără o atingere a utilizatorului.

## 🚀 Caracteristici

- **Clacheta ocupă tot ecranul** — timecode, proiect, scenă, take, cameră, dată/oră, totul mare și lizibil de la distanță
- **Timecode real** (HH:MM:SS:FF, 24/25/30 fps) — avansează live, sincronizat cu ceasul telefonului; poate fi **setat manual** (jam-sync) atingând timecode-ul, pentru sincronizare cu camera
- **CLAP** — înregistrează take-ul curent (sunet sintetizat + vibrație), apoi avansează automat la următorul
- **Sunet îmbunătățit** — Web Audio API, funcționează pe iPhone și Android, cu un "thump" de joasă frecvență adăugat pentru claritate pe difuzoarele mici de telefon
- **Editare rapidă** — atinge ✏️ sau orice rând (proiect/scenă/cameră) pentru a completa informațiile, fără să părăsești clacheta
- **Ecran complet** — se activează la prima atingere a ecranului (browserele nu permit activarea automată fără gest); ESC sau atingerea fundalului clachetei iese din mod
- **Cod QR** — acum într-un panou dedicat (▦), conține proiect/scenă/take/timecode/dată/oră
- **Istoric** — toate take-urile, cu timecode, salvate local; atinge o intrare pentru a reîncărca acele date
- **Export metadate** (⤓) — CSV (gândit pentru import parțial în DaVinci Resolve) sau JSON, cu toate take-urile înregistrate
- **Funcționează offline**, salvare automată în `localStorage`, 100% local

## 📤 Export metadate pentru DaVinci Resolve

Fișierul CSV exportat are coloanele: `File Name, Project, Scene, Take, Timecode, Date, Time, Director, Camera, Notes`.

**Important de știut**: coloana `File Name` rămâne goală. Clacheta digitală nu are acces la fișierele tale video (rulează într-un browser, izolat de sistemul de fișiere), deci nu poate ști automat ce nume de fișier corespunde fiecărui take. După ingest, completează manual acea coloană cu numele fișierelor corespunzătoare, apoi folosește **Media Pool → Metadata → Import** din Resolve pentru a asocia rândurile cu clipurile. E un pas manual, dar fișierul îți oferă deja toate celelalte informații structurate, gata de asociat.

Dacă preferi să scrii propriul script de ingest/matching, JSON-ul exportat conține aceleași date, structurat, fără ambiguități de formatare CSV.

## ⌨️ Scurtături tastatură (utile la testare pe desktop)

| Tastă | Acțiune |
|---|---|
| `+` / `-` | Take următor / anterior |
| `spațiu` | CLAP |
| `f` | Ecran complet / ieșire |
| `h` | Istoric |
| `Esc` | Închide panoul deschis / iese din ecran complet |

## 🛠️ Tehnologii

- HTML + CSS + JavaScript vanilla — un singur fișier (`index.html`)
- [qrcode.js](https://github.com/soldair/node-qrcode) (CDN) pentru codul QR
- `localStorage` pentru persistență (stare curentă + istoric)
- Web Audio API pentru sunetul de clapetă (sintetizat, fără fișier audio extern)
- Fullscreen API pentru ecran complet (browsere care o suportă)
- Service Worker (`sw.js`, network-first pentru `index.html`) pentru offline + actualizări mereu curente
- Web App Manifest (`manifest.json`) pentru instalare ca aplicație nativă

## 📁 Structura

```
docs/
├── index.html      # aplicația completă (HTML + CSS + JS)
├── manifest.json    # configurație PWA
├── sw.js             # Service Worker
├── icon-192.png
└── icon-512.png
```

## 💻 Rulare locală (dezvoltare)

```bash
cd docs
python3 -m http.server 8000
```

Apoi deschide `http://localhost:8000`. Service Worker-ul necesită HTTPS sau `localhost`.

## ⚠️ Limitări de platformă

- **Ecran complet automat la deschidere** nu e posibil tehnic în niciun browser fără o atingere a utilizatorului — de-asta clacheta intră în ecran complet la prima atingere, nu instant la încărcare. Instalată ca PWA, rulează deja fără bara de browser.
- **Timecode-ul** e generat de telefon, nu citit dintr-o cameră fizică — folosește "Setează timecode" pentru jam-sync manual dacă ai nevoie de precizie față de camera ta.
- Istoricul și câmpurile sunt salvate **per dispozitiv/browser**, fără sincronizare între telefoane.

## 👤 Autor

**Cristi Gordas (GDC)** — colorist și editor video

- [GitHub](https://github.com/gordasgdc)
- [Facebook](https://web.facebook.com/cristiGDC)
- [YouTube](https://www.youtube.com/@cristigordas)

## 📄 Licență

MIT — vezi [LICENSE](../LICENSE) din rădăcina repository-ului.
