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
# DEFINE
##############################################
_TAB_ACTIVE_ID = -2
_TAB_ALL_ID = -1
_TAB_SYS_ID = 0
_TAB_PRV_ID = 1
_TAB_USR_ID = 2
_TAB_BIN_ID = 3

##############################################
#region METHODE
def UpdateGlobalVariable(event):
    global G_BOARD,G_PANEL,G_BRAND,G_LAUNCHER,G_VOICE,G_REMOTE,G_KEYBOARD,G_VERNUM,G_MODEL,G_PACK_CONFIG_FILE,G_ANIMATION_CONFIG_FILE,G_MSTAR_TOOL_DIR,G_INPUT_DIR,G_UNPACK_DIR,G_ANDROID_DIR,G_TV_ROM_DIR,G_SOFTWARE_DIR,G_MODEL_DIR,G_WORKING_DIR,G_APK_IN_DIR

    G_BOARD    = bhelper.remove_unuse_char(cmbBoard.get())
    G_PANEL    = bhelper.remove_unuse_char(cmbPanel.get())
    G_BRAND    = bhelper.remove_unuse_char(cmbBrand.get())
    G_LAUNCHER = bhelper.remove_unuse_char(cmbLauncher.get())
    G_VOICE    = bhelper.remove_unuse_char(cmbVoice.get())
    G_REMOTE   = bhelper.remove_unuse_char(cmbRemote.get())
    G_KEYBOARD = bhelper.remove_unuse_char(cmbKeyboard.get())
    G_VERNUM   = bhelper.remove_unuse_char(strVernum.get())

    if bdef.is_P150638V601G(G_BOARD):
        G_APK_IN_DIR = True
    else:
        G_APK_IN_DIR = False

    G_MSTAR_TOOL_DIR = os.path.dirname(os.path.abspath(__file__))
    G_ANDROID_DIR    = G_MSTAR_TOOL_DIR + "/android"
    G_WORKING_DIR    = G_MSTAR_TOOL_DIR + "/working"
    G_TV_ROM_DIR     = "TV_ROM_{}_{}".format(G_VERNUM, G_BOARD)
    G_SOFTWARE_DIR   = os.path.dirname(G_MSTAR_TOOL_DIR) + "/{}/{}/{}/{}_{}/{}_{}_{}".format(G_TV_ROM_DIR, G_BOARD, G_PANEL, G_BRAND, G_LAUNCHER, G_VOICE, G_REMOTE, G_KEYBOARD) 

    G_MODEL   = "{}_{}_{}_{}".format(G_BOARD, G_PANEL, G_BRAND, G_LAUNCHER)    
    G_MODEL_DIR      = G_WORKING_DIR + "/" + G_MODEL
    G_UNPACK_DIR     = G_MODEL_DIR + "/unpack"
    G_INPUT_DIR      = G_MODEL_DIR + "/input"

    G_PACK_CONFIG_FILE        = G_MODEL_DIR + "/config/pack.ini"
    G_ANIMATION_CONFIG_FILE   = G_MODEL_DIR + "/config/animation.ini"

    if os.path.isdir(G_MODEL_DIR):
        strfwName.set(G_MODEL)
    else:
        strfwName.set("Phần mềm không tồn tại")
    opt.title(G_MODEL + "_" + G_VERNUM)
    print("[i] Global variables have been updated.")

def LoadAppConfig():
    global G_APP_CONFIG,G_APP_CONFIG_FILE
    G_APP_CONFIG_FILE = os.path.dirname(os.path.abspath(__file__)) + "/configs/appconfig.ini"
    G_APP_CONFIG = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
    G_APP_CONFIG.read(G_APP_CONFIG_FILE)
    # BOARD
    global G_BOARD_LIST,G_BOARD_DEFAULT
    h_board_list = G_APP_CONFIG.get('BOARD', 'List', raw = True)
    G_BOARD_LIST = h_board_list.split()
    G_BOARD_DEFAULT = G_APP_CONFIG['BOARD']['default']
    # PANEL
    global G_PANEL_LIST,G_PANEL_DEFAULT
    h_panel_list = G_APP_CONFIG.get('PANEL', 'List', raw = True)
    G_PANEL_LIST = h_panel_list.split()
    G_PANEL_DEFAULT = G_APP_CONFIG['PANEL']['default']
    # BRAND
    global G_BRAND_LIST,G_BRAND_DEFAULT
    h_brand_list = G_APP_CONFIG.get('BRAND', 'List', raw = True)
    G_BRAND_LIST = h_brand_list.split()
    G_BRAND_DEFAULT = G_APP_CONFIG['BRAND']['default']
    # LAUNCHER
    global G_LAUNCHER_LIST,G_LAUNCHER_DEFAULT
    h_launcher_list = G_APP_CONFIG.get('LAUNCHER', 'List', raw = True)
    G_LAUNCHER_LIST = h_launcher_list.split()
    G_LAUNCHER_DEFAULT = G_APP_CONFIG['LAUNCHER']['default']
    # VOICE
    global G_VOICE_LIST,G_VOICE_DEFAULT
    h_voice_list = G_APP_CONFIG.get('VOICE', 'List', raw = True)
    G_VOICE_LIST = h_voice_list.split()
    G_VOICE_DEFAULT = G_APP_CONFIG['VOICE']['default']
    # REMOTE
    global G_REMOTE_LIST,G_REMOTE_DEFAULT
    h_remote_list = G_APP_CONFIG.get('REMOTE', 'List', raw = True)
    G_REMOTE_LIST = h_remote_list.split()
    G_REMOTE_DEFAULT = G_APP_CONFIG['REMOTE']['default']
    # KEYBOARD
    global G_KEYBOARD_LIST,G_KEYBOARD_DEFAULT
    h_keyboard_list = G_APP_CONFIG.get('KEYBOARD', 'List', raw = True)
    G_KEYBOARD_LIST = h_keyboard_list.split()
    G_KEYBOARD_DEFAULT = G_APP_CONFIG['KEYBOARD']['default']
    # VERSION
    global G_VERNUM_DEFAULT
    G_VERNUM_DEFAULT = G_APP_CONFIG['VERSION']['vernum']
    print("[i] Application configs have been loaded.")

