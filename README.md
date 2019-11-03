# Lazy CMD
LazyCMD is an app for marking down and running your os native commands.

Developed using Python 3.7.4 on Windows 10.


## How to build

1. Use virtualenv on the project folder to make a new virtual environment.
2. Activate your virtual environment: Windows ```LazyCMD/Scripts/activate``` or Linux ```source bin/activate```
3. Pip install pyinstaller: ```pip install pyinstaller```
4. Build with: pyinstaller app.py --onefile --name LazyCMD

~~pyinstaller app.py --onefile --noconsole --name LazyCMD~~


## How to use
On initial start up the application generates these files:
* ```config.json```
* ```commands/dir.cmd```

Add your commands as text files to the commands folder. Create an entry in ```config.json``` for your command.
