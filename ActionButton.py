import os
import sys
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
                return content.split(" ")
        except:
            return "echo File %s not found." % filename

    def run_cmd(self):
        cmd = self.load_cmd(self.command_filename)
        self.output_screen.insert(tk.END, '\n> %s' % " ".join(cmd))

        theproc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        stdout, stderr = theproc.communicate()
        if stdout:
            self.display_feed(stdout)
        if stderr:
            self.display_feed(stderr)
    
    def display_feed(self, feed):
        self.output_screen.insert(tk.END, feed)
        self.output_screen.see(tk.END)
