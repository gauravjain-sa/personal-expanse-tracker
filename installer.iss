; Inno Setup Script for Expense Tracker
; Download Inno Setup from: https://jrsoftware.org/isdl.php

#define MyAppName "Expense Tracker"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Your Company Name"
#define MyAppURL "https://yourwebsite.com"
#define MyAppExeName "ExpenseTracker.exe"

[Setup]
; Application Info
AppId={{A1B2C3D4-E5F6-4A5B-8C9D-0E1F2A3B4C5D}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}

; Installation Directories
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes

; Output
OutputDir=installer_output
OutputBaseFilename=ExpenseTracker_Setup_v{#MyAppVersion}
; Custom icon - only included if the file exists (place .ico at resources\icon.ico)
#ifexist "resources\icon.ico"
SetupIconFile=resources\icon.ico
#endif
Compression=lzma2/max
SolidCompression=yes

; Privileges
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog

; UI
WizardStyle=modern
WizardSizePercent=120,100

; Uninstall
UninstallDisplayIcon={app}\{#MyAppExeName}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; Include all files from dist/ExpenseTracker folder
Source: "dist\ExpenseTracker\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "dist\ExpenseTracker\README.txt"; DestDir: "{app}"; Flags: ignoreversion isreadme

[Icons]
; Start Menu
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{group}\README"; Filename: "{app}\README.txt"

; Desktop Icon (optional)
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
; Option to launch application after installation
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[Code]
procedure InitializeWizard();
var
  WelcomeLabel: TNewStaticText;
begin
  // Custom welcome message
  WelcomeLabel := TNewStaticText.Create(WizardForm);
  WelcomeLabel.Parent := WizardForm.WelcomePage;
  WelcomeLabel.Caption :=
    'This will install Expense Tracker on your computer.' + #13#10 + #13#10 +
    'Expense Tracker is a personal finance management tool that helps you:' + #13#10 +
    '  • Track your credits and debits' + #13#10 +
    '  • Manage multiple accounts' + #13#10 +
    '  • Categorize transactions' + #13#10 +
    '  • Generate financial reports' + #13#10 +
    '  • Export data to Excel/CSV' + #13#10 + #13#10 +
    'Your data will be stored securely in your user profile.';
  WelcomeLabel.AutoSize := True;
  WelcomeLabel.WordWrap := True;
  WelcomeLabel.Left := WizardForm.WelcomeLabel2.Left;
  WelcomeLabel.Top := WizardForm.WelcomeLabel2.Top + WizardForm.WelcomeLabel2.Height + 20;
  WelcomeLabel.Width := WizardForm.WelcomeLabel2.Width;
end;

procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
var
  DataPath: String;
begin
  if CurUninstallStep = usPostUninstall then
  begin
    // Ask if user wants to keep their data
    if MsgBox('Do you want to keep your financial data?' + #13#10 + #13#10 +
              'If you select "No", all your transactions, accounts, and categories will be deleted.' + #13#10 +
              'If you select "Yes", you can reinstall the application later and your data will be preserved.',
              mbConfirmation, MB_YESNO or MB_DEFBUTTON1) = IDNO then
    begin
      // Delete user data
      DataPath := ExpandConstant('{userappdata}\Expense Tracker');
      if DirExists(DataPath) then
      begin
        if DelTree(DataPath, True, True, True) then
          MsgBox('Your financial data has been deleted.', mbInformation, MB_OK)
        else
          MsgBox('Could not delete all data. You may need to manually delete: ' + DataPath, mbError, MB_OK);
      end;
    end
    else
    begin
      MsgBox('Your financial data has been preserved at:' + #13#10 +
             ExpandConstant('{userappdata}\Expense Tracker'), mbInformation, MB_OK);
    end;
  end;
end;
