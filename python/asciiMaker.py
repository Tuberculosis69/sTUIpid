import colorama
from ascii_magic import AsciiArt, Back
from PIL import ImageEnhance
import os
import sys
from GameManager import GameManager

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
        
        # Offset to the right
        char_list = output.to_character_list(columns=48)
        offset = " " * 8
        
        for row in char_list:
            print(offset, end="")
            for char in row:
                print(char['terminal-color'] + char['character'], end="")
            print("\033[0m")  # reset color at end of each line
        
    else:
        print(f"(ERR) The game icon for appid {appid} does not exist.")
        print("(LOG) Attempting to fetch image...")
        try:
            manager = GameManager()
            manager.fix_image(int(appid))
            convertImage(appid)
        except Exception as e:
            print("(ERR) Failed to fetch image from Steam API. Maybe the hash has a problem?")
            print(e)      

convertImage(appid)