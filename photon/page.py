class Page:
    def __init__(self, app):
        self.app = app
    
    def on_render(self, sc):
        sc.addstr(0, 0, "Hello, world!")
        
    def on_input(self, key):
        print(f"Key pressed: {key}")
        