$ErrorActionPreference = "Stop"

Write-Host "==============================================" -ForegroundColor Yellow
Write-Host "   Generador de Instalador: JoinPDF" -ForegroundColor Yellow
Write-Host "==============================================" -ForegroundColor Yellow

Write-Host "`nPaso 1/4: Instalando dependencias de Python..." -ForegroundColor Cyan
pip install pypdf pyinstaller

Write-Host "`nPaso 2/4: Compilando script Python a .exe..." -ForegroundColor Cyan
pyinstaller --noconfirm --noconsole --onefile unir_seleccion.PY

Write-Host "`nPaso 3/4: Verificando Inno Setup..." -ForegroundColor Cyan
$isccPath64 = "${env:ProgramFiles(x86)}\Inno Setup 6\ISCC.exe"
$isccPath32 = "${env:ProgramFiles}\Inno Setup 6\ISCC.exe"
$isccPathUser = "${env:LOCALAPPDATA}\Programs\Inno Setup 6\ISCC.exe"

$isccPath = ""
if (Test-Path $isccPath64) {
    $isccPath = $isccPath64
} elseif (Test-Path $isccPath32) {
    $isccPath = $isccPath32
} elseif (Test-Path $isccPathUser) {
    $isccPath = $isccPathUser
}

if ($isccPath -eq "") {
    Write-Host "Inno Setup no esta instalado. Instalando a traves de winget..." -ForegroundColor Yellow
    winget install -e --id JRSoftware.InnoSetup --accept-package-agreements --accept-source-agreements
    
    if (Test-Path $isccPath64) {
        $isccPath = $isccPath64
    } elseif (Test-Path $isccPath32) {
        $isccPath = $isccPath32
    } elseif (Test-Path $isccPathUser) {
        $isccPath = $isccPathUser
    }
    
    if ($isccPath -eq "") {
        Write-Host "`n[ERROR] No se pudo encontrar Inno Setup tras la instalacion." -ForegroundColor Red
        Write-Host "Por favor, descargalo de https://jrsoftware.org/isdl.php, instalalo y vuelve a ejecutar este script." -ForegroundColor Yellow
        Pause
        exit
    }
}

Write-Host "`nPaso 4/4: Empaquetando en un Instalador Profesional..." -ForegroundColor Cyan
& $isccPath "joinpdf_setup.iss"

Write-Host "`n==============================================" -ForegroundColor Green
Write-Host "  [EXITO] Instalador creado correctamente!" -ForegroundColor Green
Write-Host "==============================================" -ForegroundColor Green
Write-Host "Se ha generado el archivo 'Instalar_Unir_PDF.exe' en esta carpeta." -ForegroundColor White
Write-Host "Ahora puedes eliminar la carpeta 'build', 'dist' y los otros scripts si lo deseas, o conservar el fuente." -ForegroundColor Gray
Write-Host ""
Pause
