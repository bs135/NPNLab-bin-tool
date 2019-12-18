import os
import time
import sys
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
import cpfile
import datetime
import re
import zipfile

if len(sys.argv) <= 4: 
	print ("Usage: auto.py")
	quit()

DEBUG_GET_ORIGIN_CUSTOM = False

#P75338V621G_LSC320AN10_ANDROID_UXCN_N_PRE05
#P75338V621G_HV430FHBN10_SANCO_UXCN_N_PRE05_UKB_213B_20191028_150300
#1           2           3     4    5 6     7   8
BOARD=sys.argv[1]
PANEL=sys.argv[2]
BRAND=sys.argv[3]
LAUNCHER=sys.argv[4]
VOICE=sys.argv[5]
REMOTE=sys.argv[6]
KEYBOARD=sys.argv[7]
VERSION=sys.argv[8]

TVSIZE = ""
RESOLUTION = "1080"
if(PANEL == "LSC320AN10"    ):     TVSIZE = "32"
if(PANEL == "LC390TA2A"     ):     TVSIZE = "39"
if(PANEL == "V400HJ6PE1"    ):     TVSIZE = "40"
if(PANEL == "V400HJ6PE1DM"  ):     TVSIZE = "40"
if(PANEL == "V400HJ6PE1EK"  ):     TVSIZE = "40"
if(PANEL == "HV430FHBN10"   ):     TVSIZE = "43"

MDIR = os.path.dirname(os.path.abspath(__file__))

print("[i] BOARD="      +BOARD)     #CV358HB42
print("[i] PANEL="      +PANEL)     #LSC320AN10
print("[i] BRAND="      +BRAND)     #UBC
print("[i] LAUNCHER="   +LAUNCHER)  #UXBH
print("[i] VOICE="      +VOICE)     #V
print("[i] REMOTE="     +REMOTE)    #PRE05
print("[i] KEYBOARD="   +KEYBOARD)  #UKB
print("[i] VERSION="    +VERSION)   #500

print("MDIR="+MDIR)

def mdir(_mdir):
    _mdir = _mdir.replace("[MDIR]", MDIR)
    _mdir = _mdir.replace("[BOARD]", BOARD)
    _mdir = _mdir.replace("[PANEL]", PANEL)
    _mdir = _mdir.replace("[BRAND]", BRAND)
    _mdir = _mdir.replace("[LAUNCHER]", LAUNCHER)
    _mdir = _mdir.replace("[VOICE]", VOICE)
    _mdir = _mdir.replace("[REMOTE]", REMOTE)
    _mdir = _mdir.replace("[KEYBOARD]", KEYBOARD)
    _mdir = _mdir.replace("[VERSION]", VERSION)
    _mdir = _mdir.replace("[TVSIZE]", TVSIZE)
    _mdir = _mdir.replace("[RESOLUTION]", RESOLUTION)
    return _mdir

def runCmd(cmd):
    cmd = mdir(cmd)
    print(">>> " + cmd)
    os.system(cmd)

def delay():
    time.sleep(1)

def remove_unuse_char(text):
    return text.replace("-","").replace(".","").replace(" ","_")

def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        print("[i] zipdir: " + dirs)
        for file in files:
            ziph.write(os.path.join(root, file), os.path.join(root, file).replace(path,""))

def makezip(src, des):
    zipf = zipfile.ZipFile(des, 'w', zipfile.ZIP_STORED)
    zipdir(src, zipf)
    zipf.close()

def unpack():
    print("[i] unpack()")
    runCmd("python3 unpack.py [MDIR]/input/[PANEL]/CtvUpgrade.bin [MDIR]/unpacked/")

def pack():
    print("[i] pack()")
    runCmd("python3 pack.py [MDIR]/configs/cv358-full.ini")

