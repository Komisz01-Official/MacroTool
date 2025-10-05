[Setup]
AppName=Macro Tool Suite
AppVersion=1.0
DefaultDirName={autopf}\Macro Tool
DefaultGroupName=Macro Tool
OutputBaseFilename=MacroToolSetup
Compression=lzma
SolidCompression=yes
PrivilegesRequired=admin

[Files]
; EXEs
Source: "C:\Users\User\AppData\Local\Programs\Python\Python313\macro_tool_v.0.5_(json)\dist\macro_tool_v.0.5_(json).exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\User\AppData\Local\Programs\Python\Python313\macro_tool_v.0.5_(json)\dist\button_press_listener_v.0.2.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\User\AppData\Local\Programs\Python\Python313\macro_tool_v.0.5_(json)\dist\controller.exe"; DestDir: "{app}"; Flags: ignoreversion

; Optional: default JSON (if you want to ship an empty template)
; The program will create it anyway if missing
Source: "mouse_buttons.json"; DestDir: "{userappdata}\MacroTool"; Flags: onlyifdoesntexist

[Icons]
; Only create shortcuts for the Controller (launcher)
Name: "{group}\Macro Controller"; Filename: "{app}\controller.exe"
Name: "{userdesktop}\Macro Controller"; Filename: "{app}\controller.exe"

[Run]
; Optionally, you can run the controller after install
Filename: "{app}\controller.exe"; Description: "Launch Macro Controller"; Flags: nowait postinstall skipifsilent
