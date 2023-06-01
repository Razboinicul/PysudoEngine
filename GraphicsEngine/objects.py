import graphics as g
import sys
#Vars
window = None
objects = []

class Window:
    #Window for graphics
    def __init__(self, title, w, h) -> None:
        global window
        self.title = title
        self.w = w
        self.h = h
        #Window variable for access
        self.window = g.GraphWin(title, w, h)
        window = self.window

    def get_window(self):
        return self.window
    
    def is_closed(self):
        return self.window.closed
    
    def wait_for_click(self):
        self.window.getMouse()
        return True
    
    def key_pressed(self):
        press = self.window.checkKey()
        return press
        
    def update(self):
        self.window.flush()
    
    def destroy(self):
        global window
        self.window.close()
        self.window = None
        sys.exit()
        
class Rect:
    def __init__(self, x1, y1, x2, y2, fill=None) -> None:
        global window
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.fill = fill
        self.window = window
        self.rect = g.Rectangle(g.Point(self.x1, self.y1), g.Point(self.x2, self.y2))
        self.rect.setFill(fill)
        self.rect.draw(self.window)
        self.drawn = True
        objects.append(self.rect)
    
    def hide(self):
        if self.drawn:
            self.rect.undraw()
            self.drawn = False
    
    def show(self):
        if not self.drawn:
            self.rect.draw(self.window)
            self.drawn = True

class Oval:
    def __init__(self, x1, y1, x2, y2, fill=None) -> None:
        global window
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.fill = fill
        self.window = window
        self.oval = g.Oval(g.Point(self.x1, self.y1), g.Point(self.x2, self.y2))
        self.oval.setFill(fill)
        self.oval.draw(self.window)
        self.drawn = True
        objects.append(self.oval)
        
    def hide(self):
        if self.drawn:
            self.oval.undraw()
            self.drawn = False
    
    def show(self):
        if not self.drawn:
            self.oval.draw(self.window)
            self.drawn = True
            
    def move(self, dx=0, dy=0):
        self.oval.move(dx, dy)
        
class Circle:
    def __init__(self, x, y, radius, fill=None) -> None:
        global window
        self.x = x
        self.y = y
        self.radius = radius
        self.fill = fill
        self.window = window
        self.circle = g.Circle(g.Point(x, y), radius)
        self.circle.setFill(fill)
        self.circle.draw(self.window)
        self.drawn = True
        objects.append(self.circle)
        
    def hide(self):
        if self.drawn:
            self.circle.undraw()
            self.drawn = False
    
    def show(self):
        if not self.drawn:
            self.circle.draw(self.window)
            self.drawn = True
            
    def move(self, dx=0, dy=0):
        self.circle.move(dx, dy)

class Line:
    def __init__(self, x1, y1, x2, y2, fill=None) -> None:
        global window
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.fill = fill
        self.window = window
        self.line = g.Line(g.Point(self.x1, self.y1), g.Point(self.x2, self.y2))
        self.line.setFill(fill)
        self.line.draw(self.window)
        self.drawn = True
        objects.append(self.line)
        
    def hide(self):
        if self.drawn:
            self.line.undraw()
            self.drawn = False
    
    def show(self):
        if not self.drawn:
            self.line.draw(self.window)
            self.drawn = True
            
    def move(self, dx=0, dy=0):
        self.line.move(dx, dy)

class Text:
    def __init__(self, x, y, text="", fill=None) -> None:
        global window
        self.x = x
        self.y = y
        self.fill = fill
        self.text = text
        self.window = window
        self.text = g.Text(g.Point(self.x, self.y), self.text)
        self.text.setFill(fill)
        self.text.draw(self.window)
        self.drawn = True
        objects.append(self.text)
        
    def hide(self):
        if self.drawn:
            self.text.undraw()
            self.drawn = False
    
    def show(self):
        if not self.drawn:
            self.text.draw(self.window)
            self.drawn = True
            
    def move(self, dx=0, dy=0):
        self.text.move(dx, dy)

class Entry:
    def __init__(self, x, y, width, fill=None) -> None:
        global window
        self.x = x
        self.y = y
        self.fill = fill
        self.width = width
        self.window = window
        self.entry = g.Entry(g.Point(self.x, self.y), self.width)
        self.entry.setFill(fill)
        self.entry.draw(self.window)
        self.drawn = True
        objects.append(self.entry)
    
    def get_text(self):
        return self.entry.getText()
        
    def hide(self):
        if self.drawn:
            self.entry.undraw()
            self.drawn = False
    
    def show(self):
        if not self.drawn:
            self.entry.draw(self.window)
            self.drawn = True
            
    def move(self, dx=0, dy=0):
        self.entry.move(dx, dy)

class Image:
    def __init__(self, x, y, filename) -> None:
        global window
        self.x = x
        self.y = y
        self.filename = filename
        self.window = window
        self.img = g.Image(g.Point(self.x, self.y), self.filename)
        self.img.draw(self.window)
        self.drawn = True
        objects.append(self.img)
        
    def hide(self):
        if self.drawn:
            self.img.undraw()
            self.drawn = False
    
    def show(self):
        if not self.drawn:
            self.img.draw(self.window)
            self.drawn = True
            
    def move(self, dx=0, dy=0):
        self.img.move(dx, dy)
        
#Polygon not working
"""class Polygon:
    def __init__(self, *points, fill=None) -> None:
        global window
        self.window = window
        self.line = g.Polygon(points)
        self.line.setFill(fill)
        self.line.draw(self.window)
        self.drawn = True
        objects.append(self.line)
        
    def hide(self):
        if self.drawn:
            self.line.undraw()
            self.drawn = False
    
    def show(self):
        if not self.drawn:
            self.line.draw(self.window)
            self.drawn = True
            
    def move(self, dx=0, dy=0):
        self.line.move(dx, dy)
"""