def make_animation():
    print("[i] make_animation()")
    ver = "{}.{}.{}".format(BRAND, LAUNCHER, VERSION)
    src_dir = mdir("[MDIR]/custom/bootanimation/[BRAND]")
    des_dir = mdir("[MDIR]/custom/bootanimation/tmp")
    font_path = mdir("[MDIR]/custom/bootanimation/font/ProductSans-Black.ttf")
    ani_path = mdir("[MDIR]/custom/bootanimation/bootanimation.zip")
    runCmd("rm -rf " + des_dir)
    runCmd("rm -f " + ani_path)
    runCmd("mkdir -p " + des_dir+"/part0")

    for fimg in os.listdir(src_dir):
        print(fimg)
        img = Image.open(src_dir + "/" + fimg)
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(font_path, 16)
        draw.text((10, 10), ver,(0,0,255),font=font)
        img.save(des_dir + "/part0/" + fimg)
    desc_file = open(des_dir+"/desc.txt","w+")
    desc_file.writelines("1280 720 20")
    desc_file.writelines("p 0 0 part0") 
    desc_file.close()
    makezip(des_dir, ani_path)

def mod_system():
    print("[i] mod_system()")
    #mount
    runCmd("sudo mount [MDIR]/unpacked/system_ex.img [MDIR]/fs")
    #mod
    runCmd("sudo cp -f [MDIR]/custom/system/usr/keylayout/[VOICE]_[REMOTE]/Generic.kl [MDIR]/fs/usr/keylayout/Generic.kl")
    runCmd("sudo cp -f [MDIR]/custom/system/bin/[VOICE]/preinstallapp.sh [MDIR]/fs/bin/preinstallapp.sh")
    
    runCmd("sudo cp -f [MDIR]/fs/build.prop [MDIR]/custom/system/build.prop/[BRAND]/build.prop")
    runCmd("sudo cp -f [MDIR]/custom/system/build.prop/[BRAND]/build.prop [MDIR]/fs/build.prop")
    
    #runCmd("sudo cp -f [MDIR]/custom/bootanimation/bootanimation.zip [MDIR]/fs/media/bootanimation.zip")
    #runCmd("sudo cp -f [MDIR]/custom/bootanimation_V500/[BRAND]/bootanimation.zip [MDIR]/fs/media/bootanimation.zip")
    runCmd("sudo cp -f [MDIR]/custom/bootanimation/[BRAND]_[LAUNCHER]/[VOICE][VERSION]/[RESOLUTION]/bootanimation.zip [MDIR]/fs/media/bootanimation.zip")
    
    runCmd("sudo rm -rf [MDIR]/fs/preinstall/app")
    runCmd("sudo cp -rf [MDIR]/custom/system/preinstall/app [MDIR]/fs/preinstall")
    runCmd("sudo cp -f [MDIR]/custom/system/preinstall/app_[BRAND]/* [MDIR]/fs/preinstall/app")

    #umount
    delay()
    runCmd("sudo umount [MDIR]/fs")
    delay()
    #convert ext
    runCmd("[MDIR]/bin/linux64/img2simg [MDIR]/unpacked/system_ex.img [MDIR]/unpacked/system.simg")

