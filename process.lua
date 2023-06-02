if window.is_closed()==false then
    key = window.key_pressed()
    text = textbox.get_text()
    x, y = window.wait_for_click()
    if rect.is_touched(x, y) then
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