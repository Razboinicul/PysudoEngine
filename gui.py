import tkinter as tk
root = None
def scene_init():
    global b
    b = tk.Button(root, text="Scene", command=lambda: root.destroy())

def show_scene():
    global b
    b.grid(row=1, column=0)

def hide_scene():
    global b
    b.grid_forget()

def main():
    global root
    root = tk.Tk()
    root.title("GraphicsEngine UI")
    v = tk.StringVar(root, "1")
    values = {"Scene" : "1",
              "Script" : "2"}
    i=1
    for (text, value) in values.items():
        tk.Radiobutton(root, text = text, variable = v,
                    value = value, indicator = 0,
                    background = "light blue").grid(row=0, column=i)
        i+=1
    scene_init()
    try:
        while root.state() == 'normal':
            if v.get() == '1':
                show_scene()
            else:
                hide_scene()
            root.update()
    except Exception as e: print(e)

if __name__ == "__main__":
    main()