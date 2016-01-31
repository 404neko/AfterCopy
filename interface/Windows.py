from error import *
import os
import struct

import win32api
import win32gui
import win32con

class PyNOTIFYICONDATA:
    _struct_format = (
        'I'
        'I'
        'I'
        'I'
        'I'
        'I'
        '128s'
        'I'
        'I'
        '256s'
        'I'
        '64s'
        'I'
    )

    _struct = struct.Struct(_struct_format)

    hWnd = 0
    uID = 0
    uFlags = 0
    uCallbackMessage = 0
    hIcon = 0
    szTip = ''
    dwState = 0
    dwStateMask = 0
    szInfo = ''
    uTimeoutOrVersion = 0
    szInfoTitle = ''
    dwInfoFlags = 0

    def pack(self):
        return self._struct.pack(
            self._struct.size,
            self.hWnd,
            self.uID,
            self.uFlags,
            self.uCallbackMessage,
            self.hIcon,
            self.szTip,
            self.dwState,
            self.dwStateMask,
            self.szInfo,
            self.uTimeoutOrVersion,
            self.szInfoTitle,
            self.dwInfoFlags
        )

    def __setattr__(self, name, value):
        if not hasattr(self, name):
            raise NameError, name
        self.__dict__[name] = value

class Interface:
    def __init__(self):
        msg_TaskbarRestart = win32gui.RegisterWindowMessage('TaskbarCreated');
        message_map = {
                msg_TaskbarRestart: self.OnRestart,
                win32con.WM_DESTROY: self.OnDestroy,
                win32con.WM_COMMAND: self.OnCommand,
                win32con.WM_USER + 20 : self.OnTaskbarNotify,
        }

        wc = win32gui.WNDCLASS()
        hinst = wc.hInstance = win32api.GetModuleHandle(None)
        wc.lpszClassName = 'AfterCopy'
        wc.style = win32con.CS_VREDRAW | win32con.CS_HREDRAW;
        wc.hCursor = win32api.LoadCursor(0, win32con.IDC_ARROW)
        wc.hbrBackground = win32con.COLOR_WINDOW
        wc.lpfnWndProc = message_map

        try:
            win32gui.RegisterClass(wc)
        except win32gui.error, err_info:
            if err_info.winerror != winerror.ERROR_CLASS_ALREADY_EXISTS:
                raise

        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        self.hwnd = win32gui.CreateWindow(wc.lpszClassName, 'AfterCopy Taskbar', style, \
                0, 0, win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT, \
                0, 0, hinst, None)
        win32gui.UpdateWindow(self.hwnd)
        self._DoCreateIcons()

    def _DoCreateIcons(self):
        hinst = win32api.GetModuleHandle(None)
        iconPathName = os.getcwd()+'\\_Resources\\AfterCopy.ico'
        if os.path.isfile(iconPathName):
            icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
            hicon = win32gui.LoadImage(hinst, iconPathName, win32con.IMAGE_ICON, 0, 0, icon_flags)
        else:
            print 'DEBUG - in AfterCopy.interface.Windows: Can\'t find icon file - using default'
            hicon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)

        flags = win32gui.NIF_ICON | win32gui.NIF_MESSAGE | win32gui.NIF_TIP
        nid = (self.hwnd, 0, flags, win32con.WM_USER + 20, hicon, 'AfterCopy v0.0.1')
        try:
            win32gui.Shell_NotifyIcon(win32gui.NIM_ADD, nid)
        except win32gui.error:
            print 'FAULT - in AfterCopy.interface.Windows: Failed to add the taskbar icon - is explorer running?'

    def OnRestart(self, hwnd, msg, wparam, lparam):
        self._DoCreateIcons()

    def OnDestroy(self, hwnd, msg, wparam, lparam):
        nid = (self.hwnd, 0)
        win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, nid)
        win32gui.PostQuitMessage(0)

    def HideWindow(self):
        ConsoleWindow=ctypes.windll.kernel32.GetConsoleWindow()
        if ConsoleWindow!=0:
            ctypes.windll.user32.ShowWindow(ConsoleWindow,0)
            ctypes.windll.kernel32.CloseHandle(ConsoleWindow)
        self.ShowBalloon('Notice','Console window hided')

    def ShowBalloon(self, title, msg):
        NIF_INFO = 16
        NIIF_INFO = 1
        NIM_MODIFY =1
        nid = PyNOTIFYICONDATA()
        nid.hWnd = self.hwnd
        nid.uFlags = NIF_INFO

        nid.dwInfoFlags = NIIF_INFO
        nid.szInfo = msg[:64]
        nid.szInfoTitle = title[:256]

        from ctypes import windll
        Shell_NotifyIcon = windll.shell32.Shell_NotifyIconA
        Shell_NotifyIcon(NIM_MODIFY, nid.pack())

    def OnTaskbarNotify(self, hwnd, msg, wparam, lparam):
        global Switch_Button
        if lparam == win32con.WM_LBUTTONUP:
            if Switch_Button > 0:
                ct = win32api.GetConsoleTitle()   
                hd = win32gui.FindWindow(0, ct)   
                win32gui.ShowWindow(hd, 0)
                Switch_Button = -1
            elif Switch_Button < 0:
                ct = win32api.GetConsoleTitle()   
                hd = win32gui.FindWindow(0, ct)   
                win32gui.ShowWindow(hd, 1)
                Switch_Button = 1
        elif lparam == win32con.WM_RBUTTONUP:
            menu = win32gui.CreatePopupMenu()
            win32gui.AppendMenu(menu, win32con.MF_STRING, 1024, 'Config')
            win32gui.AppendMenu(menu, win32con.MF_STRING, 1025, 'Exit')
            pos = win32gui.GetCursorPos()
            win32gui.SetForegroundWindow(self.hwnd)
            win32gui.TrackPopupMenu(menu, win32con.TPM_LEFTALIGN, pos[0], pos[1], 0, self.hwnd, None)
            win32gui.PostMessage(self.hwnd, win32con.WM_NULL, 0, 0)
        return 1

    def OnCommand(self, hwnd, msg, wparam, lparam):
        uin = win32api.LOWORD(wparam)
        if uin == 1024:
            pass
        elif uin == 1025:
            print 'INFO - Byebye'
            win32gui.DestroyWindow(self.hwnd)
            sys.exit(0)
        else:
            print 'DEBUG - in AfterCopy.interface.Windows: Unknow command ', uin