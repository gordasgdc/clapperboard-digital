# clapperboard-digital — reguli de arhitectură

## [PARTEA 1: REGULI GLOBALE ECOSISTEM GDC]

**34. Semnare Windows (Code Signing) obligatorie la build — Self-Signed
ca implicit pentru testare internă, real (comercial) la lansare publică
(2026-09-06).** Cerut explicit de Cristi, după clarificarea (verificată
tehnic, nu presupusă) că un certificat self-signed NU elimină avertismentul
SmartScreen/"Unknown Publisher" pentru publicul larg — doar un certificat
real de la o CA publică (cu reputație acumulată) sau un certificat EV fac
asta; din iunie 2023, CA/Browser Forum obligă orice certificat OV/EV nou
să fie stocat pe token hardware/HSM cloud (Azure Trusted Signing, DigiCert
KeyLocker, SSL.com eSigner), NU ca `.pfx` exportabil. Decizie explicită
Cristi: self-signed ACUM (testare internă + cerc restrâns, cu `.cer`
importat manual de colaboratori în Trusted Root), evaluare Azure Trusted
Signing/EV la lansarea comercială publică — regula de mai jos NU
presupune că self-signed rezolvă SmartScreen pentru clienți finali, e
DOAR pentru etapa de testare.
- **Certificatul (privat, cu cheie) NU trece NICIODATĂ prin conversația cu
  Claude** — generarea (`New-SelfSignedCertificate`, doar posibilă pe
  Windows real, Claude nu poate rula asta de pe Mac) și încărcarea ca
  secret CI (`gh secret set`, valoare base64 a `.pfx` + parola) se fac
  DIRECT de Cristi, pe mașina lui Windows — identic cu regula deja
  existentă pentru parole/chei (Claude nu vede/manipulează credențiale).
- **CI-ul de build Windows verifică ÎNTÂI existența secretelor** (ex.
  `WIN_SELFSIGN_PFX_BASE64`/`WIN_SELFSIGN_PFX_PASSWORD`) — dacă lipsesc,
  build-ul continuă NESEMNAT (exact ca varianta Mac, `APPLE_SIGN_IDENTITY_APP`
  nesetat → semnare ad-hoc, niciodată o eroare de build). Dacă sunt
  prezente: decodează `.pfx`-ul temporar, semnează cu `signtool.exe`
  (localizat dinamic din Windows Kits, NU hardcodat o versiune) atât
  executabilul PyInstaller cât și installer-ul final Inno Setup, cu
  timestamp (`/tr .../td sha256`) ca semnătura să rămână validă și după
  expirarea certificatului, apoi ȘTERGE fișierul `.pfx` temporar de pe
  disc imediat după folosire.
- **Verificare post-semnare obligatorie în CI**: `Get-AuthenticodeSignature`
  (confirmă DOAR că fișierul are efectiv o semnătură atașată — nu
  `signtool verify /pa`, care validează lanțul de încredere complet și
  eșuează mereu pe un runner CI proaspăt, unde certificatul self-signed
  nu e importat în Trusted Root; asta e normal pentru testare internă,
  nu un eșec real) pe fiecare executabil semnat, ÎNAINTE ca pasul de
  build să fie considerat trecut — o semnare care "reușește" silențios
  dar produce un binar nesemnat/corupt nu trebuie să treacă drept succes.
  **[CORECȚIE 2026-09-06]**: prima implementare folosea `signtool verify
  /pa`, care a picat CI-ul chiar și după o semnare reușită — descoperit
  la primul test real, corectat imediat.
- **Exportul `.cer` (public, fără cheie privată)** se publică alături de
  installer (asset de release sau folder `dist/`) — colaboratorii îl
  importă o SINGURĂ dată în Trusted Root, apoi orice build viitor semnat
  cu ACELAȘI certificat (persistent via secret CI, NU regenerat la
  fiecare build — un cert nou la fiecare release ar rupe încrederea deja
  acordată) e automat de încredere pe mașinile lor.
- **Aplicare**: la fiecare build de release/actualizare Windows, pe orice
  aplicație din `~/Developer/` care produce un `.exe`/installer Windows —
  aplicată incremental, la următoarea atingere reală a fiecărui repo
  (Regula 11), nu retroactiv peste tot dintr-o sesiune dedicată.
- **Implementare de referință**: CGConvertor (`build-windows.spec` +
  `.github/workflows/build-windows.yml`, 2026-09-06) — vezi
  `codesigning/README-windows.md` din acel repo pentru pașii exacți pe
  care Cristi trebuie să-i ruleze o singură dată (generare cert + upload
  secret CI).

