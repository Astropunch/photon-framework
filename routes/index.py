import photon
import os
import curses

from photon.components import Modal, Input
from photon.core import theme
from photon.theme import Variants

from . import about

class Index(photon.Page):
    def __init__(self, app):
        self.app = app
        self.__key__ = None
        
        self.input_box = Input(self.app, "Input", auto_render = False)
        self.show_modal = False
        self.modal_value = ""
    
        self.input_box.on_finish(self.on_input_box_finish)
    
    def on_render(self, sc):
        sc.addstr(0, 0, "Hello, world!")
        sc.addstr(2, 0, f"Screen dimensions: {self.app.screenX}x{self.app.screenY}")
        sc.addstr(3, 0, f"Press any key: {self.__key__} | {chr(self.__key__)}")
        sc.addstr(5, 0, "Press 'enter' to go to the about page.", curses.color_pair(theme.PRIMARY))
        
        if self.show_modal:
            Modal(self.app, "Modal", self.modal_value)
        else:
            self.input_box.on_render(sc)
        
    def on_input(self, key):
        self.__key__ = key
        
        if not self.show_modal:
            self.input_box.on_input(key)
        
    def on_input_box_finish(self, value):
        self.show_modal = True
        self.modal_value = value