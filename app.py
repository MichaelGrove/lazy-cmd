# -*- coding: utf-8 -*-
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
            with open('%s/config.json' % self.cwd, encoding="utf-8") as f:
                content = json.load(f)
                return content
        except:
            self.create_config()
            return self.load_config()

    def create_config(self):
        data = {}
        data['commands'] = []
        data['commands'].append({
            'label': 'Directory',
            'cmd': 'dir.cmd'
        })

        with open('%s/config.json' % self.cwd, "w") as cfg:
            json.dump(data, cfg)
        
        filename = '%s/commands/dir.cmd' % self.cwd
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w") as f:
            f.write("dir")

    def create_widgets(self):
        self.widget_output_screen()
        self.widget_action_buttons()
    
    def widget_action_buttons(self):
        self.actions = []
        commands = self.config["commands"]

        for command in commands:
            action_button = ActionButton(command["label"], command["cmd"], self.output_screen)
            button = tk.Button(self, text = action_button.label, command = action_button.run_cmd)
            button.pack(fill=tk.X)
            self.actions.append(button)

    def widget_output_screen(self):
        self.output_screen = ScrolledText(self)
        self.output_screen.pack(side="right") 
        self.output_screen.config(foreground='white')
        self.output_screen.config(background='black')
        self.output_screen.insert(tk.END, "Welcome. \n")

try:
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
except Exception as e:
    with open('err.log', "w") as log:
        log.write(str(e))
