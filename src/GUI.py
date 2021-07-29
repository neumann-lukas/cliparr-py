from datetime import time
from time import sleep
from tkinter.constants import N, S
import PySimpleGUI as sg
import json
import os
import ctypes
import psutil
import subprocess
import sys

delimiter = "."
config = ""
config_path = "config.json"

def nested_get(dic, keys):    
    for key in keys:
        dic = dic[key]
    return dic

def nested_set(dic, keys, value):
    for key in keys[:-1]:
        dic = dic.setdefault(key, {})
    dic[keys[-1]] = value

def layout_from_json(config):
    tab_layout = {}
    for tab in config:
        tab_layout[tab] = []
        for key,value in config[tab].items():
            row = [sg.Text(key), sg.InputText(value, key=str(tab)+delimiter+str(key), enable_events=True)]
            tab_layout[tab].append(row)

    layout = [[sg.TabGroup([[sg.Tab(i, tab_layout[i]) for i in tab_layout]])]]
    return layout


def json_from_values(values):
    global config
    for key, value in values.items():
        key = str(key)
        if delimiter in key:
            key = key.split(delimiter)
        else:
            key = [key]
        nested_set(config, key, value)

def start_hotkey_handler():
    pid = subprocess.Popen(['python', 'main.py', '-c', 'config.json'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    print("started" + str(pid.pid))
    with open("pid.txt", "w") as f:
        f.write(str(pid.pid))

def kill_hotkey_handler():
    with open("pid.txt", "r") as f:
        s = f.read()
    n = int(s)
    os.kill(n, 9)

def openGui():
    global config 
    running = False

    with open("pid.txt", "r") as f:
        r = psutil.pid_exists(int(f.read()))
        print(r)
        running = r

    with open(config_path, "r") as f:
        config = json.loads(f.read())

    sg.theme('Default1')   

    layout = []
    if running:
        layout.append([sg.Button("Stop", button_color=('black', 'red'),enable_events=True, key='switch')])
    else:
        layout.append([sg.Button("Start", button_color=('white', 'green'),enable_events=True, key='switch')])

    layout.append(layout_from_json(config)[0])
    layout.append([sg.Button('Save'), sg.Text(" By Lukas Neumann, neumann-lukas.github.io/cliparr")])
    window = sg.Window('Cliparr v1.0', layout)

    while True:
        event, values = window.read()
        if event == 'switch':
            if not running:
                window.FindElement('switch').Update(button_color=('black', 'red'))
                window.FindElement('switch').Update("Stop")
                start_hotkey_handler() 
                               
            else:
                window.FindElement('switch').Update(button_color=('white', 'green'))
                window.FindElement('switch').Update("Start")
                kill_hotkey_handler()
                

            running = not running

        if event == sg.WIN_CLOSED:
            break

        if (event=="Save"):
            if isinstance(values, dict):
                if len(values) > 1:
                    values.popitem()
                    json_from_values(values)
                    with open(config_path, "w") as f:
                        f.write("")
                        f.write(json.dumps(config))   

    window.close()
    
if __name__ == "__main__":
    def is_admin():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    if is_admin():
        openGui()
    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    

