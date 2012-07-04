##!/usr/bin/python
 # -*- coding: utf-8 -*-

import gtk

class HostnameToolWindow (gtk.Window):
    """Hostname Tool Window class, with all GUI and program logic"""

    def __init__(self):
        """Fires up the GUI"""
        super(HostnameToolWindow, self).__init__()

        self.set_title ("Hostname Tool")
        self.set_size_request (300, 280)
        self.set_position (gtk.WIN_POS_CENTER)

        self.current_hostname_label = gtk.Label ("Current hostname: ")
        self.desired_hostname_label = gtk.Label ("New hostname: ")

        self.current_hostname_textbox = gtk.Entry ()
        self.current_hostname_textbox.set_text (self.get_hostname ())

        self.desired_hostname_textbox = gtk.Entry ()

        self.change_hostname_button = gtk.Button ("Change hostname")
        self.change_hostname_button.connect ("clicked", self.change_hostname,
                                                None)
        self.change_hostname_button.connect_object ("clicked",
                                                    gtk.Widget.destroy, self)
        self.change_hostname_button.set_size_request (295, -1)

        fix = gtk.Fixed ()

        fix.put (self.current_hostname_label, 10, 20)
        fix.put (self.current_hostname_textbox, 140, 15)
        fix.put (self.desired_hostname_label, 10, 60)
        fix.put (self.desired_hostname_textbox, 140, 55)
        fix.put (self.change_hostname_button, 10, 100)

        self.add (fix)

        self.connect ("destroy", gtk.main_quit)
        self.show_all ()

    def change_hostname (self, widget, data=None):
        """Changes the name of the computer"""

        new_hostname = self.desired_hostname_textbox.get_text ()
        
        try:
            hostname_file = open ("/etc/hostname", "w")
            hostname_file.write (new_hostname)
            hostname_file.close ()

            hosts_file = open ("/etc/hosts", "r")
            hosts_lines = hosts_file.readlines ()
            hosts_file.close ()

            hosts_lines[1] = hosts_lines[1].split ()[0] + " " + new_hostname

            hosts_file = open ("/etc/hosts", "w")
            hosts_file.writelines (hosts_lines)
            hosts_file.close ()
        except IOError as (errno, strerror):
            if errno == 13:
                self.dia = gtk.Dialog('ERROR', self, 
                gtk.DIALOG_MODAL  | gtk.DIALOG_DESTROY_WITH_PARENT)
                self.dia.vbox.pack_start(gtk.Label('You must relaunch the app with root privileges !'))
                self.button = gtk.Button("Ok")
                self.button.connect("clicked", self.close_dialog, None)
                self.dia.vbox.add(self.button)
                self.dia.show_all()
                result = self.dia.run()
                self.dia.hide()

            else:
                print("I/O error({0}): {1}".format(errno, strerror))

    def get_hostname (self):
        """Returns the current computer name"""

        hostname_file = open ("/etc/hostname", "r")
        hostname = hostname_file.read()
        hostname_file.close()
        return hostname

    def close_dialog(self,*args): # we won't use *args
        if self.dia:
            self.dia.destroy()

def main ():
    """Starts the Hostname tool"""
    hostname_tool_window = HostnameToolWindow ()
    gtk.main ()

if __name__ == "__main__":
    main ()