def SaveAppConfig():
    G_APP_CONFIG['BOARD']['default']    = str(cmbBoard.current())
    G_APP_CONFIG['PANEL']['default']    = str(cmbPanel.current())
    G_APP_CONFIG['BRAND']['default']    = str(cmbBrand.current())
    G_APP_CONFIG['LAUNCHER']['default'] = str(cmbLauncher.current())
    G_APP_CONFIG['VOICE']['default']    = str(cmbVoice.current())
    G_APP_CONFIG['REMOTE']['default']    = str(cmbRemote.current())
    G_APP_CONFIG['KEYBOARD']['default']    = str(cmbKeyboard.current())
    G_APP_CONFIG['VERSION']['vernum']   = strVernum.get()
    with open(G_APP_CONFIG_FILE, 'w') as configfile:
        G_APP_CONFIG.write(configfile)
    print("[i] Application configs have been saved.")

def MstarTool(script_name):
    return G_MSTAR_TOOL_DIR + "/" + script_name

def Beep(cnt=1):
    for x in range(0, cnt):        
        print("[i] Beep ({})".format(cnt-x))
        # winsound.PlaySound("resource/sound/beep-07.wav", winsound.SND_FILENAME) # winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
        os.system("aplay resource/sound/beep-07.wav")

Beep(10)
quit()

def CheckModelFolderExist():
    err = ""
    if not os.path.isdir(G_MODEL_DIR):
        print("[!] Error: Can not find '{}'".format(G_MODEL_DIR))
        err = "Phần mềm không tồn tại!"

    global G_INPUT_FILE
    file_name = bhelper.first_file(G_INPUT_DIR, ".bin")
    G_INPUT_FILE = G_INPUT_DIR + "/" + file_name
    if not err and not os.path.isfile(G_INPUT_FILE):
        print("[!] Error: Can not find '{}'".format(G_INPUT_FILE))
        err = "Không tìm thấy tập tin *.BIN trong thư mục " + G_INPUT_DIR

    if not err and not os.path.isfile(G_PACK_CONFIG_FILE):
        print("[!] Error: Can not find '{}'".format(G_PACK_CONFIG_FILE))
        err = "Không tìm thấy tập tin " + G_PACK_CONFIG_FILE

    if not err and not os.path.isfile(G_ANIMATION_CONFIG_FILE):
        print("[!] Error: Can not find '{}'".format(G_ANIMATION_CONFIG_FILE))
        err = "Không tìm thấy tập tin " + G_ANIMATION_CONFIG_FILE

    if err:
        messagebox.showwarning("Thông báo", err, parent=app)
        return False
    return True
#endregion
##############################################
#region BUILD SCRIPT
def DoUnpackBinFile():
    print("[i] Unpack *.BIN file")
    bhelper.create_dir_if_not_exist(G_UNPACK_DIR)
    bhelper.run_script(MstarTool("unpack.py"), [G_INPUT_FILE, G_UNPACK_DIR])

def DoExtractSystemImgFile():
    print("[i] Extract system.img to /android/temp/system")
    print("    Please wait...")
    bhelper.create_dir_if_not_exist(G_ANDROID_DIR + "/temp/system")
    bhelper.run_tool(G_ANDROID_DIR + "/bin/ImgExtractor.exe", [G_UNPACK_DIR + "/system.img", G_ANDROID_DIR + "/temp/system"])
    
    global G_SYSTEM_APP_DIR,G_PRIV_APP_DIR,G_USER_APP_DIR
    G_SYSTEM_APP_DIR = G_ANDROID_DIR + "/temp/system/app"
    G_PRIV_APP_DIR   = G_ANDROID_DIR + "/temp/system/priv-app"

    if bdef.is_tt(G_BOARD):
        G_USER_APP_DIR   = G_ANDROID_DIR + "/temp/system/customer_preinstall"
    else:
        G_USER_APP_DIR = G_ANDROID_DIR + "/temp/system/media/user_system_apks"
    bhelper.create_dir_if_not_exist(G_USER_APP_DIR)

def DoMakeAnimation():
    print("[i] Make bootanimation.zip")
    ani_config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
    ani_config.read(G_ANIMATION_CONFIG_FILE)
    ani_config_main = ani_config['Main']
    ANI_DIR     = G_BRAND.lower()
    if ani_config.has_option('Main','ani_dir'):
        ANI_DIR = ani_config_main['ani_dir']
    ANI_WIDTH   = ani_config_main['ani_width']
    ANI_HEIGHT  = ani_config_main['ani_height']
    ANI_FPS     = ani_config_main['ani_fps']
    ANI_COLOR   = ani_config_main['ani_color']
    ANI_BACK    = ani_config_main['ani_back']
    VERSION = "{}.{}.{}{}".format(G_BRAND, G_LAUNCHER, G_VOICE, G_VERNUM)
    ver = VERSION
    padx = 20
    pady = 20
    if G_BRAND == "ANDROID":
        ver = "AndroidTV"
        padx = 0
        pady = 0
    aniOptions = "-t {} -i {} -o {} -w {} -h {} -s {} --color {} --size {} --back {} --padx {} --pady {} -v".format(ver, G_MSTAR_TOOL_DIR + "/resource/bootanimation/" + ANI_DIR, G_ANDROID_DIR + "/temp/system/media", ANI_WIDTH, ANI_HEIGHT, ANI_FPS,ANI_COLOR, "11", ANI_BACK, padx, pady)
    bhelper.run_tool(G_MSTAR_TOOL_DIR + "/bin/bmc/bmc.exe", [aniOptions])
    global G_LOG_SCREEN_RESOLUTION
    G_LOG_SCREEN_RESOLUTION = "{}x{}".format(ANI_WIDTH, ANI_HEIGHT)

