class Parser:
    def __init__(self, args):
        self.args = args
        
    def run(self):
        if len(self.args) <= 0:
            print("No arguments provided.")
            return
            
        print(self.args)