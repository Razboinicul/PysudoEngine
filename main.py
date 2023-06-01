import GraphicsEngine as ge

def main():
    win = ge.Window("test", 800, 600)
    img = ge.Image(600, 400, "Queen_Crow.png")
    rect = ge.Rect(10, 10, 100, 100)
    oval = ge.Oval(50, 50, 100, 85, "blue")
    circle = ge.Circle(300, 200, 25, "red")
    line = ge.Line(100, 25, 225, 75, "green")
    text = ge.Text(250, 125, "test text", "gray")
    entry = ge.Entry(400, 250, 15, "purple")
    sound = ge.Sound("otherside.mp3")
    sound.play()
    while True:
        #oval.move(1, 1)
        key = win.key_pressed()
        closed = win.is_closed()
        if key == "x":
            print(entry.get_text())
        if key == "w":
            img.move(0, -2.5)
        if key == "a":
            img.move(-2.5, 0)
        if key == "s":
            img.move(0, 2.5)
        if key == "d":
            img.move(2.5, 0)
        if (key == "Escape") or (closed == True): win.destroy()

if __name__ == "__main__":
    main()