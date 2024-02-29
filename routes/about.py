import photon

class About(photon.Page):
    def __init__(self, app):
        self.app = app
    
    def on_render(self, sc):
        sc.addstr(0, 0, "This is the about page.")
        
    def on_input(self, key):
        self.app.open("Index")