**Notă specifică acestui repo (2026-09-06)**: `clapperboard-digital` NU
are installer Inno Setup — CI-ul produce direct executabilul PyInstaller
(`dist/ClapperboardDigital.exe`), publicat ca atare pe GitHub Release.
Regula de mai sus se aplică deci cu UN SINGUR pas de semnare (executabilul
final), nu doi (executabil + installer) ca la aplicațiile GDC care au un
installer Inno Setup separat — vezi `codesigning/README-windows.md` din
acest repo.

**35. Fluxul de actualizare se VERIFICĂ pe client real, nu se presupune —
obligatoriu la FIECARE release (2026-09-11).** Cerut explicit de Cristi după
un caz real: un client a trimis o captură în care GDC Plugin Manager v1.27.0
arăta „Sunteți pe cea mai nouă versiune", deși live era 1.30.0. Auditul a
găsit **trei defecte independente**, toate invizibile din repo — codul era
corect, `update.json` din repo era corect, dar clientul instalat tot nu primea
nimic:

1. **Schimbarea formatului `update.json` rupe clienții deja instalați.** Pe
   2026-09-03 fișierul a trecut de la un câmp `version` la rădăcină la secțiuni
   separate `mac`/`windows`. Clienții ≤1.27 decodează `version` și
   `download_url` ca fiind OBLIGATORII de la rădăcină → `JSONDecoder` aruncă →
   verificarea eșuează **TĂCUT** și cade pe „ești la zi". Nu apare nicio
   eroare, nicăieri. Erau blocați permanent, fără nicio cale de ieșire în
   afară de reinstalare manuală — pe care n-aveau de unde s-o bănuiască.
2. **Oglinda servită public rămâne în urma sursei din repo.** `gordas.dev` e
   servit din `gdc-plugin-manager-catalog-vendor/docs/`, unde fiecare aplicație
   are o COPIE a lui `update.json`. Un bump în repo-ul aplicației NU actualizează
   oglinda. Găsite în urmă cu până la 3 versiuni (datamover 2.11.0 vs 2.14.0,
   gdc-production-manager 2.0.2 vs 2.0.4, media-flow-monitor 1.9.1 vs 1.9.3).
3. **`releases/latest` nu pointează unde crezi.** Un release nou care n-are
   asset pentru o platformă lasă linkul stabil al acelei platforme mort (404),
   sau „latest" rămâne pe un release mai vechi și clientul descarcă o versiune
   anterioară celei anunțate.

**Regula, obligatorie înainte de a declara ORICE release ca fiind gata:**

- **Rulează verificatorul**, nu bifa din memorie:
  `~/Developer/_gdc-tools/verify-update-flow.sh <update_url> <versiune> [link_stabil...]`
  Verifică live: fișierul e accesibil, e JSON valid, versiunea SERVITĂ e chiar
  cea publicată, câmpurile de compatibilitate pentru clienții vechi există, și
  fiecare link stabil răspunde 200 real (urmărind redirectările GitHub).
- **Formatul `update.json` nu se schimbă niciodată eliminând câmpuri.** Orice
  câmp pe care o versiune publicată îl decodează ca obligatoriu rămâne în fișier
  PENTRU TOTDEAUNA, chiar dacă versiunile noi nu-l mai folosesc. Un câmp nou se
  adaugă pe lângă, niciodată în locul celui vechi. Costul e câțiva octeți;
  alternativa e o categorie întreagă de clienți blocată definitiv, în tăcere.
- **Când un singur câmp de versiune deservește ambele platforme**, valoarea e
  MINIMUL dintre ele — niciodată maximul. Altfel o platformă e trimisă spre o
  versiune care nu există pentru ea.
- **Oglinda de pe `gordas.dev` se sincronizează în același commit** cu bump-ul
  din repo-ul aplicației. Un `update.json` corect în repo, dar vechi pe server,
  e exact la fel de rupt ca unul greșit.
- **După publicare, verifică pe release-ul REAL** că `releases/latest`
  pointează la tag-ul nou ȘI că are asset pentru FIECARE platformă pe care
  `update.json` o anunță. Un release doar-Windows face 404 linkul Mac, deși
  nimic din repo nu arată asta.
