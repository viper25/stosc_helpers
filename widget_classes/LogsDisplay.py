import logging
from tkinter.constants import END
import customtkinter

import logging
import tkinter as tk


class TkinterTextHandler(logging.Handler):
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget

    def emit(self, record):
        msg = self.format(record)
        self.text_widget.configure(state='normal')
        self.text_widget.insert(END, msg + '\n')
        self.text_widget.configure(state='disabled')
        self.text_widget.see(END)

    # Usage example


if __name__ == "__main__":
    # Create a simple Tkinter window with a Text widget for displaying logs
    root = tk.Tk()
    root.title("Tkinter Logging Example")
    text_widget = tk.Text(root, wrap='word', state='disabled', width=50, height=20)
    text_widget.grid(row=0, column=0, padx=5, pady=5)

    # Create and set the TkinterTextHandler for the root logger
    text_handler = TkinterTextHandler(text_widget)
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] - %(message)s')
    text_handler.setFormatter(formatter)
    logging.getLogger().addHandler(text_handler)
    logging.getLogger().setLevel(logging.DEBUG)

    # Generate some log messages
    logging.debug("Debug message")
    logging.info("Info message")
    logging.warning("Warning message")
    logging.error("Error message")
    logging.critical("Critical message")

    root.mainloop()