$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("$HOME\Desktop\LaneGuard Vision.lnk")
$Shortcut.TargetPath = "C:\Users\Shravya\Desktop\LaneGaurdVision\run_app.bat"
$Shortcut.WorkingDirectory = "C:\Users\Shravya\Desktop\LaneGaurdVision"
$Shortcut.IconLocation = "shell32.dll, 22"
$Shortcut.Save()
Write-Host "✅ Shortcut created on your Desktop!"