def mod_vendor():
    print("[i] mod_vendor()")
    #mount
    runCmd("sudo mount [MDIR]/unpacked/vendor_ex.img [MDIR]/fs")
    #mod
    runCmd("sudo rm -rf [MDIR]/fs/app/Apt/")
    runCmd("sudo rm -rf [MDIR]/fs/app/*STV_Play*")
    runCmd("sudo rm -rf [MDIR]/fs/app/*NPNLauncher*")
    runCmd("sudo rm -rf [MDIR]/fs/app/*Cua_Hang*")
    runCmd("sudo rm -rf [MDIR]/fs/app/*VN_Tube*")
    runCmd("sudo rm -rf [MDIR]/fs/app/*App_Manager*")

    ##################
    #vendor/build.prop
    runCmd("sudo cp -f [MDIR]/fs/build.prop [MDIR]/custom/vendor/build.prop/[BRAND]/build.prop")
    _file_name = mdir("[MDIR]/custom/vendor/build.prop/[BRAND]/build.prop")
    rfile = open(_file_name, "r") 
    content = rfile.read()
    rfile.close()
    content = re.sub('ro.product.board=.*', "ro.product.board=CV6A358_" + PANEL, content, re.M|re.I)
    #content = re.sub('ro.sys.launcher=.*', "ro.sys.launcher="+BRAND+"TV", content, re.M|re.I)
    #content = re.sub('ro.sys.sub_client_os=.*', "ro.sys.sub_client_os="+BRAND+"TV", content, re.M|re.I)
    wfile = open(_file_name, "w", newline="\r\n") 
    wfile.write(content)
    wfile.close()
    runCmd("sudo cp -f [MDIR]/custom/vendor/build.prop/[BRAND]/build.prop [MDIR]/fs/build.prop")
    ##################

    runCmd("sudo cp -f [MDIR]/custom/vendor/usr/keylayout/[KEYBOARD]/Vendor_3697_Product_0002.kl [MDIR]/fs/usr/keylayout/Vendor_3697_Product_0002.kl")
    runCmd("sudo cp -rf [MDIR]/custom/launcher/NPNLauncher [MDIR]/fs/app")
    runCmd("sudo cp -rf [MDIR]/custom/vendor/app/NPNAppManager [MDIR]/fs/app")
    runCmd("sudo cp -rf [MDIR]/custom/vendor/app/RocketClean [MDIR]/fs/app")

    #umount
    delay()
    runCmd("sudo umount [MDIR]/fs")
    delay()
    #convert ext
    runCmd("[MDIR]/bin/linux64/img2simg [MDIR]/unpacked/vendor_ex.img [MDIR]/unpacked/vendor.simg")

def mod_tvconfig():
    print("[i] mod_tvconfig()")
    #mount
    runCmd("sudo mount [MDIR]/unpacked/tvconfig.img [MDIR]/fs")

    if DEBUG_GET_ORIGIN_CUSTOM:
        runCmd("sudo cp -f [MDIR]/fs/config/panel/FullHD_CMO216_H1L01.ini [MDIR]/custom/tvconfig/config/panel/[PANEL]/FullHD_CMO216_H1L01.ini")
        runCmd("sudo cp -f [MDIR]/fs/config/model/Customer_1.ini [MDIR]/custom/tvconfig/config/model/[PANEL]/Customer_1.ini")

    #mod
    runCmd("sudo cp -f [MDIR]/custom/tvconfig/config/panel/[PANEL]/FullHD_CMO216_H1L01.ini [MDIR]/fs/config/panel/FullHD_CMO216_H1L01.ini")
    runCmd("sudo cp -f [MDIR]/custom/tvconfig/config/model/[PANEL]/Customer_1.ini [MDIR]/fs/config/model/Customer_1.ini")
    #umount
    delay()
    runCmd("sudo umount [MDIR]/fs")
    delay()

def mod_tvcustomer():
    print("[i] mod_tvcustomer()")
    #mount
    runCmd("sudo mount [MDIR]/unpacked/tvcustomer.img [MDIR]/fs")
    #mod

    ##################
    #vendor/ctvbuild.prop
    runCmd("sudo cp -f [MDIR]/fs/Customer/ctvbuild.prop [MDIR]/custom/tvcustomer/Customer/build.prop/[BRAND]/ctvbuild.prop")
    _file_name = mdir("[MDIR]/custom/tvcustomer/Customer/build.prop/[BRAND]/ctvbuild.prop")
    rfile = open(_file_name, "r")
    content = rfile.read()
    rfile.close()
    content = re.sub('ro.product.manufacturer=.*', "ro.product.manufacturer="+BRAND, content, re.M|re.I)
    content = re.sub('ro.product.model=.*', "ro.product.model="+"SmartTV"+TVSIZE, content, re.M|re.I)
    wfile = open(_file_name, "w", newline="\r\n")
    wfile.write(content)
    wfile.close()
    runCmd("sudo cp -f [MDIR]/custom/tvcustomer/Customer/build.prop/[BRAND]/ctvbuild.prop [MDIR]/fs/Customer/")
    ##################

    #runCmd("sudo cp -f [MDIR]/custom/tvcustomer/Customer/[PANEL]/cultraview_projectinfo.sql [MDIR]/fs/Customer/")
    #runCmd("sudo cp -f [MDIR]/custom/tvcustomer/Customer/[PANEL]/customer.sql [MDIR]/fs/Customer/")
    #runCmd("sudo cp -f [MDIR]/custom/tvcustomer/Customer/[PANEL]/user_setting.sql [MDIR]/fs/Customer/")
    #runCmd("sudo cp -f [MDIR]/custom/tvcustomer/Customer/[PANEL]/factory_hdmitx.sql [MDIR]/fs/Customer/")
    #runCmd("sudo cp -f [MDIR]/custom/tvcustomer/Customer/[PANEL]/factory.sql [MDIR]/fs/Customer/")
    
    #umount
    delay()
    runCmd("sudo umount [MDIR]/fs")
    delay()

