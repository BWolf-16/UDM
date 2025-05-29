import logging
import datetime
import webbrowser
import sys

log_path = "elevation_log.txt"

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler(log_path, mode='a', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

def log_info(message):
    logging.info(message)

def log_error(message, exc=None):
    logging.error(message)
    if exc:
        logging.error(f"Exception: {str(exc)}")

def log_solution_hint(module_name):
    hints = {
        'wmi': "Try running: pip install wmi",
        'customtkinter': "Try running: pip install customtkinter",
        'ctypes': "Built-in module. Your Python might be corrupted.",
        'subprocess': "Built-in module. Your Python might be corrupted.",
        'os': "Built-in module. Your Python might be corrupted.",
        'sys': "Built-in module. Your Python might be corrupted.",
        'datetime': "Built-in module. Should always be present.",
        'json': "Built-in module. Your Python might be corrupted.",
        'platform': "Built-in module. Your Python might be corrupted."
    }
    hint = hints.get(module_name, f"Search online for how to install: {module_name}")
    logging.info(f"💡 Solution: {hint}")
    if 'pip install' in hint:
        webbrowser.open(f"https://pypi.org/project/{module_name}/")
