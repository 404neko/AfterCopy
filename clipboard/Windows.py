from error import *

import win32clipboard
import win32con
from PIL import Image
from PIL import ImageGrab

class ClipBoard:

    def __init__(self):
        pass

    def get(self):
        if win32clipboard.IsClipboardFormatAvailable(win32con.CF_BITMAP):
            #win32clipboard.OpenClipboard()
            #data = win32clipboard.GetClipboardData(win32con.CF_BITMAP)
            #clipboard.CloseClipboard()
            data = ImageGrab.grabclipboard()
            return 'BITMAP', data
        if win32clipboard.IsClipboardFormatAvailable(win32con.CF_UNICODETEXT):
            win32clipboard.OpenClipboard()
            data = win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)
            win32clipboard.CloseClipboard()
            return 'UNICODE', data
        if win32clipboard.IsClipboardFormatAvailable(win32con.CF_TEXT):
            win32clipboard.OpenClipboard()
            data = win32clipboard.GetClipboardData(win32con.CF_TEXT)
            win32clipboard.CloseClipboard()
            return 'TEXT', data
        if win32clipboard.IsClipboardFormatAvailable(win32con.CF_HDROP):
            win32clipboard.OpenClipboard()
            data = win32clipboard.GetClipboardData(win32con.CF_HDROP)
            clipboard.CloseClipboard()
            return 'FILES', data
        print 'INFO - except type not found'

    def put(self,string):
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32con.CF_TEXT, string)
        win32clipboard.CloseClipboard()
