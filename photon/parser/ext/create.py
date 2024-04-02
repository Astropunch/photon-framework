#used to create new photon projects

from ...ext.object import Obj
from ...ext.templates import IndexTemplate, ScriptTemplate, DefaultVariables
import os

import json

Dirs = [
    "src",
    "src/route",
    "src/lib",
    "temp",
]

Files = [
    Obj(
        path = "photon.json",
        content = json.dumps({"name": "Photon Project", "version": "0.0.1", "author": "Unknown"}, indent=4),
        required = True 
    ),
    Obj(
        path = "vars.json",
        content = json.dumps(DefaultVariables, indent=4),
        required = True
    ),
    Obj(
        path = "src/route/index.pml",
        content = IndexTemplate,
        required = False
    ),
    Obj(
        path = "src/lib/script.py",
        content = ScriptTemplate,
        required = False
    )
]

def entry(name):
    print(f"Photon CREATE")
    
    if os.path.exists(name):
        print(f"Error: Project '{name}' already exists.")
        return
    
    os.makedirs(name)
    
    for d in Dirs:
        print(f"TASK: Create {d}")
        os.makedirs(f"{name}/{d}")
    
    for f in Files:
        print(f"TASK: Write {f.path}")
        with open(f"{name}/{f.path}", "w") as file:
            file.write(f.content)
            
    print("Project created, get started by running")
    print(f" cd {name}")
    print(" python -m photon run")