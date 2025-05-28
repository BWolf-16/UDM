import wmi

def get_device_list():
    c = wmi.WMI()
    devices = c.Win32_PnPEntity()
    return [
        {
            "name": d.Name,
            "device_id": d.DeviceID,
            "status": d.Status,
            "hardware_id": getattr(d, "PNPDeviceID", "Unknown")
        } for d in devices if d.Name
    ]