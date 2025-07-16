# PowerShell script to build GlueDo executable with PyInstaller

# Clean previous builds
Remove-Item -Recurse -Force build, dist -ErrorAction SilentlyContinue
Remove-Item gluedo_gui.spec -ErrorAction SilentlyContinue

# Run PyInstaller
pyinstaller `
  --name gluedo_gui `
  --onefile `
  --windowed `
  --icon=gluedo.ico `
  --add-data "assets;assets" `
  main.py

Write-Host "`n✅ Build complete. Output: dist\gluedo_gui.exe" -ForegroundColor Green
