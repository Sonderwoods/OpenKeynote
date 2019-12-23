import sys
from cx_Freeze import setup, Executable

#https://www.youtube.com/watch?v=zZHX9x7eNjQ


company_name = 'Marcins Programms'
product_name = 'Sokrates'

bdist_msi_options = {
    'upgrade_code': '{Banana-rama-30403344939493}',
    'add_to_path': False,
    'initial_target_dir': r'[ProgramFilesFolder]\%s\%s' % (company_name, product_name),
    }

path = sys.path
build_exe_options = {
"path": path,
"icon": "brain.ico"}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

exe = Executable(script='Sokrates__PYMATH.py',
                 base=base,
                 icon='brain.ico',
                )

setup(  name = "Sokrates",
        version = "1.1",
        description = "Powerfull Calculator for all plattforms",
        executables = [exe],
        options = {'bdist_msi': bdist_msi_options})
