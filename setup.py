# setup.py
# higly inspired from
# https://fernandofreitasalves.com/how-to-create-python-exe-with-msi-installer-and-cx_freeze/

from cx_Freeze import setup, Executable
import os.path
PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

setup(
    name="OpenKeynote",
    version="0.8.5",
    options={"build_exe": {
        'packages': ["os", "sys", "ctypes", "win32con"],
        'include_files': ['assets/icon.ico'],
        'include_msvcr': True,
    }},
    executables=[Executable("main.py", base="Win32GUI")]
)
