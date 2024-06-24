[Setup]
AppName=PharmCalc
AppVersion=1.1
DefaultDirName={localappdata}\PharmCalc
DefaultGroupName=PharmCalc
OutputDir=./CurrentVersion
OutputBaseFilename=PharmCalcInstaller
Compression=lzma
SolidCompression=yes
PrivilegesRequired=lowest
CloseApplications=yes
CloseApplicationsFilter=PharmCalc.exe
RestartApplications=yes
AllowNoIcons=yes

[Files]
Source: "dist\PharmCalc.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "icon.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autodesktop}\PharmCalc"; Filename: "{app}\PharmCalc.exe"; IconFilename: "{app}\icon.ico"

[Run]
Filename: "{app}\PharmCalc.exe"; Description: "{cm:LaunchProgram,PharmCalc}"; Flags: nowait postinstall