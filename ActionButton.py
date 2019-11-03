import os
import tkinter as tk
import subprocess


class ActionButton():

    def __init__(self, label, command_filename, output_screen):
        self.label = label
        self.command_filename = command_filename
        self.output_screen = output_screen
        self.cwd = os.getcwd()
    
    def load_cmd(self, filename):
        try:
            with open('%s/commands/%s' % (self.cwd, filename)) as f:
                content = f.read()
                f.close()
                return content
        except:
            return "echo File %s not found." % filename

    def run_cmd(self):
        cmd = self.load_cmd(self.command_filename)
        feed = os.popen(cmd).read()
        self.display_feed(feed)
    
    def get_output_total_length(self):
        return len(self.output_screen.get("1.0", tk.END))

    def display_feed(self, feed):
        if self.get_output_total_length() > 2:
            self.output_screen.insert(tk.END, "\n-----------------------\n")
        
        self.output_screen.insert(tk.END, feed)
        self.output_screen.see(tk.END)