def DoCopySystemLib():
    print("[i] Copy system/lib")
    SRC_DIR = G_MSTAR_TOOL_DIR + "/resource/system/lib/" + G_BOARD
    DES_DIR = G_MSTAR_TOOL_DIR + "/android/temp/system/lib"
    bhelper.copy_resource(SRC_DIR, DES_DIR)
    bhelper.copy_resource(SRC_DIR + "/" + G_VOICE, DES_DIR)

def DoCopySystemKL():
    print("[i] Copy system/")
    SRC_DIR = G_MSTAR_TOOL_DIR + "/resource/system/kl/" + G_BOARD
    DES_DIR = G_MSTAR_TOOL_DIR + "/android/temp/system/usr/keylayout"
    bhelper.copy_resource(SRC_DIR, DES_DIR)
    bhelper.copy_resource(SRC_DIR + "/" + G_REMOTE, DES_DIR)
    bhelper.copy_resource(SRC_DIR + "/" + G_KEYBOARD, DES_DIR)

def DoCopySystemBin():
    print("[i] Copy system/lib")
    SRC_DIR = G_MSTAR_TOOL_DIR + "/resource/system/bin/" + G_BOARD
    DES_DIR = G_MSTAR_TOOL_DIR + "/android/temp/system/bin"
    bhelper.copy_resource(SRC_DIR, DES_DIR)

def DoRemoveUnuseApk():
    print("[i] Remove old launcher")
    DES_DIR = G_MSTAR_TOOL_DIR + "/android/temp/system"
    for dx in os.listdir(DES_DIR + "/app"):
        if(re.search(r'launche', dx, re.IGNORECASE)):
            bhelper.delete_path(DES_DIR + "/app/" + dx)
    
    if bdef.is_P75338V621G(G_BOARD):
        bhelper.delete_path(DES_DIR + "/app/YouTuBe_Available.apk")
        bhelper.delete_path(DES_DIR + "/app/QuickSearchBox.apk")
        bhelper.delete_path(DES_DIR + "/customer_preinstall/VoiceSearch.apk")
    
    if bdef.is_cvt(G_BOARD):
        bhelper.delete_path(DES_DIR + "/priv-app/cvte-android-setting-inspire-mk.apk")        
        bhelper.delete_path(DES_DIR + "/priv-app/cvte-android-setting-inspire.apk")        
    
    if bdef.is_P150638V601G(G_BOARD):
        bhelper.delete_path(DES_DIR + "/app/MemManager")
        bhelper.delete_path(DES_DIR + "/app/UBCLauncher")
        bhelper.delete_path(DES_DIR + "/app/Youtube127")
        bhelper.delete_path(DES_DIR + "/priv-app/VoiceSearch")     
        bhelper.delete_path(DES_DIR + "/customer_preinstall/voice_blue")

    if bdef.is_338(G_BOARD):
        bhelper.delete_path(DES_DIR + "/app/Velvet.apk")

    btnOptItemUpdate_Click(_TAB_SYS_ID)

def DoCopyLauncher():
    print("[i] Copy launcher")
    LAUNCHER_DIR = "{}/{}/{}".format(G_BOARD, G_BRAND, G_LAUNCHER)
    SRC_DIR = G_MSTAR_TOOL_DIR + "/resource/system/launcher/" + LAUNCHER_DIR
    DES_DIR = G_MSTAR_TOOL_DIR + "/android/temp/system/app"
    bhelper.copy_resource(SRC_DIR, DES_DIR, G_APK_IN_DIR)
    btnOptItemUpdate_Click(_TAB_SYS_ID)

def DoCopySystemApp():
    print("[i] Copy system/app")
    SRC_DIR = G_MSTAR_TOOL_DIR + "/resource/system/sys-app/" + G_BOARD
    DES_DIR = G_SYSTEM_APP_DIR
    bhelper.copy_resource(SRC_DIR, DES_DIR, G_APK_IN_DIR)
    bhelper.copy_resource(SRC_DIR + "/" + G_VOICE, DES_DIR, G_APK_IN_DIR)
    btnOptItemUpdate_Click(_TAB_SYS_ID)

def DoCopySystemPrivApp():
    print("[i] Copy system/priv-app")
    SRC_DIR = G_MSTAR_TOOL_DIR + "/resource/system/priv-app/" + G_BOARD
    DES_DIR = G_PRIV_APP_DIR
    bhelper.copy_resource(SRC_DIR, DES_DIR, G_APK_IN_DIR)
    bhelper.copy_resource(SRC_DIR + "/" + G_VOICE, DES_DIR, G_APK_IN_DIR)
    btnOptItemUpdate_Click(_TAB_PRV_ID)

def DoCopyUserApk():
    print("[i] Copy user apk")
    SRC_DIR = G_MSTAR_TOOL_DIR + "/resource/system/user-app/" + G_BOARD
    DES_DIR = G_USER_APP_DIR
    if os.path.isdir(DES_DIR):
        bhelper.delete_path(DES_DIR)
    bhelper.create_dir_if_not_exist(DES_DIR)
    bhelper.copy_resource(SRC_DIR, DES_DIR, G_APK_IN_DIR)
    bhelper.copy_resource(SRC_DIR + "/" + G_VOICE, DES_DIR, G_APK_IN_DIR)
    btnOptItemUpdate_Click(_TAB_USR_ID)

def DoCopyTvconfig():
    print("[i] Copy modified img")
    SRC_DIR = G_MODEL_DIR + "/img_mod"
    DES_DIR = G_MODEL_DIR + "/unpack"
    bhelper.copy_resource(SRC_DIR, DES_DIR)
    bhelper.copy_resource(SRC_DIR + "/" + G_REMOTE, DES_DIR)

def DoRebuildSystemImgFile():
    print("[i] Clean build.prop")
    bhelper.clean_buildprop(G_ANDROID_DIR + "/temp/system/build.prop")
    bhelper.modify_buildprop(G_ANDROID_DIR + "/temp/system/build.prop", G_BOARD, G_PANEL)

    print("[i] Re-build system.img to /android")
    print("    Please wait...")
    Beep(2)
    bhelper.run_tool(G_ANDROID_DIR + "/START.exe")    # ./bin/genext2fs.exe -a -d ./temp/system -b 634880 -m 0 tmp_system.img

    print("[i] Move new system.img from /android to /unpack")
    bhelper.move_file(G_ANDROID_DIR + "/new_system.img", G_UNPACK_DIR + "/system.img")

