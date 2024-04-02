from .create import Files, Dirs
from ...pml import translate
from ...ext.object import Obj

import os
import zipfile
import requests

package_url = "https://github.com/Astropunch/photon-framework/releases/download/Package/package.zip"

def entry(path=None):
    if path:
        os.chdir(path)
        
    package_import = str(input(f"Would you like to import the photon package? (y/n) [n]: "))
    if package_import.lower() == "y":
        download_package()
    
    for d in Dirs:
        if not os.path.exists(d):
            print(f"Error: Project structure is not valid, missing '{d}' directory.")
            return
        
    for f in Files:
        if not os.path.exists(f.path) and f.required:
            print(f"Error: Project structure is not valid, missing '{f.path}' file.")
            return
        
    pml = translate_pml(path if path else ".")
    print(pml)
    
def translate_pml(path):
    out = []
    
    tr = translate.Translater()
    for root, dirs, files in os.walk("src"):
        for file in files:
            if file.endswith(".pml"):
                print(f"TASK: Parsing {root}\\{file}")
                with open(f"{root}/{file}", "r") as pml:
                    data = tr.convert(pml.read(), file)
                    out.append(data)
                    
    return out

def download_package():
    try:
        os.remove("photonui")
    except: pass
    else: print("TASK: Removed existing PhotonUI directory")
    
    os.makedirs("photonui", exist_ok=True)
    
    print(f"TASK: Downloading package from {package_url}")
    package = requests.get(package_url)
    with open("photonui/package.zip", "wb") as file:
        file.write(package.content)
        
    print("TASK: Extracting package")
    with zipfile.ZipFile("photonui/package.zip", "r") as zip_ref:
        zip_ref.extractall("photonui")
        
    os.remove("photonui/package.zip")
    print("TASK: Package imported")    