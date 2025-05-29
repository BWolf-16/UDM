import ctypes
import sys
import os
from utils.logger import log_info, log_error, log_solution_hint

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def relaunch_as_admin():
    log_info("Not admin. Attempting to relaunch with elevation.")
    params = ' '.join([f'"{arg}"' for arg in sys.argv])
    executable = sys.executable
    ret = ctypes.windll.shell32.ShellExecuteW(None, "runas", executable, params, None, 1)
    log_info(f"ShellExecuteW returned: {ret}")
    return ret > 32

# Try to elevate if not admin
if not is_admin():
    success = relaunch_as_admin()
    if success:
        sys.exit()
    else:
        log_error("Elevation failed. Continuing without admin. Some features may be limited.")

log_info("Running as admin. Launching app...")

try:
    from ui.app import launch_app
    launch_app()
except ModuleNotFoundError as e:
    log_error(f"Missing module: {e.name}", e)
    log_solution_hint(e.name)
    input("💥 Press Enter to exit...")
except Exception as e:
    log_error("Exception in launch_app:", e)
    input("💥 Press Enter to exit...")