def DoRepackBinFile():
    print("[i] Update new CRC")
    bhelper.update_config_crc(G_PACK_CONFIG_FILE)

    print("[i] Repack *.BIN file")
    bhelper.run_script(MstarTool("pack.py"), [G_PACK_CONFIG_FILE, G_UNPACK_DIR, G_INPUT_DIR])

    print("[i] Copy output file")
    TIME        = strftime("%Y%m%d_%H%M%S", localtime())
    FIRMWARE    = "{}_{}_{}_{}_{}_{}".format(G_MODEL, G_VOICE, G_REMOTE, G_KEYBOARD, G_VERNUM, TIME)
    _DIR      = G_SOFTWARE_DIR + "/{}_{}/{}".format(G_VERNUM, TIME, FIRMWARE)
    bhelper.create_dir_if_not_exist(_DIR)
    FW_FILE     = bhelper.first_file(G_INPUT_DIR)
    cpfile.copy_with_progress(G_INPUT_DIR + "/" + FW_FILE, _DIR + "/" + FW_FILE)

    print("\n")
    print("[i] Write log")
    
    # build log
    global G_NOTE
    G_NOTE = ""
    G_NOTE = G_NOTE + ("###\n")
    G_NOTE = G_NOTE + ("{}\n".format(FIRMWARE))
    G_NOTE = G_NOTE + ("- Filename   : {}\n".format(FW_FILE))
    G_NOTE = G_NOTE + ("- Datetime   : {}\n".format(TIME))
    G_NOTE = G_NOTE + ("- Checksum   : {}\n".format(bhelper.md5sum(G_INPUT_DIR + "/" + FW_FILE)))
    G_NOTE = G_NOTE + ("- Resolution : {}\n".format(G_LOG_SCREEN_RESOLUTION))
    G_NOTE = G_NOTE + ("- Remote     : {}\n".format(G_REMOTE))
    G_NOTE = G_NOTE + ("- Keyboard   : {}\n".format(G_KEYBOARD))
    G_NOTE = G_NOTE + ("- Voice      : {}\n".format(G_VOICE))
    G_NOTE = G_NOTE + ("- User apps  : \n")
    for dx in os.listdir(G_USER_APP_DIR):
        G_NOTE = G_NOTE + ("    + {}\n".format(dx))
    string_note = textBoxNote.get("1.0",END)
    string_note = string_note.replace("\r","").replace("\n", "\n    ")
    G_NOTE = G_NOTE + ("- Notes      : \n    " + string_note)
    G_NOTE = G_NOTE + ("\n\n")

    # write log
    _LOG_DIR = os.path.dirname(G_MSTAR_TOOL_DIR) + "/" + G_TV_ROM_DIR
    _LOG_FILE = _LOG_DIR + "/log.txt"
    old_data = "\n###\n"
    if os.path.isfile(_LOG_FILE):
        with open(_LOG_FILE, 'r', encoding="utf-8") as fo: 
            old_data = fo.read()
    with open(_LOG_FILE, 'w', encoding="utf-8") as f: 
        f.write(G_NOTE)
        f.write(old_data)

    print("\n[i] Completed!")

def DoCleanTemp():
    print("[i] Cleanup temporary files")
    bhelper.delete_path(G_ANDROID_DIR + "/temp")
    for dx in os.listdir(G_MSTAR_TOOL_DIR):
        if(re.match('^tmp[a-zA-Z0-9]+$', dx)):
            bhelper.delete_path(G_MSTAR_TOOL_DIR + "/" + dx)
    for dx in os.listdir(G_WORKING_DIR):
        bhelper.delete_path(G_WORKING_DIR + "/" + dx + "/unpack")
    if bdef.is_P75338V621G(G_BOARD):
        input_file = bhelper.first_file(G_INPUT_DIR)
        if input_file != "":
            bhelper.delete_path(G_INPUT_DIR + "/" + input_file)

#endregion
##############################################
#region opt EVENT HANDLER
def btnOptExit_Click():
    DoCleanTemp()
    app.deiconify()
    opt.withdraw()

def btnOptCopyDefaultApk_Click():
    DoRemoveUnuseApk()
    DoCopyLauncher()
    DoCopySystemApp()
    DoCopySystemPrivApp()
    DoCopyUserApk()
    Beep(2)
    print("[i] Done")

def btnOptBuild_Click():
    DoCopySystemLib()
    DoCopySystemKL()
    DoCopySystemBin()
    DoMakeAnimation()
    DoRebuildSystemImgFile()

    DoCopyTvconfig()
    DoRepackBinFile()

    tabOpt.select(3)
    btnOptItemUpdate_Click()
    Beep(5)
    print("[i] Done")
    messagebox.showinfo("Thành công", "Thông tin phần mềm:\n" + G_NOTE, parent=opt)

#endregion
##############################################
#region opt tab EVENT HANDLER
def btnOptItemRemove_Click():
    tabSelected = tabOpt.index(tabOpt.select())
    # if tabSelected == TAB_SYS:
    sel = listboxOptSystemApp.curselection()
    if tabSelected == _TAB_PRV_ID:
        sel = listboxOptPrivApp.curselection()
    if tabSelected == _TAB_USR_ID:
        sel = listboxOptUserApp.curselection()
    if tabSelected == _TAB_BIN_ID:
        sel = listboxOptBinFile.curselection()
    
    if len(sel) <= 0:
        print("    No file selected!")
        messagebox.showinfo("Thông báo", "Vui lòng chọn những tập tin cần xóa.", parent=opt)
        return

    result = messagebox.askyesno("Thông báo", "Bạn có chắc là muốn xóa những tập tin này?", parent=opt)
    if not result: return

    for i in sel[::-1]:
        if tabSelected == _TAB_SYS_ID:
            dx = listboxOptSystemApp.get(i)
            bhelper.delete_path(G_SYSTEM_APP_DIR + "/" + dx)
            listboxOptSystemApp.delete(i)
        if tabSelected == _TAB_PRV_ID:
            dx = listboxOptPrivApp.get(i)
            bhelper.delete_path(G_PRIV_APP_DIR + "/" + dx)
            listboxOptPrivApp.delete(i)
        if tabSelected == _TAB_USR_ID:
            dx = listboxOptUserApp.get(i)
            bhelper.delete_path(G_USER_APP_DIR + "/" + dx)
            listboxOptUserApp.delete(i)
        if tabSelected == _TAB_BIN_ID:
            dx = listboxOptBinFile.get(i)
            (board, panel, brand, launcher, voice, remote, keyboard, vernum, day, time) = dx.split("_")
            _DIR      = G_SOFTWARE_DIR + "/{}_{}_{}".format(vernum, day, time)
            bhelper.delete_path(_DIR)
            listboxOptBinFile.delete(i)

