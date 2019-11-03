import os
import sys
import json
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from ActionButton import ActionButton


class Application(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.winfo_toplevel().title("Lazy CMD")
        self.pack()
        self.cwd = os.getcwd()
        self.config = self.load_config()        
        self.create_widgets()

    def load_config(self):
        try:
            with open('%s./config.json' % self.cwd) as f:
                content = json.load(f)
                f.close()
                return content
        except:
            sys.exit(0)

    def create_widgets(self):
        self.widget_output_screen()
        self.widget_action_buttons()

    def widget_action_buttons(self):
        self.actions = []
        commands = self.config["commands"]
        for command in commands:
            action_button = ActionButton(command["label"], command["cmd"], self.output_screen)
            button = tk.Button(self, text = action_button.label, command = action_button.run_cmd)
            button.pack()
            self.actions.append(button)

    def widget_output_screen(self):
        self.output_screen = ScrolledText(self)
        self.output_screen.pack(side="right") 


root = tk.Tk()
app = Application(master=root)
app.mainloop()
