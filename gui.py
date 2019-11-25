#!/usr/bin/python3

import os
import sys
import shutil
import string
import subprocess
import configparser
import re
import bhelper
import cpfile
import bdef
import utils
from time import localtime, strftime
from tkinter import Tk,Toplevel,Menu,Listbox,messagebox,filedialog,StringVar,END,X,Y,LEFT,RIGHT,BOTH,RIDGE,FLAT,BOTTOM,EXTENDED,SINGLE,PhotoImage,Scrollbar,LabelFrame,Text
from tkinter.ttk import Style,Frame,Label,Combobox,Entry,Button,Notebook,Labelframe

##############################################
#region METHODE
def UpdateGlobalVariable(event):
    global BOARD,PANEL,BRAND,LAUNCHER,VOICE,REMOTE,KEYBOARD,VERSION,MODEL,MDIR

    BOARD    = bhelper.remove_unuse_char(cmbBoard.get())
    PANEL    = bhelper.remove_unuse_char(cmbPanel.get())
    BRAND    = bhelper.remove_unuse_char(cmbBrand.get())
    LAUNCHER = bhelper.remove_unuse_char(cmbLauncher.get())
    VOICE    = bhelper.remove_unuse_char(cmbVoice.get())
    REMOTE   = bhelper.remove_unuse_char(cmbRemote.get())
    KEYBOARD = bhelper.remove_unuse_char(cmbKeyboard.get())
    VERSION   = bhelper.remove_unuse_char(strVersion.get())

    MDIR = os.path.dirname(os.path.abspath(__file__))

    MODEL   = "{}_{}_{}_{}_{}_{}_{}".format(BOARD, PANEL, BRAND, LAUNCHER, VOICE, REMOTE, KEYBOARD)    

    strfwName.set(MODEL)
    
    print("[i] Global variables have been updated.")

def LoadAppConfig():
    global APP_CONFIG,APP_CONFIG_FILE
    APP_CONFIG_FILE = os.path.dirname(os.path.abspath(__file__)) + "/configs/appconfig.ini"
    APP_CONFIG = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
    APP_CONFIG.read(APP_CONFIG_FILE)
    # BOARD
    global BOARD_LIST,BOARD_DEFAULT
    h_board_list = APP_CONFIG.get('BOARD', 'List', raw = True)
    BOARD_LIST = h_board_list.split()
    BOARD_DEFAULT = APP_CONFIG['BOARD']['default']
    # PANEL
    global PANEL_LIST,PANEL_DEFAULT
    h_panel_list = APP_CONFIG.get('PANEL', 'List', raw = True)
    PANEL_LIST = h_panel_list.split()
    PANEL_DEFAULT = APP_CONFIG['PANEL']['default']
    # BRAND
    global BRAND_LIST,BRAND_DEFAULT
    h_brand_list = APP_CONFIG.get('BRAND', 'List', raw = True)
    BRAND_LIST = h_brand_list.split()
    BRAND_DEFAULT = APP_CONFIG['BRAND']['default']
    # LAUNCHER
    global LAUNCHER_LIST,LAUNCHER_DEFAULT
    h_launcher_list = APP_CONFIG.get('LAUNCHER', 'List', raw = True)
    LAUNCHER_LIST = h_launcher_list.split()
    LAUNCHER_DEFAULT = APP_CONFIG['LAUNCHER']['default']
    # VOICE
    global VOICE_LIST,VOICE_DEFAULT
    h_voice_list = APP_CONFIG.get('VOICE', 'List', raw = True)
    VOICE_LIST = h_voice_list.split()
    VOICE_DEFAULT = APP_CONFIG['VOICE']['default']
    # REMOTE
    global REMOTE_LIST,REMOTE_DEFAULT
    h_remote_list = APP_CONFIG.get('REMOTE', 'List', raw = True)
    REMOTE_LIST = h_remote_list.split()
    REMOTE_DEFAULT = APP_CONFIG['REMOTE']['default']
    # KEYBOARD
    global KEYBOARD_LIST,KEYBOARD_DEFAULT
    h_keyboard_list = APP_CONFIG.get('KEYBOARD', 'List', raw = True)
    KEYBOARD_LIST = h_keyboard_list.split()
    KEYBOARD_DEFAULT = APP_CONFIG['KEYBOARD']['default']
    # VERSION
    global VERSION_DEFAULT
    VERSION_DEFAULT = APP_CONFIG['VERSION']['default']
    print("[i] Application configs have been loaded.")

