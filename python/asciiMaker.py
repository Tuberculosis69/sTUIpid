import colorama
from ascii_magic import AsciiArt, Back
from PIL import ImageEnhance
import os
import sys

appid = ""

try:
    appid = sys.argv[1]
except IndexError as e:
    print("(ERR) The appid for the image was not provided for asciiMaker.py")
    
def convertImage(appid):
    file_path = f"images/{appid}.jpg"
    if os.path.exists(file_path):   
        colorama.init() 
        output = AsciiArt.from_image(file_path)
        output.image = ImageEnhance.Color(output.image).enhance(2.0)
        output.image = ImageEnhance.Contrast(output.image).enhance(2.0)
        output.to_terminal(columns=48, back=Back.BLACK)
        
    else:
        print(f"(ERR) The game icon for appid {appid} does not exist.")
        
convertImage(appid)