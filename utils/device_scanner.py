import wmi

def get_devices(include_hidden=False):
    devices = []
    try:
        w = wmi.WMI()
        for item in w.Win32_PnPEntity():
            device_id = item.DeviceID
            name = item.Name or "Unknown Device"
            status = item.Status or "Unknown"
            is_hidden = getattr(item, "ConfigManagerErrorCode", 0) != 0

            if not include_hidden and is_hidden:
                continue

            devices.append({
                "device_id": device_id,
                "name": name,
                "status": status,
                "hidden": is_hidden,
            })
    except Exception as e:
        print("Error scanning devices:", e)

    return devices
