import pytesseract
import pyautogui
from keyboard import is_pressed
from time import sleep
from screeninfo import get_monitors
import winsound
import os
from getpass import getuser
from PIL import ImageGrab
from functools import partial
ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)

username = getuser()

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)


os.system('cls')

if os.path.exists('C:\\Users\\'+ username +'\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe'):
    pytesseract.pytesseract.tesseract_cmd = 'C:\\Users\\'+ username +'\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe'

elif os.path.exists('C:\\Program Files\\Tesseract-OCR\\tesseract.exe'):
    pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

else:
    print("Error ! Tesseract Not Found !\nhttps://github.com/UB-Mannheim/tesseract/wiki\nInstall Tesseract.")
    exit() 

class Translate:

    def __init__(self):

        topleft = False
        bottomright = False

        while True:
            if is_pressed('-') and topleft == False:
                self.top_left = pyautogui.position()
                topleft = True
            if is_pressed('+') and bottomright == False:
                self.bottom_right = pyautogui.position()
                bottomright = True
            if bottomright == True and topleft == True :
                break
        
        self.xbot = self.bottom_right.x
        self.xtop = self.top_left.x
    
        
    def set_monitor(self,monitor):
        if monitor == 1:
            for m in get_monitors():
                if m.x < 0:
                    left_monitor = m.x * -1
            self.xbot = self.xbot + left_monitor
            self.xtop = self.xtop + left_monitor

    def screenshot(self):
        im = pyautogui.screenshot()
        self.img_res = im.crop((self.xtop, self.top_left.y, self.xbot, self.bottom_right.y))

    def process_image(self):
        
	    return pytesseract.image_to_string(self.img_res, lang="eng")
        

print("Press 0 if you dont have 2nd monitor\n\nPress 0 if the 2nd monitor is on your right\nPress 1 if the 2nd monitor is on your left")
monitor = int(input("\nInput : "))

if monitor == 1 or monitor == 0:

    print("\n\nTop left coordinates with - key\nBottom right coordinates with + key\nJust move your mouse to any coordinate and press it !")
    cv = Translate()
    cv.set_monitor(monitor)
    say=0
    while True:
        os.system('cls')
        if say%8==0 or say%8==4 :
            worker = "-"
        elif say%8==3 or say%8==7:
            worker = "/"
        elif say%8==2 or say%8==6:
            worker = "|"
        elif say%8==1 or say%8==5:
            worker = "\\"
        print("Working {}".format(worker))
        say+=1
        cv.screenshot()
        try:
            sentence=cv.process_image()
        except:
            print("Coordinate setup is not valid !")
            exit()
        sentence = sentence[1:]
        sleep(1)
        if sentence != "" :
            try:
                winsound.PlaySound(dname+'\\sound.wav', winsound.SND_FILENAME)
            except:
                print("Audio file not found !")

else:
    print("Invalid Selection !")
    sleep(2)
    exit()