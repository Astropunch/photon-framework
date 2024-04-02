from ..ext.object import Obj

from .ext import (help, create)

commands = [
    Obj(name="help", description="Show this help message.", func=help, args=[Obj(arg="command", required=False)]),
    Obj(name="create", description="Create a new project.", func=create, args=[Obj(arg="name", required=True)]),
]