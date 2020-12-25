import keyboard
import clipboard_handler
from time import sleep

default_config = \
[
    [
    "ctrl+f1",
    "ctrl+f2",
    "ctrl+f3",
    "ctrl+f4",
    "ctrl+f5",
    ],
    [
    "shift+f1",
    "shift+f2",
    "shift+f3",
    "shift+f4",
    "shift+f5",
    ]
]

handler = clipboard_handler.clipboard_handler()

class hotkey_handler():
    def __init__(self, hotkeys=default_config):
        self.config = hotkeys
        for hotkey in self.config[0]:
            #kotkey = "alt+v+3"
            keyboard.add_hotkey(hotkey, self.handle_press, args=('copy', self.config[0].index(hotkey)), suppress=True)
            #exit()
        for hotkey in self.config[1]:
            keyboard.add_hotkey(hotkey, self.handle_press, args=('paste', self.config[1].index(hotkey)), suppress=True)

    def handle_press(self, h_type, number):
        print(type, number)

        if h_type == "copy":
            keyboard.press_and_release('ctrl+c')
            sleep(1e-3)
            handler.save_clipboard_to_dict(number)
        else:
            handler.load_clipboard_from_dict(number)
            sleep(1e-3)
            keyboard.press_and_release('ctrl+v')
        



hotkey_handler()
keyboard.wait()