def btnOptItemAdd_Click():
    dp = filedialog.askopenfilename(title = "Chọn tập tin APK", filetypes = (("Apk files","*.apk"),("All files","*.*")))
    if dp:
        (base,ext) = os.path.splitext(dp)
        base = bhelper.remove_unuse_char(os.path.basename(base))        
        tabSelected = tabOpt.index(tabOpt.select())
        dir = ""
        item = base + ext
        if G_APK_IN_DIR: 
            dir = "/" + base
            item = base
        if tabSelected == _TAB_SYS_ID:
            ds = G_SYSTEM_APP_DIR
            listboxOptSystemApp.insert(END, item)
        if tabSelected == _TAB_PRV_ID:
            ds = G_PRIV_APP_DIR
            listboxOptPrivApp.insert(END, item)
        if tabSelected == _TAB_USR_ID:
            ds = G_USER_APP_DIR
            listboxOptUserApp.insert(END, item)

        ds = ds + dir
        bhelper.create_dir_if_not_exist(ds)
        cpfile.copy_with_progress(dp, ds + "/" + base + ext)
        print("\n    Added: " + base + ext)
    else:
        print("[i] Cancel")

def btnOptItemUpdate_Click(tab = _TAB_ACTIVE_ID):
    tabSelected = tab
    if tab == _TAB_ACTIVE_ID:
        print("[i] Actived tab: " + tabOpt.tab(tabOpt.select(), "text"))
        tabSelected = tabOpt.index(tabOpt.select())
    if tab == _TAB_ALL_ID or tabSelected == _TAB_SYS_ID:
        listboxOptSystemApp.delete(0,END)
        for dx in os.listdir(G_SYSTEM_APP_DIR):
            listboxOptSystemApp.insert(END, dx)
        print ("    Found {} system apk(s)".format(listboxOptSystemApp.size()))
    if tab == _TAB_ALL_ID or tabSelected == _TAB_PRV_ID:
        listboxOptPrivApp.delete(0,END)
        for dx in os.listdir(G_PRIV_APP_DIR):
            listboxOptPrivApp.insert(END, dx)
        print ("    Found {} private apk(s)".format(listboxOptPrivApp.size()))
    if tab == _TAB_ALL_ID or tabSelected == _TAB_USR_ID:
        listboxOptUserApp.delete(0,END)
        for dx in os.listdir(G_USER_APP_DIR):
            listboxOptUserApp.insert(END, dx)
        print ("    Found {} user apk(s)".format(listboxOptUserApp.size()))
    if tab == _TAB_ALL_ID or tabSelected == _TAB_BIN_ID:
        listboxOptBinFile.delete(0,END)
        if os.path.exists(G_SOFTWARE_DIR):
            for dy in os.listdir(G_SOFTWARE_DIR):
                for dx in os.listdir(G_SOFTWARE_DIR + "/" + dy):
                    listboxOptBinFile.insert(END, dx)
        print ("    Found {} BIN file(s)".format(listboxOptBinFile.size()))

def btnOptItemFolder_Click():
    tabSelected = tabOpt.index(tabOpt.select())
    if tabSelected == _TAB_SYS_ID:
        bhelper.open_path(G_SYSTEM_APP_DIR)
    if tabSelected == _TAB_PRV_ID:
        bhelper.open_path(G_PRIV_APP_DIR)
    if tabSelected == _TAB_USR_ID:
        bhelper.open_path(G_USER_APP_DIR)
    if tabSelected == _TAB_BIN_ID:
        bhelper.open_path(G_SOFTWARE_DIR)

def btnOptBinFileCopyUSB_Click():
    sel = listboxOptBinFile.curselection()
    if len(sel) <= 0:
        print("    No file selected!")
        messagebox.showinfo("Thông báo", "Vui lòng chọn phiên bản cần chép.", parent=opt)
        return    
    dx = ""
    for i in sel[::-1]:
        dx = listboxOptBinFile.get(i)
        print("    Selected: " + dx)

    (board, panel, brand, launcher, voice, remote, keyboard, vernum, day, time) = dx.split("_")
    dp = G_SOFTWARE_DIR + "/{}_{}_{}/{}_{}_{}_{}_{}_{}_{}".format(vernum, day, time, G_MODEL, voice, remote, keyboard, vernum, day, time)
    fname = bhelper.first_file(dp, "bin")
    fsrc = dp + "/" + fname
    print(fsrc)
    if not os.path.isfile(fsrc):
        print("    Bin file not found: " + dx)
        return
    
    dp = filedialog.asksaveasfilename(initialfile=fname, title = "Lưu tập tin", filetypes = (("Bin files","*.bin"),("All files","*.*")))
    if dp:
        print("    Copy: {}/{}".format(dx, fname))
        cpfile.copy_with_progress(fsrc, dp)
        print("")
        Beep(2)
        print("    Done")
#endregion
##############################################
#region menu EVENT HANDLER
def mnuOpenBinFolder_Click():
    if not os.path.isdir(G_MODEL_DIR):
        print("[!] Error: Can not find '" + G_MODEL_DIR + "'")
        messagebox.showwarning("Thông báo", "Phần mềm không tồn tại!", parent=app)
        return
    if not bhelper.open_path(G_SOFTWARE_DIR):
        messagebox.showwarning("Thông báo", "Chưa có phiên bản phần mềm nào của model này được build!", parent=app)
        return          

