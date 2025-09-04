import mouse
import keyboard
import pyautogui
import pystray
from PIL import Image, ImageDraw
from plyer import notification
import threading

# Globals
saved_position = None
running = True


# ---------- Icon ----------
def load_icon(path="icon.ico"):
    return Image.open(path)

# ---------- Notifications ----------
def notify(title, message):
    # Run in a thread to avoid blocking
    threading.Thread(
        target=lambda: notification.notify(title=title, message=message, timeout=2)
    ).start()

# ---------- Hotkeys ----------
def save_position():
    global saved_position
    saved_position = mouse.get_position()

def restore_position():
    global saved_position
    if saved_position:
        pyautogui.moveTo(saved_position[0], saved_position[1])

# ---------- Tray ----------
def create_image():
    img = Image.new("RGB", (64, 64), (0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse((16, 16, 48, 48), fill=(30, 144, 255))
    return img

def quit_app(icon, item):
    global running
    running = False
    icon.visible = False
    icon.stop()

def setup_tray():
    icon_image = load_icon(".\\Resources\\icon.ico")
    icon = pystray.Icon(
        "MouseSaver",
        icon_image,
        menu=pystray.Menu(
            pystray.MenuItem("Quit", quit_app)
        )
    )
    icon.run()

# ---------- Start everything ----------
keyboard.add_hotkey("ctrl+alt+shift+m", save_position)
keyboard.add_hotkey("ctrl+alt+m", restore_position)
notify("Mouse Saver", "Mouse Saver is running in the background.")
# Run tray in main thread
setup_tray()
