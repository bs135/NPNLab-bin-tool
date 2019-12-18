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

MDIR = os.path.dirname(os.path.abspath(__file__))
BOARD = "CV358HB42"
VERSION="504"
for PANEL in ["LSC320AN10","LC390TA2A","V400HJ6PE1","V400HJ6PE1EK","HV430FHBN10"]:
    for BRAND in ["UBC","SANCO","KOLIGHT"]:
        for VOICE in ["V","N"]:
            LAUNCHER="UXCN"
            REMOTE="PRE05"
            KEYBOARD="UKB"
            if BRAND=="UBC":
                LAUNCHER="UXBH"
            if BRAND=="KOLIGHT":
                REMOTE="PRE03"
            if PANEL in ["V400HJ6PE1","V400HJ6PE1EK","V400HJ6PE1DK"]:
                KEYBOARD="CVT"
            if BRAND=="KOLIGHT" and VOICE=="N":
                continue
            if PANEL=="V400HJ6PE1EK" and BRAND != "UBC":
                continue
            FIRMWARE = "{}_{}_{}_{}_{}_{}_{}".format(BOARD,PANEL,BRAND,LAUNCHER,VOICE,REMOTE,KEYBOARD)

            print("[--ALL--] BEGIN " + FIRMWARE)

            # build
            cmd = "python3 [MDIR]/auto.py {} {} {} {} {} {} {} {}".format(BOARD,PANEL,BRAND,LAUNCHER,VOICE,REMOTE,KEYBOARD,VERSION)
            cmd = cmd.replace("[MDIR]", MDIR)
            os.system(cmd)

            # write log
            _LOG_FILE =  "[MDIR]/log_[VERSION].txt".replace("[MDIR]", MDIR).replace("[VERSION]", VERSION)
            if os.path.isfile(_LOG_FILE):
                with open(_LOG_FILE, 'a', encoding="utf-8") as f: 
                    f.writelines(FIRMWARE)
            print("\n[i] Write log completed!")

            print("[--ALL--] END " + FIRMWARE)
