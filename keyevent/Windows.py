from error import *

import os
import sys 
import ctypes
from ctypes import wintypes
from functools import reduce

import win32con

def handle_win_f6():
    print 'INFO - Byebye'
    sys.exit(0)

class KeyEvent:

    byref = ctypes.byref
    user32 = ctypes.windll.user32
    DEFAULT_HOTKEYS = [
        {
            'function':handle_win_f6,
            'key': (win32con.VK_F6, win32con.MOD_CONTROL)
        },
    ]

    key_dict = win32con

    def __init__(self):
        pass

    def set_hotkey_jar(self,hotkey_jar):
        self.make_hotkeys_actions(self.DEFAULT_HOTKEYS+hotkey_jar)
        for id, values in self.HOTKEYS.items():
            vk, modifiers = values[0], reduce(lambda x, y: x | y, values[1:])
            print 'INFO - Registering id', id, 'for key', vk
            if not self.user32.RegisterHotKey (None, id, modifiers, vk):
                print 'DEBUG - in AfterCopy.keyevent.Windows: Unable to register id', id

    def make_hotkeys_actions(self,jar):
        self.HOTKEYS = {}
        self.HOTKEY_ACTIONS = {}
        count = 0
        for i in jar:
            self.HOTKEYS[count] = i['key']
            self.HOTKEY_ACTIONS[count] = i['function']
            count+=1

    def event_loop(self):
        try:
          msg = wintypes.MSG()
          while self.user32.GetMessageA(self.byref(msg), None, 0, 0) != 0:
            if msg.message == win32con.WM_HOTKEY:
              action = self.HOTKEY_ACTIONS.get(msg.wParam)
              if action:
                action()
            self.user32.TranslateMessage(self.byref(msg))
            self.user32.DispatchMessageA(self.byref(msg))
        finally:
          for id in self.HOTKEYS.keys():
            self.user32.UnregisterHotKey(None, id)
            print 'INFO - user32.UnregisterHotKey(None,',id,')'