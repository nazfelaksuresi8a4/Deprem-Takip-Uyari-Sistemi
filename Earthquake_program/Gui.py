from PyQt5.QtCore import*
from PyQt5.QtWidgets import* 
from PyQt5.QtGui import*
import sys

class LoadGui(QMainWindow):
    def __init__(self):
        super().__init__()

sp = QApplication(sys.argv)
sw = LoadGui()

def ShowWindow():
    sw.show()

    
