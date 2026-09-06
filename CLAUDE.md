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
