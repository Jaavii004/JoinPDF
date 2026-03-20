[Setup]
AppName=JoinPDF
AppVersion=1.3
AppPublisher=Jaavii004
DefaultDirName={autopf}\JoinPDF
DefaultGroupName=JoinPDF
UninstallDisplayIcon={app}\unir_seleccion.exe
Compression=lzma2
SolidCompression=yes
OutputDir=.\
OutputBaseFilename=Instalar_JoinPDF
ArchitecturesInstallIn64BitMode=x64
DisableProgramGroupPage=yes
PrivilegesRequired=admin
; Para que no lance el programa al terminar la instalacion ya que es un script silencioso
DisableReadyPage=yes

[Files]
Source: "dist\unir_seleccion.exe"; DestDir: "{app}"; Flags: ignoreversion

[Registry]
; Solucionar el limite de 15 archivos a 100
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Explorer"; ValueType: dword; ValueName: "MultipleInvokePromptMinimum"; ValueData: "100"; Flags: uninsdeletevalue
Root: HKLM; Subkey: "Software\Microsoft\Windows\CurrentVersion\Explorer"; ValueType: dword; ValueName: "MultipleInvokePromptMinimum"; ValueData: "100"; Flags: uninsdeletevalue

; 1. REGISTRO EN EL MANIPULADOR ACTUAL (MSEdgePDF) - MAS FIABLE
Root: HKCU; Subkey: "Software\Classes\MSEdgePDF\shell\JoinPDF"; ValueType: string; ValueData: "JoinPDF"; Flags: uninsdeletekey
Root: HKCU; Subkey: "Software\Classes\MSEdgePDF\shell\JoinPDF"; ValueType: string; ValueName: "Icon"; ValueData: """{app}\unir_seleccion.exe"""; Flags: uninsdeletevalue
Root: HKCU; Subkey: "Software\Classes\MSEdgePDF\shell\JoinPDF\command"; ValueType: string; ValueData: """{app}\unir_seleccion.exe"" ""%1"""; Flags: uninsdeletekey

; 2. REGISTRO UNIVERSAL EN '*' (COMO ANTIGRAVITY Y VS CODE)
; Se registra sin MUIVerb (usando el valor predeterminado) para mayor compatibilidad
Root: HKCU; Subkey: "Software\Classes\*\shell\JoinPDF"; ValueType: string; ValueData: "JoinPDF"; Flags: uninsdeletekey
Root: HKCU; Subkey: "Software\Classes\*\shell\JoinPDF"; ValueType: string; ValueName: "Icon"; ValueData: """{app}\unir_seleccion.exe"""; Flags: uninsdeletevalue
Root: HKCU; Subkey: "Software\Classes\*\shell\JoinPDF"; ValueType: string; ValueName: "AppliesTo"; ValueData: ".pdf"; Flags: uninsdeletevalue
Root: HKCU; Subkey: "Software\Classes\*\shell\JoinPDF\command"; ValueType: string; ValueData: """{app}\unir_seleccion.exe"" ""%1"""; Flags: uninsdeletekey

; 3. REGISTRO EN SYSTEM FILE ASSOCIATIONS (PARA TODOS LOS USUARIOS)
Root: HKLM; Subkey: "Software\Classes\SystemFileAssociations\.pdf\shell\JoinPDF"; ValueType: string; ValueData: "JoinPDF"; Flags: uninsdeletekey
Root: HKLM; Subkey: "Software\Classes\SystemFileAssociations\.pdf\shell\JoinPDF"; ValueType: string; ValueName: "Icon"; ValueData: """{app}\unir_seleccion.exe"""; Flags: uninsdeletevalue
Root: HKLM; Subkey: "Software\Classes\SystemFileAssociations\.pdf\shell\JoinPDF\command"; ValueType: string; ValueData: """{app}\unir_seleccion.exe"" ""%1"""; Flags: uninsdeletekey

[Code]
// Muestra un mensaje al finalizar la instalacion
procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    MsgBox('Instalacion completada.' + #13#10 + #13#10 + 'Ahora puedes seleccionar 2 o mas archivos PDF, hacer clic derecho y pulsar en "JoinPDF".', mbInformation, MB_OK);
  end;
end;
