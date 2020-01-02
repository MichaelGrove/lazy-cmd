# -*- coding: utf-8 -*-
import os
import sys
import json
import tkinter as tk
import threading
import queue
import subprocess
from tkinter.scrolledtext import ScrolledText


def command_thread(cmd, display_feed, thread_queue=None):
    display_feed('\n> %s\n' % " ".join(cmd))
    theproc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    stdout, stderr = theproc.communicate()
    if stdout:
        display_feed(stdout)
    if stderr:
        display_feed(stderr)
    thread_queue.put("Command finished")

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

    def load_cmd(self, filename):
        try:
            with open('%s/commands/%s' % (self.cwd, filename)) as f:
                content = f.read()
                return content.split(" ")
        except:
            return "echo File %s not found." % filename


    def create_widgets(self):
        self.widget_output_screen()
        self.widget_action_buttons()

    def widget_action_buttons(self):
        self.actions = []
        commands = self.config["commands"]

        for command in commands:
            button = tk.Button(self, text = command["label"], command = lambda command=command: self.run_command(command["cmd"]))
            button.pack(fill = tk.X)
            self.actions.append(button)

    def run_command(self, cmd):
        self.thread_queue = queue.Queue()
        self.new_thread = threading.Thread(
            target = command_thread,
            kwargs = {
                'cmd': self.load_cmd(cmd),
                'display_feed': self.update_output_screen,
                'thread_queue': self.thread_queue
            }
        )
        self.new_thread.start()
        self.after(100, self.listen_for_result)

    def listen_for_result(self):
        try:
            self.res = self.thread_queue.get(0)
            print(self.res)
        except queue.Empty:
            self.after(100, self.listen_for_result)

    def widget_output_screen(self):
        self.output_screen = ScrolledText(self)
        self.output_screen.pack(side="right") 
        self.output_screen.config(foreground='white')
        self.output_screen.config(background='black')
        self.output_screen.insert(tk.END, "Welcome. \n")
    
    def update_output_screen(self, feed):
        self.output_screen.insert(tk.END, feed)
        self.output_screen.see(tk.END)
        pass

try:
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
except Exception as e:
    with open('err.log', "w") as log:
        log.write(str(e))
