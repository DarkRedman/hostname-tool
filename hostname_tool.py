##!/usr/bin/python
 # -*- coding: utf-8 -*-

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class HostnameToolWindow(Gtk.Window):
    """Hostname Tool Window class, with all GUI and program logic"""

    def __init__(self):
        """Fires up the GUI"""
        super(HostnameToolWindow, self).__init__()

        self.set_title ("Hostname Tool")
        self.set_size_request (320, 150)

        self.current_hostname_label = Gtk.Label(label="Current hostname: ")
        self.desired_hostname_label = Gtk.Label(label="New hostname: ")

        self.current_hostname_textbox = Gtk.Entry()
        self.current_hostname_textbox.set_text(self.get_hostname())

        self.desired_hostname_textbox = Gtk.Entry ()

        self.change_hostname_button = Gtk.Button(label="Change hostname")
        self.change_hostname_button.connect("clicked", self.change_hostname, None)
        self.change_hostname_button.connect_object("clicked", Gtk.Widget.destroy, self)
        self.change_hostname_button.set_size_request(295, -1)

        fix = Gtk.Fixed ()

        fix.put(self.current_hostname_label, 10, 20)
        fix.put(self.current_hostname_textbox, 140, 15)
        fix.put(self.desired_hostname_label, 10, 60)
        fix.put(self.desired_hostname_textbox, 140, 55)
        fix.put(self.change_hostname_button, 10, 100)

        self.add(fix)

        self.connect("destroy", Gtk.main_quit)
        self.show_all()

    def change_hostname(self, widget, data=None):
        """Changes the name of the computer"""

        current_hostname = self.get_hostname()
        new_hostname = self.desired_hostname_textbox.get_text()

        if new_hostname:
            try:
                with open("/etc/hostname", "w") as f:
                    f.writeline(new_hostname)

                with open("/etc/hosts", "r") as f:
                    data = f.read()

                assert current_hostname in data,"Current hostname invalid"

                with open("/etc/hosts", "w") as f:
                    f.write(data.replace(current_hostname, new_hostname))
            except PermissionError as e:
                if e.errno == 13:
                    self.dia = Gtk.Dialog(title='ERROR', parent=self, modal=True, destroy_with_parent=True)
                    self.dia.vbox.pack_start(Gtk.Label(label='You must relaunch the app with root privileges !'), True, True, 0)
                    self.button = Gtk.Button(label="Ok")
                    self.button.connect("clicked", self.close_dialog, None)
                    self.dia.vbox.add(self.button)
                    self.dia.show_all()
                    result = self.dia.run()
                    self.dia.hide()

                else:
                    print("I/O error({0}): {1}".format(e.errno, e.strerror))
        else:
            print("Empty hostname!")

    def get_hostname(self):
        """Returns the current computer name"""

        with open("/etc/hostname", "r") as f:
            hostname = f.read().strip()
        return hostname

    def close_dialog(self,*args): # we won't use *args
        if self.dia:
            self.dia.destroy()

def main():
    """Starts the Hostname tool"""
    hostname_tool_window = HostnameToolWindow()
    Gtk.main()

if __name__ == "__main__":
    main ()
