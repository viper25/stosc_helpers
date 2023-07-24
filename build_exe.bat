del /s /q .\dist\main_2\*
rd /s /q build
rd /s /q __pycache__
@REM pyinstaller --icon glider.ico --version-file winver.rc --onefile --distpath .\dist\main_2 main_2.py --add-data 'config.toml:.'
pyinstaller --onefile --version-file winver.rc --distpath .\dist\main_2 main_2.py
@REM start cmd.exe /c ""%programfiles%\7-Zip\7z.exe"" a -tzip .\dist\authly_windows_x64_PING.zip .\dist\windows_x64_PING\*