import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage

from .config import FG_COLOR, BG_COLOR

class CircularButton:
    def __init__(self, mode_frame, row, col, bg):
         # Manual Mode Button
        self.button = tk.Canvas(mode_frame, width=150, height=150, bg=bg, highlightthickness=0)
        self.button.grid(row=row, column=col, padx=30)
        
    def set(self, text, size, fill):
        self.button.create_oval(10, 10, 120, 120, fill=fill, outline="")
        self.text = self.button.create_text(65, 65, text=text, fill=FG_COLOR, font=("Segoe UI", size, "bold"))

    def bind(self, handler):
        self.handler = handler
        self.button.tag_bind(self.text, "<Button-1>", lambda e: self.handler())
