from PIL import Image
from PIL import ImageGrab

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

    def get_hotkey_jar(self):
        return self.hotkey_jar

    def bitmap(self,PIL_Image):
        PIL_Image.save()

    def text(self,builtin_str):
        print builtin_str

    def files(self,hdrop):
        print hdrop