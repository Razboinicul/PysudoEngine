import tkinter as tk
from tkinter import ttk

def main():
    root = tk.Tk()
    root.geometry('300x200')
    root.resizable(False, False)
    root.title('')

    ttk.Label(root, text="First Label").grid(row=0, column=0)
    ttk.Label(root, text="Second Label").grid(row=0, column=2)

    root.mainloop()

if __name__ == "__main__": main()