from .gui import GUI
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    app = GUI(root)
    app.run()
