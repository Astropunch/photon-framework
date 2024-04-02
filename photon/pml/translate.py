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
        
        self.elements = {
            "p": f'Text("$text", auto_render=False, x=$x, y=$y, reverse=$reverse, variant=Variants.DEFAULT)',
            "h1": f'Text("$text", auto_render=False, x=$x, y=$y, reverse=$reverse, variant=Variants.PRIMARY)',
            "h2": f'Text("$text", auto_render=False, x=$x, y=$y, reverse=$reverse, variant=Variants.PRIMARY)',
            "h3": f'Text("$text", auto_render=False, x=$x, y=$y, reverse=$reverse, variant=Variants.PRIMARY)',
        }
        
    def params(self, string):
        for key in self.variables:
            string = string.replace(f"${key}", self.variables[key])
        
    def convert(self, src, path):
        _id = "".join(random.choice(string.ascii_letters + string.digits) for _ in range(24))
        
        output_head = []
        output_body = []
        dependencies = []
        
        #parse pml (photon markup language)
        soup = bs4.BeautifulSoup(src, "html.parser")
        pml = soup.find("pml")
        
        if not pml:
            print(f"WARNING: skipping unsupported file {path}")
            return
        
        #parse pml head and body
        head = pml.find("head")
        body = pml.find("body")
        
        if not body:
            print(f"WARNING: skipping unsupported file {path}")
            return
        
        output_head += f"""
class Page{_id}(Page):
    def __init__(self, app):
        self.app = app
        """.splitlines()
        
        output_body += f"""
    def on_render(self, sc):
        """.splitlines()
        
        #parse body elements
        for element in body.find_all():
            if self.elements.get(element.name):
                data = self.parse_element(element)
                output_body.append(data.body)
                output_head.append(data.head)
            else:
                print(f"WARNING: skipping unsupported element <{element.name}/> in {path}")
                                
        return Obj(
            pageId = _id,
            dependencies = dependencies,
            output = output_head + output_body
        )
        
    def parse_element(el):
        return Obj(
            body = "",
            head = "    pass"
        )