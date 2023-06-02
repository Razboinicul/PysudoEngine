function _ready ()
    circle = engine.Circle(100, 100, 10)
    rect = engine.Rect(200, 120, 345, 300, "blue")
    textbox = engine.Entry(250, 250, 5)
    button = engine.Button(500, 400, 550, 450, "red", "Exit")
end

function _process ()
    key = window.key_pressed()
    text = textbox.get_text()
    x, y = window.wait_for_click()
    if button.is_touched(x, y) then
        window.destroy()
    end
    if key == "w" then
        circle.move(0, 2.5)
    end
    if key == "s" then
        circle.move(0, -2.5)
    end
    if key == "a" then
        circle.move(-2.5, 0)
    end
    if key == "d" then
        circle.move(2.5, 0)
    end
    if key == "Return" then
        print(text)
    end
end