; ============================================================
;  GELİR GİDER TAKİBİ - Inno Setup Script
;  SEYIR 7 ENTEGRE SISTEMLER
;  Surum: 4.0   (Inno Setup 7 uyumlu)
; ============================================================

#define MyAppName "GELİR GİDER TAKİBİ"
#define MyAppVersion "4.0"
#define MyAppPublisher "SEYİR 7 ENTEGRE SİSTEMLER"
#define MyAppURL "https://github.com/seyir7entegresistemler"
#define MyAppExeName "GelirGider.exe"

[Setup]
; --- Kimlik ---
AppId={{8F3A2B1C-9D4E-4F5A-B6C7-D8E9F0A1B2C3}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}

; --- Kurulum ayarları ---
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
AllowNoIcons=yes

; --- Kurulum klasörü seçme adımı AÇIK ---
DisableDirPage=no

; --- Sıkıştırma ---
Compression=lzma2/ultra64
SolidCompression=yes
LZMANumBlockThreads=4

; --- Görsel / İkon ---
SetupIconFile=icons\images.ico
UninstallDisplayIcon={app}\{#MyAppExeName}
WizardStyle=modern

; --- Çıktı ---
OutputDir=dist_installer
OutputBaseFilename=GELIRGIDER_TAKIBI_v4.0_Setup
PrivilegesRequired=admin
ArchitecturesInstallIn64BitMode=x64compatible

; --- Lisans / Bilgi (boş bırakıldı) ---

[Languages]
Name: "turkish"; MessagesFile: "compiler:Languages\Turkish.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; Ana EXE
Source: "GelirGider.exe"; DestDir: "{app}"; Flags: ignoreversion

; İkonlar
Source: "icons\*"; DestDir: "{app}\icons"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\icons\images.ico"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\icons\images.ico"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{app}\gelirgider"
Type: filesandordirs; Name: "{app}\icons"

[Code]
// ============================================================
//  SON ADIMDA ÖZEL MESAJ
// ============================================================
procedure CurPageChanged(CurPageID: Integer);
begin
  if CurPageID = wpFinished then
  begin
    WizardForm.FinishedLabel.Caption :=
      'Kurulum tamamlandı!' + #13#10 + #13#10 +
      'GELİR GİDER TAKİBİ v4.0' + #13#10 +
      'SEYİR 7 ENTEGRE SİSTEMLER' + #13#10 + #13#10 +
      'KAZANCINIZ BOL BEREKETLİ VE DAİMA OLSUN!';
  end;
end;