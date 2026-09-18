# clapperboard-digital — reguli de arhitectură

## [PARTEA 1: REGULI GLOBALE ECOSISTEM GDC] — mutată în `~/Developer/CLAUDE.md`

> Din 2026-09-18, regulile globale stau într-un singur fișier,
> `~/Developer/CLAUDE.md`, citit automat de Claude Code în orice proiect din
> `~/Developer/`. Nu se mai copiază aici. Ce era specific acestui repo în fosta
> Partea 1 (statusuri, excepții) e la finalul fișierului.

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

### Completări specifice acestui repo, mutate din fosta Partea 1 (2026-09-18)

Păstrate verbatim. Regula generală la care se referă fiecare e în
`~/Developer/CLAUDE.md`.

**Regula 34:**

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
