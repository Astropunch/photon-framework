from ..ext.object import Obj

from .ext import (help, create, build)

commands = [
    Obj(name="help", description="Show this help message.", func=help, args=[Obj(arg="command", required=False)]),
    Obj(name="create", description="Create a new project.", func=create, args=[Obj(arg="name", required=True)]),
    Obj(name="build", description="Build the project.", func=build, args=[Obj(arg="path", required=False)])
]