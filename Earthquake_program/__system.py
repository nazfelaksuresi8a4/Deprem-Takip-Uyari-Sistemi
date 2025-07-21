import Gui
from sys import stderr,stdin,stdout
import sys as _s

class exitGuiThread():
    def __init__(self,*args,**kwargs):
        super().__init__()
        _s.exit(Gui.sp.exec_())