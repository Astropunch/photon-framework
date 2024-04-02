from . import commands

class Parser:
    def __init__(self, args):
        self.args = args
        
    def run(self):
        if len(self.args) <= 0:
            print("No arguments provided, use 'photon help' for command overview.")
            return
            
        for command in commands.commands:
            #find command
            if command.name == self.args[0]:
                #check if command has an entry point                    
                if not hasattr(command.func, "entry"):
                    print("Error: Command does not have an entry function.")
                    return
            
                #check if there is not too many arguments
                if len(self.args) - 1 > len(command.args):
                    print(f"Error: Too many arguments, use 'photon help {command.name}' for usage.")
                    return
                
                try:
                    out = command.func.entry(*self.args[1:])
                    if out:
                        print(f"{command.name.upper()}: {out}")
                except Exception as error:
                    print(f"Error: failed to run command '{command.name}'\n>>> {error}")
                    
                return
            
        print(f"Error: Command '{self.args[0]}' not found, use 'photon help' for command overview.")
                    