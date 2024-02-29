from ..page import Page
from ..core import theme
from .. import utils

import curses

class Modal(Page):
    def __init__(self, app, title = "", content = ""):
        self.title = title if title else "Modal"
        self.content = content if content else "This is a modal."
        
        if not app.sc:
            raise Exception("App screen is not initialized.")
        
        self.show(app)
    
        
    def show(self, app):
        ###] Modal [################
        # This is a modal.         #
        ############################
        
        screenX = app.screenX
        screenY = app.screenY
        
        #get start of the Y axis
        sizeY = len(self.content.splitlines()) + 2
        y = utils.centerY(app, sizeY)
        
        #get start of the X axis
        maxX = 0
        for ln in self.content.splitlines() + [self.title]:
            maxX = len(ln) if len(ln) > maxX else maxX
        maxX += 4
        
        x = utils.centerX(app, maxX)
        
        #draw the modal
        
        #draw the background
        for i in range(y, y + sizeY):
            app.sc.addstr(i, x, " " * maxX, curses.color_pair(theme.PRIMARY_BG))
        
        #draw the border
        app.sc.addstr(y, x, "#" * maxX, curses.color_pair(theme.PRIMARY_BG)) #top
        app.sc.addstr(y + sizeY - 1, x, "#" * maxX, curses.color_pair(theme.PRIMARY_BG)) #bottom
        for i in range(y, y + sizeY):
            app.sc.addstr(i, x, "#", curses.color_pair(theme.PRIMARY_BG)) #left
            app.sc.addstr(i, x + maxX - 1, "#", curses.color_pair(theme.PRIMARY_BG)) #right
            
        #draw the title
        title = f"] {self.title} ["
        app.sc.addstr(y, utils.centerTextX(app, title), title, curses.color_pair(theme.PRIMARY_BG))
        
        #draw the content
        for i, ln in enumerate(self.content.splitlines()):
            app.sc.addstr(y + 1 + i, utils.centerTextX(app, ln), ln, curses.color_pair(theme.PRIMARY_BG))
        
        
        
        
        
