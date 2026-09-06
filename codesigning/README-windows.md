# codesigning/ — semnare Windows (Self-Signed, testare internă)

Acest folder acoperă semnarea codului pentru build-ul Windows al
Clapperboard Digital (CLAUDE.md, Regula 34 — regulă globală GDC).

## De ce Self-Signed, și ce NU rezolvă

Un certificat self-signed **nu elimină avertismentul SmartScreen/"Unknown
publisher"** pentru publicul larg — doar un certificat real de la o CA
publică (cu reputație acumulată) sau un certificat EV fac asta. Self-signed
e util STRICT pentru:
- testare internă (buildurile pe care le rulează Cristi însuși),
- distribuire către un cerc restrâns de colaboratori care importă manual
  certificatul public (`.cer`) în Trusted Root o singură dată.

La lansarea comercială publică, planul e Azure Trusted Signing sau un
certificat EV (HSM cloud) — vezi CLAUDE.md Regula 34 pentru context complet.

## Certificatul e COMUN pentru toate aplicațiile GDC

Secretele CI se numesc IDENTIC în toate repo-urile:
`WIN_SELFSIGN_PFX_BASE64` și `WIN_SELFSIGN_PFX_PASSWORD`. Dacă certificatul
a fost deja generat pentru o altă aplicație din ecosistem (ex. CGConvertor),
**NU se generează unul nou aici** — se încarcă doar ACELAȘI `.pfx` ca
secrete pentru ACEST repo (`gh secret set ... --repo gordasgdc/
clapperboard-digital`). Colaboratorii care au importat deja `.cer`-ul în
Trusted Root nu trebuie să repete nimic.

## Setup unic (o dată, făcut DIRECT de Cristi pe Windows real)

Certificatul (privat, cu cheie) nu trece niciodată prin conversația cu
Claude — la fel ca orice altă parolă/cheie din ecosistem.

1. Dacă certificatul comun GDC NU există încă, pe Windows real (Parallels
   e suficient), deschide PowerShell **ca Administrator** și rulează:
   ```powershell
   .\codesigning\generate-self-signed-cert.ps1
   ```
   Scriptul cere o parolă nouă (pentru `.pfx`) și produce două fișiere:
   - `gdc-selfsign.pfx` — **PRIVAT**, nu se distribuie, nu se comite în git.
   - `gdc-selfsign.cer` — **PUBLIC**, se distribuie colaboratorilor.

   Dacă certificatul EXISTĂ deja (generat pentru altă aplicație GDC),
   sari direct la pasul 2, folosind `.pfx`-ul deja existent.

2. Încarcă `.pfx`-ul ca secrete GitHub Actions pentru ACEST repo
   (necesită `gh` CLI autentificat pe acea mașină):
   ```powershell
   gh secret set WIN_SELFSIGN_PFX_BASE64 --repo gordasgdc/clapperboard-digital --body $b64
   gh secret set WIN_SELFSIGN_PFX_PASSWORD --repo gordasgdc/clapperboard-digital
   ```

3. Șterge `.pfx`-ul local imediat după (`Remove-Item gdc-selfsign.pfx -Force`)
   — rămâne doar în secretele CI, criptate.

4. Distribuie `.cer`-ul colaboratorilor (dacă nu a fost deja distribuit
   pentru altă aplicație GDC). Pe fiecare mașină a lor, o singură dată:
   dublu-click → **Install Certificate** → **Local Machine** → "Place all
   certificates in the following store" → **Trusted Root Certification
   Authorities**.

Odată făcuți pașii 1-4, **fiecare build viitor din CI** (`git push
origin vX.Y.Z`) semnează automat executabilul cu ACELAȘI certificat —
colaboratorii nu mai trebuie să reimporte nimic la versiunile următoare.

## Ce face CI-ul automat (`.github/workflows/build-windows.yml`)

- Dacă secretele NU sunt setate: build-ul continuă **nesemnat**, exact ca
  până acum — nicio eroare, nicio schimbare de comportament.
- Dacă secretele SUNT setate: după ce `ClapperboardDigital.exe`
  (PyInstaller) există, e semnat cu `signtool.exe` (localizat dinamic din
  Windows Kits, cu timestamp), apoi verificat cu `Get-AuthenticodeSignature`
  — confirmă DOAR că semnătura a fost atașată corect, fără să ceară lanț de
  încredere complet (asta ar eșua mereu pe un runner CI proaspăt, care nu
  are certificatul în Trusted Root — normal pentru self-signed, nu un bug).
  Un eșec real de semnare (fișier fără nicio semnătură) tot oprește
  build-ul (CI roșu).

**Notă privind formatul de distribuție**: acest repo NU are un installer
Inno Setup — CI-ul produce direct executabilul PyInstaller
(`dist/ClapperboardDigital.exe`), atașat ca atare la GitHub Release. De
aceea există un singur pas de semnare (executabilul), nu doi (executabil +
installer) ca la aplicațiile GDC care au installer Inno Setup separat.

## Regenerarea certificatului (dacă expiră sau e compromis)

Rulează din nou `generate-self-signed-cert.ps1`, reîncarcă secretele
(pasul 2 de mai sus îi suprascrie pe cei vechi) — pentru TOATE repo-urile
GDC care folosesc certificatul comun — dar **toți colaboratorii trebuie să
reimporte noul `.cer`**, altfel văd din nou avertismentul pentru versiunile
semnate cu noul certificat. Evită regenerarea inutilă — de asta scriptul
folosește o valabilitate de 5 ani.
