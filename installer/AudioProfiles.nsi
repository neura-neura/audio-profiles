Unicode True
ManifestDPIAware True
SetCompressor /SOLID lzma
RequestExecutionLevel user

!include "MUI2.nsh"
!include "FileFunc.nsh"
!include "LogicLib.nsh"

!insertmacro GetParameters
!insertmacro GetOptions

Name "Audio Profiles"
BrandingText "Audio Profiles by neura-neura"
OutFile "..\dist\AudioProfilesSetup-1.0.3.exe"
InstallDir "$LOCALAPPDATA\Audio Profiles"
InstallDirRegKey HKCU "Software\AudioProfiles" "InstallDir"
ShowInstDetails show
ShowUninstDetails show
Var LaunchAfterInstall

!define MUI_ABORTWARNING
!define MUI_CUSTOMFUNCTION_ONINIT ParseLaunchFlag
!define MUI_ICON "..\src\AudioProfiles\Assets\AppIcon.ico"
!define MUI_UNICON "..\src\AudioProfiles\Assets\AppIcon.ico"
!define MUI_WELCOMEPAGE_TITLE "Install Audio Profiles"
!define MUI_WELCOMEPAGE_TEXT "Audio Profiles lets you switch Windows speakers and microphones with one click. Created by neura-neura. No administrator account is required."
!define MUI_FINISHPAGE_NOAUTOCLOSE
!define MUI_FINISHPAGE_RUN
!define MUI_FINISHPAGE_RUN_FUNCTION LaunchApp
!define MUI_FINISHPAGE_RUN_TEXT "Open Audio Profiles"
!define MUI_FINISHPAGE_SHOWREADME
!define MUI_FINISHPAGE_SHOWREADME_FUNCTION CreateDesktopShortcut
!define MUI_FINISHPAGE_SHOWREADME_TEXT "Create a desktop shortcut"

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_LANGUAGE "English"

Function ParseLaunchFlag
  StrCpy $LaunchAfterInstall "0"
  ${GetParameters} $R0
  ${GetOptions} $R0 "/LAUNCH" $R1
  IfErrors +2 0
    StrCpy $LaunchAfterInstall "1"
FunctionEnd

Section "Install"
  DetailPrint "Closing Audio Profiles if it is running..."
  ExecWait 'taskkill /IM AudioProfiles.exe /F'
  Sleep 800
  SetOutPath "$INSTDIR"
  File /r "payload\*.*"

  CreateDirectory "$SMPROGRAMS\Audio Profiles"
  CreateShortCut "$SMPROGRAMS\Audio Profiles\Audio Profiles.lnk" "$INSTDIR\AudioProfiles.exe" "" "$INSTDIR\Assets\AppIcon.ico"
  CreateShortCut "$SMPROGRAMS\Audio Profiles\Uninstall Audio Profiles.lnk" "$INSTDIR\Uninstall.exe"

  WriteRegStr HKCU "Software\AudioProfiles" "InstallDir" "$INSTDIR"
  WriteUninstaller "$INSTDIR\Uninstall.exe"

  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\AudioProfiles" "DisplayName" "Audio Profiles"
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\AudioProfiles" "DisplayIcon" "$INSTDIR\AudioProfiles.exe"
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\AudioProfiles" "DisplayVersion" "1.0.3"
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\AudioProfiles" "Publisher" "neura-neura"
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\AudioProfiles" "URLInfoAbout" "https://github.com/neura-neura/audio-profiles"
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\AudioProfiles" "HelpLink" "https://github.com/neura-neura"
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\AudioProfiles" "URLUpdateInfo" "https://github.com/neura-neura/audio-profiles/releases"
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\AudioProfiles" "InstallLocation" "$INSTDIR"
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\AudioProfiles" "UninstallString" "$INSTDIR\Uninstall.exe"
  WriteRegDWORD HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\AudioProfiles" "NoModify" 1
  WriteRegDWORD HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\AudioProfiles" "NoRepair" 1

  ${GetSize} "$INSTDIR" "/S=0K" $0 $1 $2
  IntFmt $0 "0x%08X" $0
  WriteRegDWORD HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\AudioProfiles" "EstimatedSize" "$0"
  ${If} $LaunchAfterInstall == "1"
    Call LaunchApp
  ${EndIf}
SectionEnd

Section "Uninstall"
  Delete "$SMPROGRAMS\Audio Profiles\Audio Profiles.lnk"
  Delete "$SMPROGRAMS\Audio Profiles\Uninstall Audio Profiles.lnk"
  RMDir "$SMPROGRAMS\Audio Profiles"

  Delete "$DESKTOP\Audio Profiles.lnk"
  Delete "$SMSTARTUP\Audio Profiles.lnk"

  RMDir /r "$INSTDIR"

  DeleteRegKey HKCU "Software\AudioProfiles"
  DeleteRegKey HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\AudioProfiles"
SectionEnd

Function CreateDesktopShortcut
  CreateShortCut "$DESKTOP\Audio Profiles.lnk" "$INSTDIR\AudioProfiles.exe" "" "$INSTDIR\Assets\AppIcon.ico"
FunctionEnd

Function LaunchApp
  SetOutPath "$INSTDIR"
  System::Call "user32::AllowSetForegroundWindow(i -1)"
  Exec '"$INSTDIR\AudioProfiles.exe" --foreground'
FunctionEnd