def mod_tvdatabase():
    print("[i] mod_tvdatabase()")
    #mount
    runCmd("sudo mount [MDIR]/unpacked/tvdatabase.img [MDIR]/fs")
    #mod
    runCmd("sudo cp -f [MDIR]/custom/tvdatabase/[PANEL]/Database/user_setting.db [MDIR]/fs/Database/user_setting.db")
    runCmd("sudo cp -f [MDIR]/custom/tvdatabase/[PANEL]/Database/factory.db [MDIR]/fs/Database/factory.db")
    runCmd("sudo cp -f [MDIR]/custom/tvdatabase/[PANEL]/Database/cultraview_projectinfo.db [MDIR]/fs/Database/cultraview_projectinfo.db")    
    
    runCmd("sudo cp -f [MDIR]/custom/tvdatabase/[PANEL]/DatabaseBackup/user_setting.db [MDIR]/fs/DatabaseBackup/user_setting.db")
    runCmd("sudo cp -f [MDIR]/custom/tvdatabase/[PANEL]/DatabaseBackup/factory.db [MDIR]/fs/DatabaseBackup/factory.db")
    runCmd("sudo cp -f [MDIR]/custom/tvdatabase/[PANEL]/DatabaseBackup/cultraview_projectinfo.db [MDIR]/fs/DatabaseBackup/cultraview_projectinfo.db")
    #umount
    delay()
    runCmd("sudo umount [MDIR]/fs")
    delay()

def cp_output():
    TIME = datetime.datetime.now().strftime(r"%Y%m%d_%H%M%S")
    firmwareDir = "[BOARD]_[PANEL]_[BRAND]"
    firmware = "[VERSION]_[VOICE]_[REMOTE]_[KEYBOARD]_" + TIME
    
    ################
    # Copy to USB
    #runCmd("cp [MDIR]/CtvUpgrade.bin /media/nguyen/KSD/CtvUpgrade.bin")
    #runCmd("cp [MDIR]/CtvUpgrade.bin /media/nguyen/BSUSB/CtvUpgrade.bin")
    #runCmd("cp [MDIR]/CtvUpgrade.bin /media/nguyen/KINGSTON/CtvUpgrade.bin")
    ################

    outDir = "[MDIR]/output/" + firmwareDir + "/" + firmware
    runCmd("mkdir -p " + outDir)
    runCmd("mv [MDIR]/CtvUpgrade.bin " + outDir + "/CtvUpgrade.bin")
    #runCmd("nautilus " + outDir)
#####################
# Build Proccess
#####################
print("[MDIR]: " + MDIR)

if(not os.path.exists(mdir("[MDIR]/fs/"))):
    runCmd("mkdir [MDIR]/fs")

#make_animation()

unpack()
mod_system()
mod_vendor()
mod_tvconfig()
mod_tvcustomer()
#mod_tvdatabase()
pack()
cp_output()

runCmd("rm -rf [MDIR]/fs")
runCmd("rm -rf [MDIR]/unpacked")

print("DONE!")
