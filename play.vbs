' GUI Launcher for The Forgotten Mansion (Windows)
' Launches the game in GUI mode without any console window
' For terminal mode, run: python main.py from command prompt

Set objShell = CreateObject("WScript.Shell")
objShell.Run "pythonw play.py", 0, False
