import subprocess

def disable_device(device_id):
    subprocess.call(["pnputil", "/disable-device", device_id])

def enable_device(device_id):
    subprocess.call(["pnputil", "/enable-device", device_id])

def restart_device(device_id):
    disable_device(device_id)
    enable_device(device_id)