- **Un update checker nu trebuie să eșueze tăcut.** La orice atingere a
  codului de verificare, o eroare de rețea/decodare se loghează explicit
  (`DiagnosticLog`, Regula 25) — „n-am putut verifica" și „ești la zi" sunt
  două stări diferite și nu trebuie să arate identic utilizatorului.

**36. Verificările se automatizează, nu se țin minte — `~/Developer/_gdc-tools/`
(2026-09-11).** Cerut explicit de Cristi, după ce trei defecte de release au
trecut neobservate deși toate regulile existau scrise: *"să nu depinzi de
memorie, să-ți creezi tot timpul acea structură automatizată"*.

Motivul e concret: o regulă scrisă într-un jurnal de 1000 de linii e bifată
din memorie, iar memoria ratează exact cazurile rare — cele care produc
bug-uri. O verificare rulată produce un rezultat, nu o impresie.

**Uneltele existente** (comune tuturor repo-urilor, nu duplicate per proiect):
- **`preflight-release.sh`** — rulat în rădăcina oricărui repo GDC înainte de
  a declara un release gata. Verifică automat Regulile 32 (zero atribuire
  Claude), 14 (versiuni sincronizate în toate fișierele care le țin), 25
  (CHANGELOG actualizat), 29 (zero informație internă în notele publice) și
  23 (`dist/` deținut de root).
  `cd ~/Developer/<Repo> && ~/Developer/_gdc-tools/preflight-release.sh [versiune]`
- **`verify-update-flow.sh`** — Regula 35, verificare live a fluxului de
  actualizare (fișier accesibil, versiune servită, compatibilitate cu clienții
  vechi, linkuri stabile 200 real).
- **`clean-claude-attribution.sh`** — curățarea istoricului (Regula 32).

**Regula de lucru:**
- Înainte de a raporta un release ca fiind gata, rulează preflight-ul ȘI
  verificatorul de update. Un „am verificat" fără ieșirea comenzii nu e o
  verificare.
- **Orice bug de proces descoperit devine o verificare în unealtă**, în aceeași
  sesiune — nu doar un paragraf nou de jurnal. Dacă un defect a putut trece o
  dată, va trece din nou; singura apărare care ține este una executabilă.
- Uneltele trăiesc într-un singur loc (`~/Developer/_gdc-tools/`), niciodată
  copiate per repo — o copie divergentă e mai rea decât lipsa ei.
- Ieșirea lor e în română, explicită, și spune ce anume să faci la eșec, nu
  doar că ceva e greșit.
- **Versionate pe GitHub** (`gordasgdc/gdc-tools`, repo PRIVAT — conțin detalii
  interne de proces, Regula 29). Pe o mașină nouă:
  `git clone git@github.com:gordasgdc/gdc-tools.git ~/Developer/_gdc-tools`.
  Orice verificare nouă se comite acolo, nu rămâne doar local — o unealtă care
  trăiește pe un singur disc e la o defecțiune distanță de a nu mai exista.
- **`audit-ecosystem.sh`** (a treia unealtă) — compară, pentru toate
  aplicațiile deodată, versiunea din COD cu cea PUBLICATĂ. Diferența dintre
  ele e exact ce vede (sau nu vede) clientul.
- **Un fals pozitiv se repară imediat**, nu se tolerează: ascunde golurile
  adevărate în zgomot. (Prima rulare a `audit-ecosystem.sh` raporta „?" la
  cinci aplicații doar fiindcă nu știa unde își țin versiunea — reparat în
  aceeași sesiune.)

## Etapa 2026-09-11 — v1.2.1 publicat cu semnare Windows activa

Secretele CI (`WIN_SELFSIGN_PFX_BASE64`/`WIN_SELFSIGN_PFX_PASSWORD`,
certificat COMUN ecosistemului) erau deja incarcate de Cristi. Acest release
e primul in care semnarea Regulii 34 chiar a rulat pe un build real.

Verificat direct, nu presupus: pasul de semnare marcat OK in lista de pasi a
job-ului, plus directorul de securitate din header-ul PE al installer-ului
descarcat = 7496 bytes de semnatura Authenticode (acelasi certificat +
timestamp pe toate aplicatiile). Link stabil `releases/latest/download/...`
verificat HTTP 200.

**Bug preexistent gasit si reparat pe drum**: `APP_VERSION` din
`backend/config.py` ramasese blocat la 1.0.0 din commit-ul initial, desi
tag-urile ajunsesera la 1.2.0 - fereastra About arata o versiune gresita de
mai multe release-uri. Sincronizat la 1.2.1.
