function _ready ()
    circle = engine.Circle(100, 100, 10)
    rect = engine.Rect(200, 120, 345, 300, "blue")
    textbox = engine.Entry(250, 250, 5)
    button = engine.Button(500, 400, 550, 450, "red", "Exit")
    image = engine.Image(600, 400, "Queen_Crow.png")
    oval = engine.Oval(50, 50, 100, 85, "blue")
    line = engine.Line(100, 25, 225, 75, "green")
    text = engine.Text(250, 125, "test text", "gray")
    sound = engine.Sound("sound.wav")
    sound.play()
end

function _process ()
    key = window.key_pressed()
    text = textbox.get_text()
    x, y = window.get_click()
    if button.is_touched(x, y) then
        window.destroy()
    end
    if key == "w" then
        image.move(0, 2.5)
    end
    if key == "s" then
        image.move(0, -2.5)
    end
    if key == "a" then
        image.move(-2.5, 0)
    end
    if key == "d" then
        image.move(2.5, 0)
    end
    if key == "Return" then
        print(text)
    end
end