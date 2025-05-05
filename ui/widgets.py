import customtkinter as ctk
from tkinter import messagebox

def create_entry_label_frame(master, label_text, entry_var):
    """
    Creates a label and entry widget for user input.
    :param master: The parent widget
    :param label_text: The text for the label
    :param entry_var: The variable to bind to the entry widget
    :return: The frame containing the label and entry
    """
    frame = ctk.CTkFrame(master)
    label = ctk.CTkLabel(frame, text=label_text)
    label.pack(side="left", padx=10, pady=5)
    entry = ctk.CTkEntry(frame, textvariable=entry_var)
    entry.pack(side="left", padx=10, pady=5)
    frame.pack(pady=5)
    return frame


def create_button(master, text, command):
    """
    Creates a button widget that triggers the given command.
    :param master: The parent widget
    :param text: The text for the button
    :param command: The function to call when the button is clicked
    :return: The button widget
    """
    button = ctk.CTkButton(master, text=text, command=command)
    button.pack(pady=10)
    return button

def show_error(message):
    """
    Shows an error message in a pop-up.
    :param message: The message to show in the pop-up
    """
    messagebox.showerror("Error", message)

def show_info(message):
    """
    Shows an information message in a pop-up.
    :param message: The message to show in the pop-up
    """
    messagebox.showinfo("Information", message)
