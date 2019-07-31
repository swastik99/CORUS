import sys
import os.path
from cx_Freeze import setup, Executable


PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')
# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"], 'include_files':['tcl86t.dll','tk86t.dll']}
# These dll files need to be included in the file to run it tcl86t.dll, tk86t.dll which are in our python folder
# C:\Users\superuser\AppData\Local\Programs\Python\Python37-32\

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"



setup(  name = "Corus",
        version = "0.1",
        description = "Media player application having great GUI",
        options = {"build_exe": build_exe_options},
        executables = [Executable("main.py", base=base)])


# This setup.py file is to change .py file to .exe executable file and all this need to be imported properly
# Compile using in cmd : python setup.py build