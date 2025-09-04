import os
from PIL import Image, ImageDraw
import threading
import tkinter
from tkinter import messagebox

# Globals
saved_position = None
running = True


if os.name == 'nt':  # Windows

    from plyer import notification
    import keyboard
    import pyautogui
    import pystray
    import mouse 
    # ---------- Icon ----------
    def load_icon(path=".\\Resources\\icon.ico"):
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

    def quit_app(icon, item):
        global running
        running = False
        icon.visible = False
        icon.stop()

    def show_help():
        root = tkinter.Tk()
        root.geometry("400x100")
        root.title("Mouse Saver Help")
        root.iconbitmap(".\\Resources\\icon.ico")
        root.resizable(False, False)
        root.focus_force()
        helptext = tkinter.Label(root)
        helptext["text"] = "\nSave Position: Ctrl + Alt + Shift + M\nRestore Position: Ctrl + Alt + M"
        helptext.pack()
        root.mainloop()


    def setup_tray():
        icon_image = load_icon()
        icon = pystray.Icon(
            "Mouse Saver",
            icon_image,
            menu=pystray.Menu(
                pystray.MenuItem("Help", show_help),
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
elif os.name == 'posix':  # macOS or Linux
    import rumps
    from pynput import keyboard, mouse
    import pync

    class MouseSaverApp(rumps.App):
        def __init__(self):
            super(MouseSaverApp, self).__init__("MouseSaver", icon="icon.icns")  # you can set .icns icon
            self.saved_position = None
            self.mouse_controller = mouse.Controller()

            # Add menu item
            self.menu = ["Quit"]

            # Register hotkeys
            self.listener = keyboard.GlobalHotKeys({
                "<ctrl>+<alt>+<shift>+7": self.save_position,
                "<ctrl>+<alt>+7": self.restore_position
            })
            self.listener.start()

        def save_position(self):
            self.saved_position = self.mouse_controller.position
            pync.notify(f"Saved position: {self.saved_position}", title="Mouse Saver")

        def restore_position(self):
            if self.saved_position:
                self.mouse_controller.position = self.saved_position
                pync.notify(f"Restored to: {self.saved_position}", title="Mouse Saver")

        @rumps.clicked("Quit")
        def quit_app(self, _):
            self.listener.stop()
            rumps.quit_application()

    if __name__ == "__main__":
        MouseSaverApp().run()
