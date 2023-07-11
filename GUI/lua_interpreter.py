import PysudoEngine
import sys
from lupa import LuaRuntime
filepath = "lua_example.lua"
lua = LuaRuntime(unpack_returned_tuples=True)
g = lua.globals()

def run_process():
    global filepath, lua, g, text
    while not g.window.is_closed():
        lua.execute("_process()")
    g.window.destroy()

def interpret_code(filepath):
    global g
    g.engine = PysudoEngine
    g.window = PysudoEngine.Window("GraphicsEngine", 800, 600)
    f = open(filepath, "r+")
    read = f.readlines()
    f.close()
    text = """"""
    for line in read:
        text += line+"\n"
    lua.execute(text)
    lua.execute("_ready()")
    run_process()

if __name__ == "__main__": interpret_code()