import PysudoEngine as ge

def main():
    win = ge.Window("test", 800, 600)
    img = ge.Image(600, 400, "Queen_Crow.png")
    rect = ge.Rect(15, 15, 500, 500)
    rect1 = ge.Rect(15, 15, 25, 25)
    oval = ge.Oval(50, 50, 100, 85, "blue")
    circle = ge.Circle(300, 200, 25, "red")
    line = ge.Line(100, 25, 225, 75, "green")
    text = ge.Text(250, 125, "test text", "gray")
    entry = ge.Entry(400, 250, 15, "purple")
    button = ge.Button(500, 400, 550, 450, "red", "Exit")
    sound = ge.Sound("sound.wav", 75)
    sound.play()
    while True:
        if rect.is_colliding(rect1.x1, rect1.y1, rect1.x2, rect1.y2): print("colliding")
        else: rect1.move(0, 1)
        if not win.is_closed():
            key = win.key_pressed()
            x, y = win.get_click()
            if button.is_touched(x, y):
                for i in ge.objects:
                    i.hide()
                #win.destroy()
            if key == "Return":
                print(entry.get_text())
            if key == "w":
                img.move(0, 2.5)
            if key == "a":
                img.move(-2.5, 0)
            if key == "s":
                img.move(0, -2.5)
            if key == "d":
                img.move(2.5, 0)
            if key == "Escape":
                win.destroy()
        else:
            win.destroy()

if __name__ == "__main__":
    main()