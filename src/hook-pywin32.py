"""
PyInstaller hook for PyWin32 to ensure all required DLLs are included.
"""
import os
import sys
import glob
import site
from PyInstaller.utils.hooks import collect_dynamic_libs

# Add PyWin32 binaries
binaries = []

# Try to find the DLLs in various locations
dll_names = ['pythoncom310.dll', 'pywintypes310.dll']
dll_found = False

# Approach 1: Check site-packages/pywin32_system32
site_packages = site.getsitepackages()
for site_pkg in site_packages:
    pywin32_path = os.path.join(site_pkg, 'pywin32_system32')
    if os.path.exists(pywin32_path):
        for dll in dll_names:
            dll_path = os.path.join(pywin32_path, dll)
            if os.path.exists(dll_path):
                binaries.append((dll_path, '.'))
                dll_found = True

# Approach 2: Check in Python's DLLs directory
if not dll_found:
    python_dll_dir = os.path.join(os.path.dirname(sys.executable), "DLLs")
    if os.path.exists(python_dll_dir):
        for dll in dll_names:
            dll_path = os.path.join(python_dll_dir, dll)
            if os.path.exists(dll_path):
                binaries.append((dll_path, '.'))
                dll_found = True

# Approach 3: Check in win32 package directory
if not dll_found:
    for site_pkg in site_packages:
        win32_path = os.path.join(site_pkg, 'win32')
        if os.path.exists(win32_path):
            dll_paths = glob.glob(os.path.join(win32_path, '*.dll'))
            for dll_path in dll_paths:
                if os.path.basename(dll_path) in dll_names:
                    binaries.append((dll_path, '.'))
                    dll_found = True

# Also collect any other dynamic libraries from win32 modules
try:
    win32_libs = collect_dynamic_libs('win32')
    binaries.extend(win32_libs)
except Exception:
    pass

try:
    pythoncom_libs = collect_dynamic_libs('pythoncom')
    binaries.extend(pythoncom_libs)
except Exception:
    pass

try:
    pywintypes_libs = collect_dynamic_libs('pywintypes')
    binaries.extend(pywintypes_libs)
except Exception:
    pass 