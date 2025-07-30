# Очистка
Remove-Item -Recurse -Force build, dist, *.spec -ErrorAction SilentlyContinue

# Сборка
pyinstaller `
  --name "GlueDo" `
  --onefile `
  --windowed `
  --icon "assets/gluedo.ico" `
  --add-data "assets;assets" `
  main.py
