#!/usr/bin/python3

import os
import subprocess
import shutil
import re
from distutils.dir_util import copy_tree
import cpfile
import bdef
import hashlib
from functools import partial
import zipfile

def say_hello():
	print("[i] Hello world!")

def posix_style_dir(dir):
    return dir.replace("\\", "/")

def run_script(script_path, argvs = []):
    if not os.path.exists(script_path):
        print("[!] Error: Can not find '" + script_path + "'")
        quit()
    # os.chdir(os.path.dirname(script_path))
    str_argv = ""
    for arg in argvs:
        str_argv = str_argv + " " + arg
    os.system("py " + script_path + " " + str_argv)
    # os.chdir(WORKING_DIR)

def run_tool(tool_path, argvs = []):
    if not os.path.exists(tool_path):
        print("[!] Error: Can not find '" + tool_path + "'")
        quit()
    str_argv = ""
    for arg in argvs:
        str_argv = str_argv + " " + arg
    subprocess.call(tool_path + " " + str_argv)
	
def first_file(from_dir, ext = ""):
    if not os.path.exists(from_dir):
        print("[!] Error: Can not find '" + from_dir + "'")
        return ""
    if not os.path.isdir(from_dir):
        print("[!] Error: '" + from_dir + "' is not directory.")
        return ""
    if not ext == "":
        for fname in os.listdir(from_dir):
            if os.path.splitext(fname)[1] == ext:
                return fname
    if len(os.listdir(from_dir)) > 0:
        return os.listdir(from_dir)[0]
    print("[!] Error: Can not find any file in '" + from_dir + "'")
    return ""

def delete_path(_path):
    if os.path.exists(_path):
        if os.path.isdir(_path):
            shutil.rmtree(_path, ignore_errors=True)
            print("    Deleted folder: " + _path)
        elif os.path.isfile(_path):
            os.unlink(_path)
            print("    Deleted file: " + _path)

