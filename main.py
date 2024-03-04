#getting started with photon

import photon
from photon.keymap import get_key

#Create a Page
class MyPage(photon.Page):
    def __init__(self, app):
        self.app = app
        
        self.pressed_key = 1
        
    def on_render(self, sc):
        sc.addstr(0, 0, f"Pressed Key: {get_key(self.pressed_key)}")
        
    def on_input(self, key):
        self.pressed_key = key
           
#Initialize Photon 
App = photon.Photon()

#Add an event listener
@App.event("on_init")
def on_init():
    App.register_page(MyPage(App))
    App.open("MyPage")
    
#Run the application
App.run()