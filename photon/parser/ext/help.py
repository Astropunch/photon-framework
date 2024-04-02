#display help for commands

from .. import commands

def entry(command=None):
    if not command:
        print("Available Commands  |  [] - Optional, <> - Required\n")
        for command in commands.commands:
            args = " ".join([f"<{arg.arg}>" if arg.required else f"[{arg.arg}]" for arg in command.args])
            print(f"  {command.name} {args} - {command.description}")
        return
    
    else:
        for cmd in commands.commands:
            if cmd.name == command:
                print(f"Showing help for command '{command}'\n\n> {cmd.description}")
                print(f"Usage: photon {cmd.name} {' '.join([f'<{arg.arg}>' if arg.required else f'[{arg.arg}]' for arg in cmd.args])}")
                return
            
        print(f"Error: Command '{command}' not found, use 'photon help' for command overview.")