def SaveAppConfig():
    APP_CONFIG['BOARD']['default']    = str(cmbBoard.current())
    APP_CONFIG['PANEL']['default']    = str(cmbPanel.current())
    APP_CONFIG['BRAND']['default']    = str(cmbBrand.current())
    APP_CONFIG['LAUNCHER']['default'] = str(cmbLauncher.current())
    APP_CONFIG['VOICE']['default']    = str(cmbVoice.current())
    APP_CONFIG['REMOTE']['default']    = str(cmbRemote.current())
    APP_CONFIG['KEYBOARD']['default']    = str(cmbKeyboard.current())
    APP_CONFIG['VERSION']['default']   = strVersion.get()
    with open(APP_CONFIG_FILE, 'w') as configfile:
        APP_CONFIG.write(configfile)
    print("[i] Application configs have been saved.")

#endregion
##############################################
#region app EVENT HANDLER
def btnStart_Click():
    result = messagebox.askyesno("Thông báo", "Bạn có chắc là muốn build phiên bản này?", parent=app)
    if not result: return

    app.withdraw()
    print("[i] START")
    cmd = "python3 [MDIR]/auto.py {} {} {} {} {} {} {} {}".format(BOARD,PANEL,BRAND,LAUNCHER,VOICE,REMOTE,KEYBOARD,VERSION)
    cmd = cmd.replace("[MDIR]", MDIR)
    os.system(cmd)
    app.deiconify()
    print("[i] DONE")

def appExit_Click():
    SaveAppConfig()
    quit()

def btnAddNewBin_Click():
    return

#endregion
##############################################
# INIT
##############################################
LoadAppConfig()

##############################################
# UI
##############################################
#region FormMain
app = Tk()
app.geometry("380x310+200+200")

app.title("mstar-bin-tool-gui")
app.resizable(0,0)

app.protocol("WM_DELETE_WINDOW", appExit_Click)

