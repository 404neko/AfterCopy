from PIL import Image
from PIL import ImageGrab
import os
import time
import WeiboPic

def CreatFolder(Path):
    if Path.find('/')==-1:
        if not os.path.exists(Path):
            os.mkdir(Path)
    else:
        Path=Path.split('/')
        Path0=''
        for PathItem in Path:
            Path0=Path0+PathItem+'/'
            if not os.path.exists(Path0):
                os.mkdir(Path0)

class Module:

    def __init__(self,clipboard,interface,keyevent):
        self.clipboard = clipboard
        self.interface = interface
        self.keyevent = keyevent
        self.win32con = keyevent.key_dict
        #bitmap = self.bitmap
        #text = self.text
        #files = self.files
        def handle_win_f10():
            clipboard_content = self.clipboard.get()
            if clipboard_content[0]=='BITMAP':
                self.bitmap(clipboard_content[1])
            if clipboard_content[0]=='UNICODE':
                self.unicode(clipboard_content[1])
                return None
            if clipboard_content[0]=='TEXT':
                self.text(clipboard_content[1])
            if clipboard_content[0]=='FILES':
                self.files(clipboard_content[1])
        self.hotkey_jar = [
            {
             'function':handle_win_f10,
                'key': (self.win32con.VK_F10, self.win32con.MOD_CONTROL)
            },
        ]
        CreatFolder('Data/Pictures')
        self.text_file_handle = open('Data/Clipboard.txt','a+')

    def reload(self):
        try:
            self.text_file_handle.close()
        except:
            pass
        self.text_file_handle = open('Data/Clipboard.txt','a+')

    def unicode(self,builtin_unicode):
        self.text_file_handle.write(str(int(time.time())))
        self.text_file_handle.write(' --- ')
        self.text_file_handle.write(builtin_unicode.encode('GBK'))
        self.text_file_handle.write('\r\n')
        self.interface.ShowBalloon('INFO','INFO - Text logged.')

    def get_hotkey_jar(self):
        return self.hotkey_jar

    def bitmap(self,PIL_Image):
        self.last_picture = str(int(time.time()))
        PIL_Image.save('Data/Pictures/'+self.last_picture+'.png','PNG')
        print 'INFO - Picture saved at '+os.getcwd()+'/Data/Pictures/'+self.last_picture+'.png'
        self.clipboard.put(os.getcwd()+'/Data/Pictures/'+self.last_picture+'.png')
        self.interface.ShowBalloon('INFO','INFO - Picture saved at '+os.getcwd()+'/Data/Pictures/'+self.last_picture+'.png')
        url = WeiboPic.Upload(os.path.split(os.getcwd()+'/Data/Pictures/'+self.last_picture+'.png'))
        if url[0]=='ERROR':
            self.interface.ShowBalloon('ERROR','Picture upload fail.')
        else:
            self.clipboard.put(url[1])
            self.interface.ShowBalloon('INFO','Picture url has puted in the clipboard.')

    def text(self,builtin_str):
        self.text_file_handle.write(str(int(time.time())))
        self.text_file_handle.write(' --- ')
        self.text_file_handle.write(builtin_str)
        self.text_file_handle.write('\r\n')
        self.interface.ShowBalloon('INFO','INFO - Text logged.')

    def files(self,hdrop):
        print 'INFO - File copyed:',hdrop