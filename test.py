from screeninfo import get_monitors

def list_monitors():
    monitors = get_monitors()
    print(f"Detected {len(monitors)} monitors.\n")
    
    for index, monitor in enumerate(monitors):
        print(f"Monitor {index + 1}:")
        print(f"Name: {monitor.name}")
        print(f"Width: {monitor.width}, Height: {monitor.height}")
        print(f"Position: (X: {monitor.x}, Y: {monitor.y})\n")

if __name__ == "__main__":
    list_monitors()