#endregion
#region FormMain/FrameParent
frameParent = Frame(app, relief=RIDGE, borderwidth=1)
frameParent.pack(fill=BOTH, expand=True, padx=3, pady=3)
#endregion
#region FormMain/FrameParent/FrameBoard
frmBoard = Frame(frameParent)
frmBoard.pack(fill=X)
lblBoard = Label(frmBoard, text="Mã board", width=15)
lblBoard.pack(side=LEFT, padx=5, pady=8)
cmbBoard = Combobox(frmBoard, state="readonly", values=BOARD_LIST)
cmbBoard.pack(fill=X, padx=5, expand=True)
cmbBoard.current(int(BOARD_DEFAULT))
cmbBoard.bind("<<ComboboxSelected>>", UpdateGlobalVariable)
#endregion
#region FormMain/FrameParent/FramePanel
frmPanel = Frame(frameParent)
frmPanel.pack(fill=X)
lblPanel = Label(frmPanel, text="Mã panel", width=15)
lblPanel.pack(side=LEFT, padx=5, pady=5)
cmbPanel = Combobox(frmPanel, state="readonly", values=PANEL_LIST)
cmbPanel.pack(fill=X, padx=5, expand=True)
cmbPanel.current(int(PANEL_DEFAULT))
cmbPanel.bind("<<ComboboxSelected>>", UpdateGlobalVariable)
#endregion
#region FormMain/FrameParent/FrameBrand
frmBrand = Frame(frameParent)
frmBrand.pack(fill=X)
lblBrand = Label(frmBrand, text="Thương hiệu", width=15)
lblBrand.pack(side=LEFT, padx=5, pady=5)
cmbBrand = Combobox(frmBrand, state="readonly", values=BRAND_LIST)
cmbBrand.pack(fill=X, padx=5, expand=True)
cmbBrand.current(int(BRAND_DEFAULT))
cmbBrand.bind("<<ComboboxSelected>>", UpdateGlobalVariable)
#endregion
#region FormMain/FrameParent/FrameLauncher
frmLauncher = Frame(frameParent)
frmLauncher.pack(fill=X)
lblLauncher = Label(frmLauncher, text="Giao diện", width=15)
lblLauncher.pack(side=LEFT, padx=5, pady=5)
cmbLauncher = Combobox(frmLauncher, state="readonly", values=LAUNCHER_LIST)
cmbLauncher.pack(fill=X, padx=5, expand=True)
cmbLauncher.current(int(LAUNCHER_DEFAULT))
cmbLauncher.bind("<<ComboboxSelected>>", UpdateGlobalVariable)
#endregion
#region FormMain/FrameParent/FrameVoice
frmVoice = Frame(frameParent)
frmVoice.pack(fill=X)
lblVoice = Label(frmVoice, text="Giọng nói", width=15)
lblVoice.pack(side=LEFT, padx=5, pady=5)
cmbVoice = Combobox(frmVoice, state="readonly", values=VOICE_LIST)
cmbVoice.pack(fill=X, padx=5, expand=True)
cmbVoice.current(int(VOICE_DEFAULT))
cmbVoice.bind("<<ComboboxSelected>>", UpdateGlobalVariable)
#endregion
#region FormMain/FrameParent/FrameRemote
frmRemote = Frame(frameParent)
frmRemote.pack(fill=X)
lblRemote = Label(frmRemote, text="Remote", width=15)
lblRemote.pack(side=LEFT, padx=5, pady=5)
cmbRemote = Combobox(frmRemote, state="readonly", values=REMOTE_LIST)
cmbRemote.pack(fill=X, padx=5, expand=True)
cmbRemote.current(int(REMOTE_DEFAULT))
cmbRemote.bind("<<ComboboxSelected>>", UpdateGlobalVariable)
#endregion
#region FormMain/FrameParent/FrameKeyboard
frmKeyboard = Frame(frameParent)
frmKeyboard.pack(fill=X)
lblKeyboard = Label(frmKeyboard, text="Bàn phím", width=15)
lblKeyboard.pack(side=LEFT, padx=5, pady=5)
cmbKeyboard = Combobox(frmKeyboard, state="readonly", values=KEYBOARD_LIST)
cmbKeyboard.pack(fill=X, padx=5, expand=True)
cmbKeyboard.current(int(KEYBOARD_DEFAULT))
cmbKeyboard.bind("<<ComboboxSelected>>", UpdateGlobalVariable)
#endregion
#region FormMain/FrameParent/FrameVersion
frmVersion = Frame(frameParent)
frmVersion.pack(fill=X)
lblVersion = Label(frmVersion, text="Phiên bản", width=15)
lblVersion.pack(side=LEFT, padx=5, pady=5)
strVersion = StringVar()
strVersion.set(VERSION_DEFAULT)
entVersion = Entry(frmVersion, textvariable=strVersion)
entVersion.pack(fill=X, padx=5, expand=True)
entVersion.bind("<KeyRelease>", UpdateGlobalVariable)
#endregion
#region FormMain/FrameParent/FrameFirmwareNameLabel
frmFW = Frame(frameParent)
frmFW.pack(fill=BOTH, expand=True)
strfwName = StringVar()
lblFWName = Label(frmFW, textvariable=strfwName)
lblFWName.pack(side=BOTTOM, padx=5, expand=True)
#endregion
#region FormMain/FrameParent/Buttons
btnStart = Button(app, text="Bắt đầu", command=btnStart_Click)
btnStart.pack(side=RIGHT, padx=3, pady=3)
# btnAddBin = Button(app, text="Chọn BIN mới", command=btnAddNewBin_Click)
# btnAddBin.pack(side=LEFT, padx=3, pady=3)
#endregion
##############################################

##############################################
#region FormMain/MenuBar
menubar = Menu(app)
filemenu = Menu(menubar, tearoff = 0)
filemenu.add_command(label = "Exit", command = appExit_Click)
menubar.add_cascade(label = "File", menu = filemenu)

#endregion
##############################################
UpdateGlobalVariable(app)
#app.config(menu = menubar)
app.mainloop()
