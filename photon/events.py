class EventManager:
    def __init__(self):
        self.events = {
            "on_init": None, #called when the app is initialized
            "on_exit": None, #called when the app is exited
            "on_exit_attempt": None, #called when app prevents an exit
            
            "on_render": None, #called every render loop
            "on_input": None, #called on every input
            
        }
        
    def decorate(self, event:str):
        def decorator(func):
            self.events[event] = func
            return func
        return decorator
    
    def call(self, event:str, *args, **kwargs):
        if self.events[event] != None:
            self.events[event](*args, **kwargs)