def mnuOpenWorkingFolder_Click():
    if not bhelper.open_path(G_MODEL_DIR):
        result = messagebox.askyesno("Thông báo", "Phần mềm không tồn tại!\nBạn có muốn tạo thư mục làm việc cho phần mềm này không?", parent=app)
        if result:
            bhelper.create_dir_if_not_exist(G_MODEL_DIR)
            bhelper.open_path(G_MODEL_DIR)
            
def mnuOpenAnimationCfg_Click():
    bhelper.open_path(G_ANIMATION_CONFIG_FILE)

def mnuOpenPackCfg_Click():
    bhelper.open_path(G_PACK_CONFIG_FILE)

def mnuOpenAppCfg_Click():
    bhelper.open_path(G_APP_CONFIG_FILE)

def mnuOpenAndroidFolder_Click():
    if not bhelper.open_path(G_ANDROID_DIR + "/temp/system"):
        bhelper.open_path(G_ANDROID_DIR)
        
def mnuOpenBuildprop_Click():
    if not bhelper.open_path(G_ANDROID_DIR + "/temp/system/build.prop"):
        messagebox.showinfo("Thông báo", "Chưa có tập tin build.prop", parent=opt)

def mnuOpenResForm_Click():
    quit()

def mnuOpenOutForm_Click():
    quit()

def mnuAddNewBin_Click():
    dp = filedialog.askopenfilename(title = "Chọn tập tin BIN", filetypes = (("BIN files","*.bin"),("All files","*.*")))
    if dp:
        print("[i] Copy new BIN")
        dp_file = os.path.basename(dp)
        ds = G_INPUT_DIR
        ds_file = bhelper.first_file(ds)
        if dp_file != ds_file and ds_file != "":
            result = messagebox.askyesno("Thông báo", "Tập tin BIN mới ({}) có tên khác với tập tin BIN có sẵn ({}). Bạn có chắc là muốn tiếp tục không?".format(dp_file, ds_file), parent=app)
            if not result: return
        if ds_file != "":
            bhelper.delete_path(ds + "/" + ds_file)
        bhelper.create_dir_if_not_exist(ds)
        print("    Copy '{}'\n    => from: {} \n    => to {}".format(dp_file, dp, ds))
        cpfile.copy_with_progress(dp, ds)
        print("\n    Added: " + dp_file)
        Beep(2)
        print("    Done")
    else:
        print("[i] Cancel")
#endregion
##############################################
#region app EVENT HANDLER
def btnStart_Click():
    if not CheckModelFolderExist(): return
    result = messagebox.askyesno("Thông báo", "Bạn có chắc là muốn build phiên bản này?", parent=app)
    if not result: return

    DoUnpackBinFile()
    DoExtractSystemImgFile()
    btnOptItemUpdate_Click(_TAB_ALL_ID)
    app.withdraw()
    opt.deiconify()
    Beep(2)

def btnClean_Click():
    DoCleanTemp()

def appExit_Click():
    DoCleanTemp()
    SaveAppConfig()
    quit()

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
app.geometry("300x310+200+200")

app.title("mstar-bin-tool-gui")
app.style = Style()
app.style.theme_use("winnative")
app.resizable(0,0)
app.iconbitmap("resource/icon/app.ico")

app.protocol("WM_DELETE_WINDOW", appExit_Click)

icon_sync   = PhotoImage(file="resource/icon/sync_x16.png")
icon_folder = PhotoImage(file="resource/icon/folder_x16.png")
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
cmbBoard = Combobox(frmBoard, state="readonly", values=G_BOARD_LIST)
cmbBoard.pack(fill=X, padx=5, expand=True)
cmbBoard.current(int(G_BOARD_DEFAULT))
cmbBoard.bind("<<ComboboxSelected>>", UpdateGlobalVariable)
#endregion
#region FormMain/FrameParent/FramePanel
frmPanel = Frame(frameParent)
frmPanel.pack(fill=X)
lblPanel = Label(frmPanel, text="Mã panel", width=15)
lblPanel.pack(side=LEFT, padx=5, pady=5)
cmbPanel = Combobox(frmPanel, state="readonly", values=G_PANEL_LIST)
cmbPanel.pack(fill=X, padx=5, expand=True)
cmbPanel.current(int(G_PANEL_DEFAULT))
cmbPanel.bind("<<ComboboxSelected>>", UpdateGlobalVariable)
#endregion
#region FormMain/FrameParent/FrameBrand
frmBrand = Frame(frameParent)
frmBrand.pack(fill=X)
lblBrand = Label(frmBrand, text="Thương hiệu", width=15)
lblBrand.pack(side=LEFT, padx=5, pady=5)
cmbBrand = Combobox(frmBrand, state="readonly", values=G_BRAND_LIST)
cmbBrand.pack(fill=X, padx=5, expand=True)
cmbBrand.current(int(G_BRAND_DEFAULT))
cmbBrand.bind("<<ComboboxSelected>>", UpdateGlobalVariable)
#endregion
#region FormMain/FrameParent/FrameLauncher
frmLauncher = Frame(frameParent)
frmLauncher.pack(fill=X)
lblLauncher = Label(frmLauncher, text="Giao diện", width=15)
lblLauncher.pack(side=LEFT, padx=5, pady=5)
cmbLauncher = Combobox(frmLauncher, state="readonly", values=G_LAUNCHER_LIST)
cmbLauncher.pack(fill=X, padx=5, expand=True)
cmbLauncher.current(int(G_LAUNCHER_DEFAULT))
cmbLauncher.bind("<<ComboboxSelected>>", UpdateGlobalVariable)
#endregion
#region FormMain/FrameParent/FrameVoice
frmVoice = Frame(frameParent)
frmVoice.pack(fill=X)
lblVoice = Label(frmVoice, text="Giọng nói", width=15)
lblVoice.pack(side=LEFT, padx=5, pady=5)
cmbVoice = Combobox(frmVoice, state="readonly", values=G_VOICE_LIST)
cmbVoice.pack(fill=X, padx=5, expand=True)
cmbVoice.current(int(G_VOICE_DEFAULT))
cmbVoice.bind("<<ComboboxSelected>>", UpdateGlobalVariable)
#endregion
#region FormMain/FrameParent/FrameRemote
frmRemote = Frame(frameParent)
frmRemote.pack(fill=X)
lblRemote = Label(frmRemote, text="Remote", width=15)
lblRemote.pack(side=LEFT, padx=5, pady=5)
cmbRemote = Combobox(frmRemote, state="readonly", values=G_REMOTE_LIST)
cmbRemote.pack(fill=X, padx=5, expand=True)
cmbRemote.current(int(G_REMOTE_DEFAULT))
cmbRemote.bind("<<ComboboxSelected>>", UpdateGlobalVariable)
#endregion
#region FormMain/FrameParent/FrameKeyboard
frmKeyboard = Frame(frameParent)
frmKeyboard.pack(fill=X)
lblKeyboard = Label(frmKeyboard, text="Keyboard", width=15)
lblKeyboard.pack(side=LEFT, padx=5, pady=5)
cmbKeyboard = Combobox(frmKeyboard, state="readonly", values=G_KEYBOARD_LIST)
cmbKeyboard.pack(fill=X, padx=5, expand=True)
cmbKeyboard.current(int(G_KEYBOARD_DEFAULT))
cmbKeyboard.bind("<<ComboboxSelected>>", UpdateGlobalVariable)
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
btnAddBin = Button(app, text="Chọn BIN mới", command=mnuAddNewBin_Click)
btnAddBin.pack(side=LEFT, padx=3, pady=3)
#endregion
##############################################
#region FormOption
opt = Toplevel()
opt.geometry("650x400+606+200")