def create_dir_if_not_exist(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

def copy_dir(from_dir, to_dir):
    if os.path.exists(from_dir):
        copy_tree(from_dir, to_dir)

def move_file(from_file, to_file):
    if os.path.exists(from_file) and os.path.exists(os.path.dirname(to_file)):
        shutil.move(from_file, to_file)

def modify_buildprop(buildprop_file, board_name, panel_name):
    if not os.path.exists(buildprop_file):
        return
    rfile = open(buildprop_file, "r") 
    content = rfile.read()
    rfile.close()

    # Android display version
    # TOPTECH 338 KOLIGHT
    if bdef.is_P75338V621G(board_name):
        content = content.replace("4.4.4", "UX 8.1.1")
        content = content.replace("ro.product.model=MStar Android TV", "ro.product.model=Android TV")
        content = content.replace("ro.product.brand=MStar", "ro.product.brand=KOLIGHT")
        content = content.replace("ro.product.manufacturer=MStar Semiconductor, Inc.", "ro.product.manufacturer=KOLIGHT")
        content = content.replace("persist.sys.timezone=Asia/Hanoi", "persist.sys.timezone=Asia/Bangkok")
        content = content.replace("mstar.FAT_paychanel.select=0", "mstar.FAT_paychanel.select=1")
        content = content.replace("ro.build.cus.pro.id=U007_VIETNAM_PANA_FullHD_CMO216_H1L01", "ro.build.cus.pro.id=U007_VIETNAM_KOLIGHT_FullHD_CMO216_H1L01")
        if panel_name in ["ST3151A058","PT320AT011","LSC320AN10"]:
            content = content.replace("ro.sf.lcd_density=240", "ro.sf.lcd_density=160")

    # TOPTECH 638
    if bdef.is_P150638V601G(board_name):
        content = content.replace("ro.sf.lcd_density=320", "ro.sf.lcd_density=240")
        content = content.replace("5.1.1", "UX 8.1.1")
        content = content.replace("ro.product.model=MStar Android TV", "ro.product.model=UBC Android TV")
        content = content.replace("ro.product.brand=MStar", "ro.product.brand=UBC")
        content = content.replace("ro.product.manufacturer=MStar Semiconductor, Inc.", "ro.product.manufacturer=UBCVN")
        content = content.replace("ro.build.cus.pro.id=Vietnam_087B_UD_VB1_8LANE_DualPort1_PANA_A05F", "ro.build.cus.pro.id=Vietnam_087B_UD_VB1_8LANE_DualPort1_UBC_A05F")
        content = content.replace("mstar.FAT.enable=0", "mstar.FAT.enable=1")
        content = content.replace("mstar.FAT_paychanel.select=0", "mstar.FAT_paychanel.select=1")
        
    # CVTE 338
    if bdef.is_TPMSD338PB801(board_name) or bdef.is_TPMSD338PB802(board_name):
        content = content.replace("ro.product.brand=MStar", "ro.product.brand=UBC")
        content = content.replace("ro.product.manufacturer=CVTE", "ro.product.manufacturer=UBCVN")
        content = content.replace("ro.product.model=CVTE_MSD338_1G", "ro.product.model=UBC_MSD338_1G")
        content = content.replace("dalvik.vm.heapstartsize=5m", "dalvik.vm.heapstartsize=8m")
        content = content.replace("dalvik.vm.heapgrowthlimit=48m", "dalvik.vm.heapgrowthlimit=128m")
        content = content.replace("dalvik.vm.heapsize=128m", "dalvik.vm.heapsize=384m")
        content = content.replace("dalvik.vm.heapmaxfree=2m", "dalvik.vm.heapmaxfree=8m")
        content = content.replace("ro.config.low_ram=true", "ro.config.low_ram=false")

    # HL 338
    if bdef.is_HLMS338PC822(board_name):
        #content = content.replace("ro.sf.lcd_density=160", "ro.sf.lcd_density=240")
        content = content.replace("ro.product.manufacturer=CVTE", "ro.product.manufacturer=UBCVN")
        content = content.replace("ro.product.model=HLTV_MSD338_1G", "ro.product.model=UBC_MSD338_1G")
        content = content.replace("dalvik.vm.heapstartsize=5m", "dalvik.vm.heapstartsize=8m")
        content = content.replace("dalvik.vm.heapgrowthlimit=48m", "dalvik.vm.heapgrowthlimit=128m")
        content = content.replace("dalvik.vm.heapsize=128m", "dalvik.vm.heapsize=384m")
        content = content.replace("dalvik.vm.heapmaxfree=2m", "dalvik.vm.heapmaxfree=8m")
        content = content.replace("ro.config.low_ram=true", "ro.config.low_ram=false")

    # CVTE 638
    if bdef.is_TPMS638PC822(board_name):
        content = content.replace("4.4.4", "UX 8.1.1")
        content = content.replace("ro.product.manufacturer=CVTE", "ro.product.manufacturer=UBCVN")
        content = content.replace("ro.product.model=SMART", "ro.product.model=UBC_MSD638_1G")
        content = content.replace("dalvik.vm.heapstartsize=5m", "dalvik.vm.heapstartsize=8m")
        content = content.replace("dalvik.vm.heapgrowthlimit=56m", "dalvik.vm.heapgrowthlimit=96m")
        content = content.replace("dalvik.vm.heapsize=192m", "dalvik.vm.heapsize=256m")
        content = content.replace("dalvik.vm.heapmaxfree=5m", "dalvik.vm.heapmaxfree=8m")

    wfile = open(buildprop_file, "w", newline="\n") 
    wfile.write(content)
    wfile.close()

def clean_buildprop(buildprop_file):
    if not os.path.exists(buildprop_file):
        return

    rfile = open(buildprop_file, "r") 
    content = rfile.read()
    rfile.close()

    content = content.replace("# Made In RK3xxx Firmware Tools by SergioPoverony from 4pda.ru \n", "")
    content = content.replace("# Re-build by NPNLab \n", "")
    content = content + "# Re-build by NPNLab \n"

    wfile = open(buildprop_file, "w", newline="\n") 
    wfile.write(content)
    wfile.close()

def update_config_crc(config_file):
    if not os.path.exists(config_file):
        print("[i] Config file not found!")
        return

    rfile = open(config_file, "r") 
    content = rfile.read()
    rfile.close()

    m = re.search('CEnv_UpgradeCRC_Val +((0x)?[0-9a-fA-F]+)', content, re.MULTILINE)
    if m:
        mstr = m.group(1)
        crctmp = int(mstr, 16)
        crctmp = crctmp + 1
        nstr = hex(crctmp)
        print("[i] CEnv_UpgradeCRC : " + mstr + " -> " + nstr)
        content = content.replace(mstr, nstr)
        wfile = open(config_file, "w", newline="\r\n") 
        wfile.write(content)
        wfile.close()    
    else:
        print("[i] CEnv_UpgradeCRC not found!")

def remove_unuse_char(text):
    return text.replace("-","").replace(".","").replace(" ","_")

def open_path(pth):
    if os.path.exists(pth):
        os.startfile(pth)
        print("[i] Start path: " + pth)
        return True
    else:
        print("[i] Path does not exist: " + pth)
        return False

def copy_resource(src_dir, des_dir, is_in_dir = False):
    if not os.path.exists(src_dir):
        print("[i] Path does not exist: " + src_dir)
        return
    if not os.path.exists(des_dir):
        print("[i] Path does not exist: " + des_dir)
        return
    for dx in os.listdir(src_dir):
        src_file = src_dir + "/" + dx
        if(os.path.isfile(src_file)):
            (base,ext) = os.path.splitext(dx)
            if(re.search(r'apk', ext, re.IGNORECASE)):
                base = remove_unuse_char(base)
            des_file = des_dir + "/" + base + ext
            if is_in_dir:
                des_file = des_dir + "/" + base
                create_dir_if_not_exist(des_file)
                des_file = des_file + "/" + base + ext
            print("    Copy: " + dx)
            cpfile.copy_with_progress(src_file, des_file)
            print("")

def md5sum(filename):
    with open(filename, mode='rb') as f:
        d = hashlib.md5()
        for buf in iter(partial(f.read, 128), b''):
            d.update(buf)
    return d.hexdigest()

def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file), os.path.join(root, file).replace(path,""))

def zip(src, des):
    zipf = zipfile.ZipFile(des, 'w', zipfile.ZIP_STORED)
    zipdir(src, zipf)
    zipf.close()
