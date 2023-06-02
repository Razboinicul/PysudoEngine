import GraphicsEngine
from lupa import LuaRuntime
filepath = "process.lua"
lua = LuaRuntime(unpack_returned_tuples=True)

def ready():
    f = open("ready.lua", "r+")
    read = f.readlines()
    f.close()
    text = """"""
    for line in read:
        text += line+"\n"
    lua.execute(text)

def run_process():
    global filepath, lua, g
    f = open(filepath, "r+")
    read = f.readlines()
    f.close()
    text = """"""
    for line in read:
        text += line+"\n"
    while True:
        if g.window.is_closed():
            break
        lua.execute(text)

g = lua.globals()
g.engine = GraphicsEngine
g.window = GraphicsEngine.Window("GraphicsEngine", 800, 600)
ready()
run_process()