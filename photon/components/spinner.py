from ..page import Page
from ..core import theme
from ..theme import Variants
from .. import utils

import curses
import time

class Spinner(Page):
    def __init__(self, app, x = None, y = None, frames:dict=None, variant:Variants = Variants.DEFAULT, auto_render = True):
        self.app = app
        
        self.x = x
        self.y = y
        
        self.variant = variant
        
        self.frames = frames if frames else {
            0: "⠋",
            1: "⠙",
            2: "⠹",
            3: "⠸",
            4: "⠼",
            5: "⠴",
            6: "⠦",
            7: "⠧",
            8: "⠇",
            9: "⠏",
        }
        
        self.start_time = time.time()
        
        if not auto_render: return
        if not app.sc:
            raise Exception("App screen is not initialized.")
        
        self.on_render(app.sc)
        
    def on_render(self, sc):
        colors = theme.get_colors(self.variant)
        fg = colors[0]
        
        frame = self.frames[int((time.time() - self.start_time) * len(self.frames)) % len(self.frames)]
        
        if self.x == None: self.x = int((self.app.screenX - len(frame)) / 2)
        if self.y == None: self.y = int((self.app.screenY - len(frame.splitlines())) / 2)
        
        for i, line in enumerate(frame.splitlines()):
            sc.addstr(self.y+i, self.x, line, curses.color_pair(fg))