import keyboard
import clipboard_handler
import argparse
from time import sleep, time
import os
import json

class hotkey_handler():
    def __init__(self, keep, hotkeys):
        print("hotkey_handler started")
        self.running = True
        self.slots = len(hotkeys) + 1
        self.handler = clipboard_handler.clipboard_handler(self.slots)
        self.keep = keep
        print(hotkeys)
        self.config = hotkeys

        copykeys = [value for key,value in self.config.items() if str(key).startswith("copy")]
        pastekeys = [value for key,value in self.config.items() if str(key).startswith("paste")]

        for hotkey in copykeys:
            keyboard.add_hotkey(hotkey, self.handle_press, args=('copy', copykeys.index(hotkey)), suppress=True)
        for hotkey in pastekeys:
            keyboard.add_hotkey(hotkey, self.handle_press, args=('paste', pastekeys.index(hotkey)), suppress=True)
        keyboard.wait()

    def handle_press(self, h_type, number):
        if self.keep:

            if h_type == "copy":
                self.handler.save_clipboard_to_dict(self.slots-1)
                sleep(1e-3)
                keyboard.press_and_release('ctrl+c')
                sleep(1e-3)
                self.handler.save_clipboard_to_dict(number)
                self.handler.load_clipboard_from_dict(self.slots-1)

            else:
                self.handler.save_clipboard_to_dict(self.slots-1)
                self.handler.load_clipboard_from_dict(number)
                sleep(1e-3)
                keyboard.press_and_release('ctrl+v')
                sleep(1e-3)
                self.handler.load_clipboard_from_dict(self.slots-1)



        else:
            if h_type == "copy":
                keyboard.press_and_release('ctrl+c')
                sleep(1e-3)
                self.handler.save_clipboard_to_dict(number)
            else:
                self.handler.load_clipboard_from_dict(number)
                sleep(1e-3)
                keyboard.press_and_release('ctrl+v')
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config',
                    required=True,
                    type=str,
                    default=None, 
                    dest="config",
                    metavar="<config-file>",
                    help="Config file, if this argument is set, everyhing else will be ignored!" )


    args = parser.parse_args()
    print(args)
    hotkey_handler(True, json.load(open(args.config))["hotkey"])

     # sys.exit(2)
    #hotkey_handler(int(sys.argv[0]), bool(sys.argv[1]))


