#!/usr/bin/python3

import os
import sys
import shutil
import string
import subprocess
import configparser
import re
import winsound
import bhelper
import cpfile
import bdef
import utils
from time import localtime, strftime
from msvcrt import getch
from tkinter import Tk,Toplevel,Menu,Listbox,messagebox,filedialog,StringVar,END,X,Y,LEFT,RIGHT,BOTH,RIDGE,FLAT,BOTTOM,EXTENDED,SINGLE,PhotoImage,Scrollbar,LabelFrame,Text
from tkinter.ttk import Style,Frame,Label,Combobox,Entry,Button,Notebook,Labelframe

G_MSTAR_TOOL_DIR = os.path.dirname(os.path.abspath(__file__))

def DoMakeAnimation(G_BRAND, G_LAUNCHER, G_VOICE, G_VERNUM, ANI_WIDTH, ANI_HEIGHT, ANI_COLOR, ANI_BACK):
    print("[i] Make bootanimation.zip")
    ANI_FPS     = 20
    VERSION     = "{}.{}.{}{}".format(G_BRAND, G_LAUNCHER, G_VOICE, G_VERNUM)
    OUT_DIR     = G_MSTAR_TOOL_DIR + "/custom/bootanimation/" + G_BRAND + "_" + G_LAUNCHER + "/" + G_VOICE + str(G_VERNUM) + "/" + str(ANI_HEIGHT)
    IN_DIR      = G_MSTAR_TOOL_DIR + "/custom/bootanimation_src/" + G_BRAND + "/"
    ver = VERSION
    padx = 20
    pady = 20
    aniOptions = "-t {} -i {} -o {} -w {} -h {} -s {} --color {} --size {} --back {} --padx {} --pady {} -v".format(ver, IN_DIR, OUT_DIR, ANI_WIDTH, ANI_HEIGHT, ANI_FPS, ANI_COLOR, "11", ANI_BACK, padx, pady)
    bhelper.run_tool(G_MSTAR_TOOL_DIR + "/bin/bmc/bmc.exe", [aniOptions])

for vnum in range(500, 510):
    for voice in ["V", "N"]:
        #DoMakeAnimation("UBC",     "UXBH", voice, vnum, 1920, 1080, "blue", "white")
        #DoMakeAnimation("SANCO",   "UXCN", voice, vnum, 1920, 1080, "blue", "white")
        DoMakeAnimation("SANCO",   "UXCN", voice, vnum, 1920, 1080, "white", "#06559e")
        #DoMakeAnimation("KOLIGHT", "UXCN", voice, vnum, 1920, 1080, "white","black")

    # DoMakeAnimation("UBC",     "UXBH", "V", vnum, 1280, 720, "blue", "white")
    # DoMakeAnimation("UBC",     "UXBH", "N", vnum, 1280, 720, "blue", "white")
    # DoMakeAnimation("SANCO",   "UXCN", "V", vnum, 1280, 720, "blue", "white")
    # DoMakeAnimation("SANCO",   "UXCN", "N", vnum, 1280, 720, "blue", "white")
    # DoMakeAnimation("KOLIGHT", "UXCN", "V", vnum, 1280, 720, "white","black")
    # DoMakeAnimation("KOLIGHT", "UXCN", "N", vnum, 1280, 720, "white","black")
