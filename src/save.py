import win32clipboard

storage_directory = ""
file_ending = ".ca"

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


def write_data_to_file(name, data):
    if type(data) != bytes:
        data = bytes(data, "utf-8")

    with open(storage_directory + str(name) + file_ending, "wb") as file:
        file.write(data)
        file.close()


def save_clipboard_to_directory(storage_directory_f):
    global storage_directory
    storage_directory = storage_directory_f
    win32clipboard.OpenClipboard(None)
    code = 0
    while True:
        code = win32clipboard.EnumClipboardFormats(code)
        if code == 0:
            break

        data = win32clipboard.GetClipboardData(code)
        write_data_to_file(str(code), data)

        print('Saving: {}, type = {}'.format(str(code) + file_ending, format_name_from_code(code)))

    win32clipboard.CloseClipboard()
