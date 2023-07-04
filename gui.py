import PySimpleGUI as sg
import sys
win = lambda: start()
p_name, p_path = "", ""

def start():
    global win
    layout = [[sg.Button(button_text="New Project", key="NP")],
              [sg.Button(button_text="Load Project", key="LP")]]
    window = sg.Window("Pysudo Engine", layout)
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED: sys.exit()
        if event == "NP": 
            win = lambda: new_project()
            break
        if event == "LP": 
            win = lambda: load_project()
            break
    window.close()

def new_project():
    global win, p_name, p_path
    layout = [[sg.Text("Project Name:"), sg.Input(key='P_NAME')],
            [sg.Text("Project Path:"), sg.Input(key='P_PATH', change_submits=True), sg.FolderBrowse(key="P_BROWSE")],
            [sg.Button('Create'), sg.Button('Quit')]]
    window = sg.Window('New Project', layout)
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Quit':
            sys.exit()
        if event == "Create":
            p_name = values["P_NAME"]
            p_path = values["P_PATH"]
            win = lambda: main()
            break
    window.close()

def load_project():
    global win, p_name, p_path
    layout = [[sg.Text("Project Path:"), sg.Input(key='P_PATH'), sg.FolderBrowse(key="P_BROWSE")],
            [sg.Button('Load')]]
    window = sg.Window('Load Project', layout)
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Quit':
            sys.exit()
        if event == "Load":
            p_name = ""
            p_path = values["P_PATH"]
            win = lambda: main()
            break
    window.close()

def test():
    layout = []
    window = sg.Window('Test', layout)
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Quit':
            sys.exit()
    window.close()

def main():
    global p_name
    layout = [[sg.Button('Sprites', key="SP")],
              [sg.Button('Quit')]]
    window = sg.Window(p_name, layout)
    print(p_name, p_path)
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Quit':
            sys.exit()
    window.close()

if __name__ == "__main__":
    while True:
        win()