opt.style = Style()
opt.style.theme_use("winnative")
opt.resizable(0,0)
opt.iconbitmap("resource/icon/app.ico")
opt.withdraw()
opt.protocol("WM_DELETE_WINDOW", btnOptExit_Click)
#endregion
#region FormOption/FrameParent
optFrameParent = Frame(opt, relief=FLAT, borderwidth=1)
optFrameParent.pack(fill=BOTH, expand=True, padx=3, pady=3)
tabOpt = Notebook(optFrameParent)
tabOpt.pack(expand=1, fill="both")
#endregion
#region FormOption/FrameParent/Listbox/system-apk
tabSystemApp = Frame(tabOpt, relief=FLAT, borderwidth=1)
tabOpt.add(tabSystemApp, text="system-app")
frmOptSystem = Frame(tabSystemApp, relief=FLAT)
frmOptSystem.pack(fill=X)
btnOptSystemAppRemove = Button(frmOptSystem, text="Xóa", command=btnOptItemRemove_Click)
btnOptSystemAppRemove.pack(side=RIGHT, padx=3, pady=3)
btnOptSystemAppAdd = Button(frmOptSystem, text="Thêm", command=btnOptItemAdd_Click)
btnOptSystemAppAdd.pack(side=RIGHT, pady=3)
btnOptSystemAppUpdate = Button(frmOptSystem, text="Sync", image=icon_sync, command=btnOptItemUpdate_Click)
btnOptSystemAppUpdate.pack(side=LEFT, padx=3, pady=3)
btnOptSystemAppFolder = Button(frmOptSystem, text="Folder", image=icon_folder, command=btnOptItemFolder_Click)
btnOptSystemAppFolder.pack(side=LEFT, pady=3)

listboxOptSystemApp = Listbox(tabSystemApp, selectmode=EXTENDED, activestyle="none")
listboxOptSystemApp.pack(fill=BOTH, expand=True, padx=3, pady=3)
scrollbarOptSystemApp = Scrollbar(listboxOptSystemApp, orient="vertical")
scrollbarOptSystemApp.pack(side=RIGHT, fill=Y)
listboxOptSystemApp.config(yscrollcommand=scrollbarOptSystemApp.set)
scrollbarOptSystemApp.config(command=listboxOptSystemApp.yview)
#endregion
#region FormOption/FrameParent/Listbox/priv-apk
tabPrivApp = Frame(tabOpt, relief=FLAT, borderwidth=1)
tabOpt.add(tabPrivApp, text='priv-app')
frmOptPriv = Frame(tabPrivApp, relief=FLAT)
frmOptPriv.pack(fill=X)
btnOptPrivAppRemove = Button(frmOptPriv, text="Xóa", command=btnOptItemRemove_Click)
btnOptPrivAppRemove.pack(side=RIGHT, padx=3, pady=3)
btnOptPrivAppAdd = Button(frmOptPriv, text="Thêm", command=btnOptItemAdd_Click)
btnOptPrivAppAdd.pack(side=RIGHT, pady=3)
btnOptPrivAppUpdate = Button(frmOptPriv, text="Sync", image=icon_sync, command=btnOptItemUpdate_Click)
btnOptPrivAppUpdate.pack(side=LEFT, padx=3, pady=3)
btnOptPrivAppFolder = Button(frmOptPriv, text="Folder", image=icon_folder, command=btnOptItemFolder_Click)
btnOptPrivAppFolder.pack(side=LEFT, pady=3)

