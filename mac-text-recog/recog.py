import subprocess
import os
import time
from rumps import *
import pyperclip


basePath = "/".join(os.path.realpath(__file__).split("/")[0:-1])+"/"
#timeStamp = lambda: str(int(round(time.time() * 1000)))



class CaptureApp(rumps.App):
    justClose = 0
    copyToClipboard = 1

    name = "Capture Text"
    indicatorIcon = basePath + "icon.png"

    def __init__(self):
        #super(AwesomeStatusBarApp, self).__init__("Awesome App")
        super(CaptureApp, self).__init__(self.name)
        self.menu = ["Capture"]
        self.icon = self.indicatorIcon
        rumps.debug_mode(False)

    @clicked('Capture')
    def button(self, sender):
        imagePath = getScreenSelection()
        text = getText(imagePath)
        if(text):
            #Window(text).run()
            window = Window(message='', title=self.name, default_text=text, ok="Copy to clipboard", cancel="close")
            window.icon = self.indicatorIcon
            response = window.run()
            if response.clicked == CaptureApp.copyToClipboard:
                addToClipboard(response.text)


    # @clicked('About')
    # def button(self, sender):
    #     #show the about page



def getScreenSelection():
    #outfile = basePath + timeStamp() + ".jpg"
    outfile = basePath + "screenshot.jpg"
    osExec("screencapture -i " + outfile)
    return outfile

def getText(picture):
    command = basePath + "tesseract " + picture + " stdout 2>/dev/null"
    output, err = osExec(command)

    return output.strip().decode('utf-8')

def addToClipboard(text):
    pyperclip.copy(text)



def osExec(command):
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    return proc.communicate()




if __name__ == '__main__':
    CaptureApp().run()