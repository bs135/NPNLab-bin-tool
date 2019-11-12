import os
import time
import sys
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
import bhelper
import cpfile
import datetime

if len(sys.argv) <= 4: 
	print ("Usage: auto.py")
	quit()

#P75338V621G_LSC320AN10_ANDROID_UXCN
#P75338V621G_HV430FHBN10_SANCO_UXCN_N_PRE05_UBC_213B_20191028_150300
#1           2           3     4    5 6     7   8
BOARD=sys.argv[1]
PANEL=sys.argv[2]
BRAND=sys.argv[3]
LAUNCHER=sys.argv[4]
VOICE=sys.argv[5]
REMOTE=sys.argv[6]
KEYBOARD=sys.argv[7]
VERSION=sys.argv[8]

MDIR = os.path.dirname(os.path.abspath(__file__))

print("[i] BOARD="+BOARD)       #CV358HB42
print("[i] PANEL="+PANEL)       #LSC320AN10
print("[i] BRAND="+BRAND)       #UBC
print("[i] LAUNCHER="+LAUNCHER) #UXBH
print("[i] VOICE="+VOICE)       #V
print("[i] REMOTE="+REMOTE)     #PRE05
print("[i] KEYBOARD="+KEYBOARD) #UBC
print("[i] VERSION="+VERSION)   #500

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
    return _mdir

def runCmd(cmd):
    cmd = mdir(cmd)
    print(">>> " + cmd)
    os.system(cmd)

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
    bhelper.delete_path(des_dir)
    bhelper.delete_path(ani_path)
    bhelper.create_dir_if_not_exist(des_dir+"/part0")
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
    bhelper.zip(des_dir, ani_path)

def mod_system():
    print("[i] mod_system()")
    #mount
    runCmd("sudo mount [MDIR]/unpacked/system_ex.img [MDIR]/fs")
    #mod
    runCmd("sudo cp -f [MDIR]/custom/system/usr/keylayout/Generic.kl [MDIR]/fs/usr/keylayout/Generic.kl")
    runCmd("sudo cp -f [MDIR]/custom/system/bin/preinstallapp.sh [MDIR]/fs/bin/preinstallapp.sh")
    runCmd("sudo cp -f [MDIR]/custom/system/build.prop/[BRAND]/build.prop [MDIR]/fs/build.prop")
    
    #runCmd("sudo cp -f [MDIR]/custom/bootanimation/bootanimation.zip [MDIR]/fs/media/bootanimation.zip")
    runCmd("sudo cp -f [MDIR]/custom/bootanimation_V500/[BRAND]/bootanimation.zip [MDIR]/fs/media/bootanimation.zip")
    
    runCmd("sudo rm -rf [MDIR]/fs/preinstall/app")
    runCmd("sudo cp -rf [MDIR]/custom/system/preinstall/app [MDIR]/fs/preinstall")

    #umount
    time.sleep(2)
    runCmd("sudo umount [MDIR]/fs")
    time.sleep(2)
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

    runCmd("sudo cp -f [MDIR]/custom/vendor/build.prop/[BRAND]/build.prop [MDIR]/fs/build.prop")

    runCmd("sudo cp -f [MDIR]/custom/vendor/usr/keylayout/[KEYBOARD]/Vendor_3697_Product_0002.kl [MDIR]/fs/usr/keylayout/Vendor_3697_Product_0002.kl")
    runCmd("sudo cp -rf [MDIR]/custom/launcher/[BRAND]_[LAUNCHER]/NPNLauncher [MDIR]/fs/app")
    runCmd("sudo cp -rf [MDIR]/custom/vendor/app/NPNAppManager [MDIR]/fs/app")

    #umount
    time.sleep(2)
    runCmd("sudo umount [MDIR]/fs")
    time.sleep(2)
    #convert ext
    runCmd("[MDIR]/bin/linux64/img2simg [MDIR]/unpacked/vendor_ex.img [MDIR]/unpacked/vendor.simg")

def mod_tvconfig():
    print("[i] mod_tvconfig()")
    #mount
    runCmd("sudo mount [MDIR]/unpacked/tvconfig.img [MDIR]/fs")
    #mod
    runCmd("sudo cp -f [MDIR]/custom/tvconfig/config/panel/[PANEL]/FullHD_CMO216_H1L01.ini [MDIR]/fs/config/panel/FullHD_CMO216_H1L01.ini")
    runCmd("sudo cp -f [MDIR]/custom/tvconfig/config/model/[PANEL]/Customer_1.ini [MDIR]/fs/config/model/Customer_1.ini")
    #umount
    time.sleep(2)
    runCmd("sudo umount [MDIR]/fs")
    time.sleep(2)

def mod_tvcustomer():
    print("[i] mod_tvcustomer()")
    #mount
    runCmd("sudo mount [MDIR]/unpacked/tvcustomer.img [MDIR]/fs")
    #mod
    runCmd("sudo cp -f [MDIR]/custom/tvcustomer/Customer/build.prop/[BRAND]/ctvbuild.prop [MDIR]/fs/Customer/")
    # runCmd("sudo cp -f [MDIR]/custom/tvcustomer/Customer/[PANEL]/cultraview_projectinfo.sql [MDIR]/fs/Customer/")
    #umount
    time.sleep(2)
    runCmd("sudo umount [MDIR]/fs")
    time.sleep(2)

def cp_output():
    TIME = datetime.datetime.now().strftime(r"%Y%m%d_%H%M%S")
    firmwareDir = "[BOARD]_[PANEL]_[BRAND]_[LAUNCHER]"
    firmware = "[VERSION]_[VOICE]_[REMOTE]_[KEYBOARD]_" + TIME
    
    #runCmd("cp [MDIR]/CtvUpgrade.bin /media/nguyen/KSD/CtvUpgrade.bin")
    runCmd("cp [MDIR]/CtvUpgrade.bin /media/nguyen/BS/CtvUpgrade.bin")
    #runCmd("cp [MDIR]/CtvUpgrade.bin /media/nguyen/KINGSTON/CtvUpgrade.bin")

    runCmd("mkdir -p [MDIR]/output/" + firmwareDir + "/" + firmware)
    runCmd("mv [MDIR]/CtvUpgrade.bin [MDIR]/output/" + firmwareDir + "/" + firmware + "/CtvUpgrade.bin")

#####################
# Build Proccess
#####################
print("[MDIR]: " + MDIR)
#runCmd("sudo -s")

if(not os.path.exists(mdir("[MDIR]/fs/"))):
    runCmd("mkdir [MDIR]/fs")

#make_animation()

unpack()
mod_system()
mod_vendor()
mod_tvconfig()
mod_tvcustomer()
pack()
cp_output()

runCmd("rm -rf [MDIR]/fs")
runCmd("rm -rf [MDIR]/unpacked")

print("DONE!")
