from error import *
import ctypes

class KeyEvent:

    def __init__(self):
        try:
            import pyHook
        except:
            raise NecessaryLibraryNotFound('pyHook')
        try:
            import win32gui
        except:
            raise NecessaryLibraryNotFound('win32gui')
        __init()

    def on_keyboard_event(self):


    def __init(self):
        hook_manager = pyHook.HookManager()
        hook_manager.KeyDown = self.on_keyboard_event
        hook_manager.HookKeyboard()
        win32gui.PumpMessages()

    def 