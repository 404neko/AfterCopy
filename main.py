from main_import import *

CONFIG = {
    'module':'default',
    'HIDE':1
}

from config import *
module = __import__('module.'+CONFIG['module'])

clipboard_ = clipboard.ClipBoard()
interface_ = interface.Interface()
keyevent_ = keyevent.KeyEvent()
module_ = module.default.Module(clipboard_, interface_, keyevent_)

keyevent_.set_hotkey_jar(module_.get_hotkey_jar())

keyevent_.event_loop()