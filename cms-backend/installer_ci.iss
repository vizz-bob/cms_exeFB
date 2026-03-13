; installer_ci.iss
; ================
; Inno Setup 6 script for GitHub Actions CI builds.
;
; Paths here are relative to the cms-backend repo root
; (i.e. where the workflow checks out the code).
;
; For local Windows builds from the cms_exe/ parent folder,
; use installer.iss instead.

#define AppName      "XpertAI CMS"
#define AppVersion   "1.0.0"
#define AppPublisher "XpertAI Global"
#define AppExeName   "CMS_Server.exe"
#define AppURL       "http://127.0.0.1:8000"

[Setup]
AppId={{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher={#AppPublisher}
AppPublisherURL={#AppURL}
AppSupportURL={#AppURL}
AppUpdatesURL={#AppURL}

DefaultDirName={autopf}\{#AppName}
DefaultGroupName={#AppName}

; Output folder (relative to this .iss file location = repo root)
OutputDir=Output
OutputBaseFilename=CMS_Setup

Compression=lzma2/ultra64
SolidCompression=yes
LZMAUseSeparateProcess=yes

WizardStyle=modern
WizardSizePercent=120
DisableProgramGroupPage=no
MinVersion=6.1

ArchitecturesInstallIn64BitMode=x64compatible
ArchitecturesAllowed=x64compatible

AllowNoIcons=yes
UninstallDisplayIcon={app}\{#AppExeName}
UninstallDisplayName={#AppName}


[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"


[Tasks]
Name: "desktopicon"; Description: "Create a &desktop shortcut"; GroupDescription: "Additional shortcuts:"; Flags: unchecked
Name: "startupicon"; Description: "Launch CMS automatically at &Windows startup"; GroupDescription: "Additional shortcuts:"; Flags: unchecked


[Files]
; PyInstaller onedir output — path is relative to repo root in CI
Source: "dist\CMS_Server\*"; \
    DestDir: "{app}"; \
    Flags: ignoreversion recursesubdirs createallsubdirs


[Icons]
Name: "{group}\{#AppName}";           Filename: "{app}\{#AppExeName}"
Name: "{group}\Uninstall {#AppName}"; Filename: "{uninstallexe}"
Name: "{commondesktop}\{#AppName}";   Filename: "{app}\{#AppExeName}"; Tasks: desktopicon
Name: "{userstartup}\{#AppName}";     Filename: "{app}\{#AppExeName}"; Tasks: startupicon


[Registry]
Root: HKLM; Subkey: "Software\{#AppPublisher}\{#AppName}"; \
    ValueType: string; ValueName: "InstallDir"; ValueData: "{app}"; \
    Flags: uninsdeletekey


[Run]
Filename: "{app}\{#AppExeName}"; \
    Description: "Launch {#AppName} now"; \
    Flags: nowait postinstall skipifsilent shellexec


[UninstallDelete]
Type: filesandordirs; Name: "{app}\cms_data"


[Code]
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
      'Admin panel: http://127.0.0.1:8000/admin/',
      mbInformation, MB_OK
    );
  end;
end;
