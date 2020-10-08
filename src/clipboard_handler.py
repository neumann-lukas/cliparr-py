import win32clipboard


saved = [{} for _ in range(10)]

formats = {1: 'CF_TEXT', 2: 'CF_BITMAP', 3: 'CF_METAFILEPICT', 4: 'CF_SYLK', 5: 'CF_DIF', 6: 'CF_TIFF', 7: 'CF_OEMTEXT',
           8: 'CF_DIB', 9: 'CF_PALETTE', 10: 'CF_PENDATA', 11: 'CF_RIFF', 12: 'CF_WAVE', 13: 'CF_UNICODETEXT',
           14: 'CF_ENHMETAFILE', 15: 'CF_HDROP', 16: 'CF_LOCALE', 17: 'CF_DIBV5', 18: 'CF_MAX', 128: 'CF_OWNERDISPLAY',
           129: 'CF_DSPTEXT', 130: 'CF_DSPBITMAP', 131: 'CF_DSPMETAFILEPICT', 142: 'CF_DSPENHMETAFILE'}


def format_name_from_code(fmt):
    if fmt in formats:
        return formats[fmt]
    try:
        return win32clipboard.GetClipboardFormatName(fmt)
    except:
        return None


def get_clipboard_data(code):
    return win32clipboard.GetClipboardData(code)


def set_clipboard_data(code, data):
    win32clipboard.SetClipboardData(code, data)


def save_clipboard_to_dict(i):
    global saved
    saved[i] = {}
    win32clipboard.OpenClipboard(None)
    code = 0
    while True:
        code = win32clipboard.EnumClipboardFormats(code)
        if code == 0:
            break

        data = get_clipboard_data(code)
        print('Saving: {}, type = {}'.format(str(code), type(data)))
        saved[i][code] = data
    win32clipboard.CloseClipboard()


def load_clipboard_from_dict(i):
    global saved
    win32clipboard.OpenClipboard(None)
    win32clipboard.EmptyClipboard()
    for code, data in saved[i].items():
        print('Loading: {}, type = {}'.format(str(code), type(data)))
        set_clipboard_data(code, data)
    win32clipboard.CloseClipboard()


#ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

