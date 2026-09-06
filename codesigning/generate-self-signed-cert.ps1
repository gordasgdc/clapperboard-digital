# generate-self-signed-cert.ps1
#
# IMPORTANT: certificatul de Code Signing self-signed e COMUN pentru toate
# aplicatiile GDC (vezi CLAUDE.md, Regula 34) - daca l-ai generat deja
# pentru alta aplicatie (ex. CGConvertor), NU rula acest script din nou
# aici. In loc, doar incarca ACELASI .pfx ca secrete pentru ACEST repo
# (comenzile de mai jos, cu --repo schimbat) - certificatul ramane
# identic, colaboratorii care au importat deja .cer-ul in Trusted Root
# nu trebuie sa repete nimic.
#
# Ruleaza acest script DOAR daca certificatul comun GDC inca nu exista
# (prima aplicatie din ecosistem care are nevoie de semnare Windows).
# Rulat O SINGURA DATA, de Cristi, pe Windows real (nu de Claude - un
# certificat cu cheie privata nu trece niciodata prin conversatie).
# Genereaza un certificat Self-Signed de Code Signing STABIL (valabil 5
# ani) - NU se regenereaza la fiecare build, ca sa nu rupa increderea
# deja acordata de colaboratori.
#
# Foloseste:
#   1. Ruleaza acest script o data (PowerShell, ca Administrator).
#   2. Produce doua fisiere in acelasi folder:
#      - gdc-selfsign.pfx  (PRIVAT, cu cheie - NU se distribuie,
#        NU se comite in git, NU se lipeste in chat/conversatie)
#      - gdc-selfsign.cer  (PUBLIC, fara cheie - se distribuie
#        colaboratorilor pentru import manual in Trusted Root)
#   3. Incarca .pfx-ul ca secrete GitHub Actions (comenzile exacte sunt
#      afisate la finalul scriptului) - pentru ACEST repo SI pentru orice
#      alt repo GDC care produce un .exe Windows (aceleasi nume de secret
#      peste tot: WIN_SELFSIGN_PFX_BASE64 / WIN_SELFSIGN_PFX_PASSWORD).

$ErrorActionPreference = "Stop"

$subject = "CN=GDC (Self-Signed, testare interna)"
$pfxPath = Join-Path $PSScriptRoot "gdc-selfsign.pfx"
$cerPath = Join-Path $PSScriptRoot "gdc-selfsign.cer"
$pfxPassword = Read-Host -Prompt "Alege o parola noua pentru fisierul .pfx (o vei pune ca secret CI)" -AsSecureString

Write-Host "==> Generez certificatul self-signed (valabil 5 ani)..."
$cert = New-SelfSignedCertificate `
    -Type CodeSigningCert `
    -Subject $subject `
    -CertStoreLocation "Cert:\CurrentUser\My" `
    -NotAfter (Get-Date).AddYears(5) `
    -KeyUsage DigitalSignature `
    -KeyAlgorithm RSA `
    -KeyLength 2048

Write-Host "==> Exporting .pfx (PRIVAT - nu distribui acest fisier)..."
Export-PfxCertificate -Cert $cert -FilePath $pfxPath -Password $pfxPassword | Out-Null

Write-Host "==> Exporting .cer (PUBLIC - acesta se distribuie colaboratorilor)..."
Export-Certificate -Cert $cert -FilePath $cerPath | Out-Null

Write-Host ""
Write-Host "==> Gata:"
Write-Host "    $pfxPath  (PRIVAT - foloseste-l DOAR pentru pasii de mai jos, apoi sterge-l local)"
Write-Host "    $cerPath  (PUBLIC - trimite-l colaboratorilor)"
Write-Host ""
Write-Host "==> Urmatorul pas - incarca secretele in GitHub Actions (necesita 'gh' CLI autentificat):"
Write-Host ""
Write-Host '    $b64 = [Convert]::ToBase64String([IO.File]::ReadAllBytes("' -NoNewline
Write-Host "$pfxPath" -NoNewline
Write-Host '"))'
Write-Host '    gh secret set WIN_SELFSIGN_PFX_BASE64 --repo gordasgdc/clapperboard-digital --body $b64'
Write-Host '    gh secret set WIN_SELFSIGN_PFX_PASSWORD --repo gordasgdc/clapperboard-digital'
Write-Host "    (al doilea comand cere parola interactiv - foloseste ACEEASI parola aleasa mai sus)"
Write-Host ""
Write-Host "==> Repeta cele doua comenzi 'gh secret set' de mai sus (cu --repo schimbat) pentru"
Write-Host "    ORICE alt repo GDC care produce un .exe Windows - ACELASI .pfx, acelasi b64."
Write-Host ""
Write-Host "==> Dupa ce secretele sunt incarcate, sterge fisierul .pfx local:"
Write-Host "    Remove-Item `"$pfxPath`" -Force"
Write-Host ""
Write-Host "==> Distribuie $cerPath colaboratorilor. Import manual pe masinile lor:"
Write-Host "    dublu-click pe .cer -> Install Certificate -> Local Machine ->"
Write-Host "    'Place all certificates in the following store' -> Trusted Root Certification Authorities."
