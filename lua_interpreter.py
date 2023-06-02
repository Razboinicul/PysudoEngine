import GraphicsEngine
import sys
from lupa import LuaRuntime
filepath = "lua_example.lua"
lua = LuaRuntime(unpack_returned_tuples=True)

def run_process():
    global filepath, lua, g, text
    while True:
        if g.window.is_closed():
            sys.exit()
        else:
            lua.execute("_process()")

g = lua.globals()
g.engine = GraphicsEngine
g.window = GraphicsEngine.Window("GraphicsEngine", 800, 600)
f = open(filepath, "r+")
read = f.readlines()
f.close()
text = """"""
for line in read:
    text += line+"\n"
lua.execute(text)
lua.execute("_ready()")
run_process()