listboxOptPrivApp = Listbox(tabPrivApp, selectmode=EXTENDED, activestyle="none")
listboxOptPrivApp.pack(fill=BOTH, expand=True, padx=3, pady=3)
scrollbarOptPrivApp = Scrollbar(listboxOptPrivApp, orient="vertical")
scrollbarOptPrivApp.pack(side=RIGHT, fill=Y)
listboxOptPrivApp.config(yscrollcommand=scrollbarOptPrivApp.set)
scrollbarOptPrivApp.config(command=listboxOptPrivApp.yview)
#endregion
#region FormOption/FrameParent/Listbox/user-apk
tabUserApp = Frame(tabOpt, relief=FLAT, borderwidth=1)
tabOpt.add(tabUserApp, text='user-app')
frmOptUser = Frame(tabUserApp, relief=FLAT)
frmOptUser.pack(fill=X)
btnOptUserAppRemove = Button(frmOptUser, text="Xóa", command=btnOptItemRemove_Click)
btnOptUserAppRemove.pack(side=RIGHT, padx=3, pady=3)
btnOptUserAppAdd = Button(frmOptUser, text="Thêm", command=btnOptItemAdd_Click)
btnOptUserAppAdd.pack(side=RIGHT, pady=3)
btnOptUserAppUpdate = Button(frmOptUser, text="Sync", image=icon_sync, command=btnOptItemUpdate_Click)
btnOptUserAppUpdate.pack(side=LEFT, padx=3, pady=3)
btnOptUserAppFolder = Button(frmOptUser, text="Folder", image=icon_folder, command=btnOptItemFolder_Click)
btnOptUserAppFolder.pack(side=LEFT, pady=3)

listboxOptUserApp = Listbox(tabUserApp, selectmode=EXTENDED, activestyle="none")
listboxOptUserApp.pack(fill=BOTH, expand=True, padx=3, pady=3)
scrollbarOptUserApp = Scrollbar(listboxOptUserApp, orient="vertical")
scrollbarOptUserApp.pack(side=RIGHT, fill=Y)
listboxOptUserApp.config(yscrollcommand=scrollbarOptUserApp.set)
scrollbarOptUserApp.config(command=listboxOptUserApp.yview)
#endregion
#region FormOption/FrameParent/Listbox/BIN
tabBinFile = Frame(tabOpt, relief=FLAT, borderwidth=1)
tabOpt.add(tabBinFile, text='BIN')
frmOptUser = Frame(tabBinFile, relief=FLAT)
frmOptUser.pack(fill=X)
btnOptBinFileRemove = Button(frmOptUser, text="Xóa", command=btnOptItemRemove_Click)
btnOptBinFileRemove.pack(side=RIGHT, padx=3, pady=3)
btnOptBinFileAdd = Button(frmOptUser, text="Chép USB", command=btnOptBinFileCopyUSB_Click)
btnOptBinFileAdd.pack(side=RIGHT, pady=3)
btnOptBinFileUpdate = Button(frmOptUser, text="Sync", image=icon_sync, command=btnOptItemUpdate_Click)
btnOptBinFileUpdate.pack(side=LEFT, padx=3, pady=3)
btnOptBinFileFolder = Button(frmOptUser, text="Folder", image=icon_folder, command=btnOptItemFolder_Click)
btnOptBinFileFolder.pack(side=LEFT, pady=3)

listboxOptBinFile = Listbox(tabBinFile, selectmode=SINGLE, activestyle="none")
listboxOptBinFile.pack(fill=BOTH, expand=True, padx=3, pady=3)
scrollbarOptBinFile = Scrollbar(listboxOptBinFile, orient="vertical")
scrollbarOptBinFile.pack(side=RIGHT, fill=Y)
listboxOptBinFile.config(yscrollcommand=scrollbarOptBinFile.set)
scrollbarOptBinFile.config(command=listboxOptBinFile.yview)
#endregion

#region FormOption/Note
optFrameNote = LabelFrame(opt, text="Ghi chú")
optFrameNote.pack(fill=BOTH, expand=True, padx=3, pady=3)

textBoxNote = Text(optFrameNote)
textBoxNote.pack(fill=BOTH, expand=True, padx=3, pady=3)
scrollbarNote = Scrollbar(textBoxNote, orient="vertical")
scrollbarNote.pack(side=RIGHT, fill=Y)
textBoxNote.config(yscrollcommand=scrollbarNote.set)
scrollbarNote.config(command=textBoxNote.yview)

#endregion

#region FormOption/FrameParent/Buttons
btnOptBuild = Button(opt, text="Thực hiện", command=btnOptBuild_Click)
btnOptBuild.pack(side=RIGHT, padx=3, pady=3)
btnOptCopyDefaultApk = Button(opt, text="Chép lại APK", command=btnOptCopyDefaultApk_Click)
btnOptCopyDefaultApk.pack(side=LEFT, padx=3, pady=3)

lblVersion = Label(opt, text="Phiên bản ")
lblVersion.pack(side=LEFT, padx=15, pady=3)
strVernum = StringVar()
strVernum.set(G_VERNUM_DEFAULT)
entVersion = Entry(opt, textvariable=strVernum, width=15)
entVersion.pack(side=LEFT, padx=3, pady=3)
entVersion.bind("<KeyRelease>", UpdateGlobalVariable)

#endregion
##############################################
#region FormMain/MenuBar
menubar = Menu(app)
filemenu = Menu(menubar, tearoff = 0)
filemenu.add_command(label = "Exit", command = appExit_Click)
menubar.add_cascade(label = "File", menu = filemenu)

editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label = "Animation config", command = mnuOpenAnimationCfg_Click)
editmenu.add_command(label = "Pack config", command = mnuOpenPackCfg_Click)
editmenu.add_command(label = "Modify build.prop", command = mnuOpenBuildprop_Click)
editmenu.add_separator()
editmenu.add_command(label = "Software folder", command = mnuOpenBinFolder_Click)
editmenu.add_command(label = "Working folder", command = mnuOpenWorkingFolder_Click)
editmenu.add_command(label = "Android folder", command = mnuOpenAndroidFolder_Click)
editmenu.add_separator()
editmenu.add_command(label = "Modify system config file", command = mnuOpenAppCfg_Click)
menubar.add_cascade(label = "Edit", menu = editmenu)

# resmenu = Menu(menubar, tearoff = 0)
# resmenu.add_command(label = "TV software", command = mnuOpenOutForm_Click)
# resmenu.add_command(label = "Android System", command = mnuOpenResForm_Click)
# menubar.add_cascade(label = "Resource", menu = resmenu)

#endregion
##############################################
UpdateGlobalVariable(app)
opt.config(menu = menubar)
app.config(menu = menubar)
app.mainloop()
