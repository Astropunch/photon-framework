import re
import bs4
import json
import random
import string

from ..ext.object import Obj

class Translater:
    def __init__(self):
        
        self.variables = json.loads(open(f"vars.json", "r").read())
        self.data = json.loads(open(f"photon.json", "r").read())
        
    def params(self, string):
        for key in self.variables:
            string = string.replace(f"${key}", self.variables[key])
        
    def convert(self, src):
        
        output = []
        dependencies = []
        
        #parse pml (photon markup language)
        soup = bs4.BeautifulSoup(src, "html.parser")
        pml = soup.find("pml")
        
        if not pml:
            raise Exception("Unspecified pml root element")
        
        #parse pml head and body
        head = pml.find("head")
        body = pml.find("body")
        
        if not head or not body:
            raise Exception("Unspecified pml head or body element")
        
        for element in head.find_all():
            if element.name == "attach":
                if element.get('src'):
                    dependencies.append(element.get('src'))
                                
        return Obj(
            pageId = "".join(random.choice(string.ascii_letters + string.digits) for _ in range(24)),
            dependencies = dependencies,
            output = output
        )