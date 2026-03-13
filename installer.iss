; installer.iss
; =============
; Inno Setup 6 script for XpertAI CMS Windows Installer
;
; Prerequisites:
;   - Run build_installer.bat first to produce cms-backend\dist\CMS_Server\
;   - Inno Setup 6  https://jrsoftware.org/isinfo.php
;
; Compile with:
;   "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer.iss

#define AppName      "XpertAI CMS"
#define AppVersion   "1.0.0"
#define AppPublisher "XpertAI Global"
#define AppExeName   "CMS_Server.exe"
#define AppURL       "http://127.0.0.1:8000"

[Setup]
; Basic info
AppId={{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher={#AppPublisher}
AppPublisherURL={#AppURL}
AppSupportURL={#AppURL}
AppUpdatesURL={#AppURL}

; Install to Program Files
DefaultDirName={autopf}\{#AppName}
DefaultGroupName={#AppName}

; Output
OutputDir=Output
OutputBaseFilename=CMS_Setup
SetupIconFile=

; Compression
Compression=lzma2/ultra64
SolidCompression=yes
LZMAUseSeparateProcess=yes

; UI
WizardStyle=modern
WizardSizePercent=120
DisableProgramGroupPage=no

; Windows version requirement (Vista+)
MinVersion=6.1

; 64-bit aware
ArchitecturesInstallIn64BitMode=x64compatible
ArchitecturesAllowed=x64compatible

; Allow re-install over existing
AllowNoIcons=yes
UninstallDisplayIcon={app}\{#AppExeName}
UninstallDisplayName={#AppName}


[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"


[Tasks]
Name: "desktopicon";   Description: "Create a &desktop shortcut";   GroupDescription: "Additional shortcuts:"; Flags: unchecked
Name: "startupicon";   Description: "Launch CMS automatically at &Windows startup"; GroupDescription: "Additional shortcuts:"; Flags: unchecked


[Files]
; Main application bundle (PyInstaller onedir output)
Source: "cms-backend\dist\CMS_Server\*"; \
    DestDir: "{app}"; \
    Flags: ignoreversion recursesubdirs createallsubdirs


[Icons]
; Start Menu
Name: "{group}\{#AppName}";          Filename: "{app}\{#AppExeName}"
Name: "{group}\Uninstall {#AppName}"; Filename: "{uninstallexe}"

; Desktop shortcut (optional)
Name: "{commondesktop}\{#AppName}";  Filename: "{app}\{#AppExeName}"; \
    Tasks: desktopicon

; Startup (optional)
Name: "{userstartup}\{#AppName}";    Filename: "{app}\{#AppExeName}"; \
    Tasks: startupicon


[Registry]
; Register app so it appears in "Apps & features"
Root: HKLM; Subkey: "Software\{#AppPublisher}\{#AppName}"; \
    ValueType: string; ValueName: "InstallDir"; ValueData: "{app}"; \
    Flags: uninsdeletekey


[Run]
; Offer to launch the app immediately after install
Filename: "{app}\{#AppExeName}"; \
    Description: "Launch {#AppName} now"; \
    Flags: nowait postinstall skipifsilent shellexec


[UninstallDelete]
; Remove the writable data folder created at runtime next to the exe
Type: filesandordirs; Name: "{app}\cms_data"


[Code]
// Show a "first-run" info page before the final step
procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    MsgBox(
      'Installation complete!' + #13#10 + #13#10 +
      'To start XpertAI CMS:' + #13#10 +
      '  1. Open the Start Menu and click "XpertAI CMS"' + #13#10 +
      '     (or use the desktop shortcut if you created one)' + #13#10 +
      '  2. A console window will open — wait ~5 seconds' + #13#10 +
      '  3. Your browser will open automatically at:' + #13#10 +
      '     http://127.0.0.1:8000' + #13#10 + #13#10 +
      'Admin panel: http://127.0.0.1:8000/admin/' + #13#10 +
      '(Create a superuser by running the app once and' + #13#10 +
      ' visiting /admin/ to set up your account.)',
      mbInformation, MB_OK
    );
  end;
end;
