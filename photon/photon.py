import os
import time
import curses
import threading

from .page import Page
from .events import EventManager
from .theme import Theme, default_theme

from . import core


class Photon:
    def __init__(self, screenX:int=120, screenY:int=28, root:Page=None, maxFps: int = None, preventExit:bool=False, theme:Theme=default_theme):
        """
        Initializes a Photon object.

        Args:
            screenX (int): The width of the screen in characters. Defaults to 120.
            screenY (int): The height of the screen in characters. Defaults to 28.
            root (Page): The root page of the application. Defaults to None.
            maxFps (int): The maximum frames per second. Unlimited by default.
            preventExit (bool): Whether to prevent the application from exiting. Defaults to False.
            theme (Theme): The theme to be used for the application. Defaults to the default theme.
        """
        self.screenX = screenX
        self.screenY = screenY
        self.preventExit = preventExit
        
        self.pages = []
        self.page = None
        self.root = root(self) if root else None
        self.sc = None
        self.fps = 0
        
        self.delay = 1/maxFps if maxFps else 0
        
        self.running = True
        self.em = EventManager()
        
        self.event = self.em.decorate

        if type(theme) != Theme:
            self.em.call("on_error", self, "theme must be an instance of photon.Theme")
            raise TypeError("theme must be an instance of photon.Theme")
        
        core.theme = theme
    
    def run(self):
        if threading.current_thread() != threading.main_thread():
            self.em.call("on_error", self, "Photon.run() can be only ran from the main thread")
            raise Exception("Photon.run() can be only ran from the main thread")
            
        self.listener_thread = threading.Thread(target=self.listener)
        self.listener_thread.start()

        while True: #main thread
            try:
                curses.wrapper(self.renderloop)
            except (KeyboardInterrupt, SystemExit):
                if not self.preventExit:
                    self.exit()
                    os._exit(0)
                    break
                
                self.em.call("on_error", self, "PreventExit is enabled, use Photon.exit() to exit the app.")
                self.em.call("on_exit_attempt")
            
    def exit(self):
        self.em.call("on_exit")
        self.running = False
            
    #RENDERING -----------------    
        
    def renderloop(self, sc):
        self.em.call("on_init")
        self.sc = sc
        
        curses.start_color()
        core.theme.apply()
        
        curses.curs_set(0)
        
        fps_data = {
            "slice": 0,
            "frames": 0,
        }
        
        while self.running:
            #reset screen
            self.em.call("on_render", sc)
            sc.erase()
            
            #render root
            if type(self.root).__base__ == Page:
                self.root.on_render(sc)
            
            #render page
            try:
                if type(self.page).__base__ == Page:
                    self.page.on_render(sc)
                else:
                    self.em.call("on_error", self, "RENDER ERROR: page must be an instance of photon.Page")
                    sc.addstr(0, 0, "RENDER ERROR: page must be an instance of photon.Page")
            except Exception as e:
                self.em.call("on_error", self, f"RENDER ERROR: {e}")
                sc.addstr(0, 0, f"RENDER ERROR: {e}")
            
            #calculate fps
            fps_data["frames"] += 1
            if time.time() - fps_data["slice"] > 1:
                self.fps = fps_data["frames"]
                fps_data["frames"] = 0
                fps_data["slice"] = time.time()
            
            #fps limiter
            if self.delay:
                time.sleep(self.delay)
            
            #update
            sc.refresh()
           
    #KEY LISTENERS -----------------
            
    def listener(self):
        curses.wrapper(self.listenerloop)
            
    def listenerloop(self, sc):
        while self.running:
            key = sc.getch()
            self.em.call("on_input", key)
            
            try:
                if type(self.root) != None:
                    self.root.on_input(key)
            except Exception as e:
                self.em.call("on_error", self, f"INPUT ERROR: (root) {e}")
            
            try:
                if type(self.page).__base__ == Page:
                    self.page.on_input(key)
                else:
                    self.em.call("on_error", self, "INPUT ERROR: page must be an instance of photon.Page")
                    raise UserWarning("INPUT ERROR: page must be an instance of photon.Page")
            except:
                self.em.call("on_error", self, "INPUT ERROR: page must be an instance of photon.Page")
                
    #PAGES -----------------
            
    def register_page(self, page:Page):
        #check for type
        if type(page).__base__ != Page:
            self.em.call("on_error", self, "page must be an instance of photon.Page")
            raise TypeError('page must be an instance of photon.Page')

        #check for duplicated pages
        for p in self.pages:
            if p.__class__.__name__ == page.__class__.__name__:
                self.em.call("on_error", self, f"Page '{page.__class__.__name__}' already registered")
                raise ValueError(f"Page '{page.__class__.__name__}' already registered")

        self.pages.append(page)
        
    def open(self, page_name):
        for page in self.pages:
            if page.__class__.__name__ == page_name:
                self.page = page
                return
        
        self.em.call("on_error", self, f"Page '{page_name}' not found")