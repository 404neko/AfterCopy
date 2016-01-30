from error import *
import platform

try:
    clipboard = __import__('clipboard.'+platform.system())
    clipboard = eval('clipboard.'+platform.system())
except:
    print 'FAULT - in AfterCopy.main_import.'
    raise NecessaryLibraryNotFound('clipboard')

try:
    interface = __import__('interface.'+platform.system())
    interface = eval('interface.'+platform.system())
except:
    print 'FAULT - in AfterCopy.main_import.'
    raise NecessaryLibraryNotFound('interface')

try:
    keyevent = __import__('keyevent.'+platform.system())
    keyevent = eval('keyevent.'+platform.system())
except:
    print 'FAULT - in AfterCopy.main_import.'
    raise NecessaryLibraryNotFound('keyevent')