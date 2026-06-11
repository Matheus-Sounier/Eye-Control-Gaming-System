try:
    from pygrabber.dshow_graph import FilterGraph

    graph = FilterGraph()
    devices = graph.get_input_devices()

    print("Cameras found via DirectShow")
    for i, name in enumerate(devices):
        print(f"  [{i}] {name}")
    print()

except ImportError:
    print("pygrabber not installed, trying other approaches\n")
    devices = []

try:
    import wmi

    c = wmi.WMI()

    for cam in c.Win32_PnPEntity(PNPClass="Camera"):
        print(f"  {cam.Name}")
    print()

except ImportError:
    print("wmi not installed\n")

import cv2

if devices:
    for i, name in enumerate(devices):
        cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)

        ret, frame = cap.read()

        status = "OK ✓" if (ret and frame is not None) else "failed"

        print(f"  [{i}] {name} → {status}")

        cap.release()

else:
    print("  No devices listed by pygrabber.")