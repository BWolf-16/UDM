import wmi

def normalize_status(raw):
    if not raw:
        return "Unknown"
    raw = raw.lower()
    if "ok" in raw or "working" in raw:
        return "Enabled"
    if "disable" in raw:
        return "Disabled"
    if "degrade" in raw or "warn" in raw:
        return "Degraded"
    return raw.capitalize()

def get_devices():
    devices = []
    try:
        w = wmi.WMI()
        for item in w.Win32_PnPEntity():
            if item.DeviceID and item.Name:
                devices.append({
                    "device_id": item.DeviceID,
                    "name": item.Name,
                    "status": normalize_status(item.Status)
                })
    except Exception as e:
        print("WMI Error:", e)
    return devices
