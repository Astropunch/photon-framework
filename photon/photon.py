import os
import curses
import threading

from .page import Page

class Photon:
    def __init__(self, screenX:int=120, screenY:int=28, preventExit:bool=False):
        self.screenX = screenX
        self.screenY = screenY
        self.preventExit = preventExit
        
        self.pages = []
        self.page = None
    
    def run(self):
        if threading.current_thread() != threading.main_thread():
            raise Exception("Photon.run() can be only ran from the main thread")
            
        threading.Thread(target=self.listener).start()

        while True: #main thread
            try:
                curses.wrapper(self.renderloop)
            except (KeyboardInterrupt, SystemExit):
                if not self.preventExit:
                    os._exit(0)
            
    #RENDERING -----------------    
        
    def renderloop(self, sc):
        while True:
            sc.erase()
            
            if type(self.page).__base__ == Page:
                self.page.on_render(sc)
            else:
                sc.addstr(0, 0, "RENDER ERROR: page must be an instance of photon.Page")
            
            sc.refresh()
           
    #KEY LISTENERS -----------------
            
    def listener(self):
        curses.wrapper(self.listenerloop)
            
    def listenerloop(self, sc):
        while True:
            key = sc.getch()
            
            if type(self.page).__base__ == Page:
                self.page.on_input(key)
            else:
                raise UserWarning("INPUT ERROR: page must be an instance of photon.Page")
    
    #PAGES -----------------
            
    def register_page(self, page:Page):
        #check for type
        if type(page).__base__ != Page:
            raise TypeError('page must be an instance of photon.Page')

        #check for duplicated pages
        for p in self.pages:
            if p.__class__.__name__ == page.__class__.__name__:
                raise ValueError(f"Page '{page.__class__.__name__}' already registered")

        self.pages.append(page)
        
    def open(self, page_name):
        for page in self.pages:
            if page.__class__.__name__ == page_name:
                self.page = page
                return
            
        raise ValueError(f"Page '{page_name}' not found")

