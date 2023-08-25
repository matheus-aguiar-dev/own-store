import subprocess
import time
import gi
gi.require_version("Gtk", '3.0')
from gi.repository import Gtk

class SignalsController:
    def __init__(self, main):
        self.main = main
        
    def quit(self, arg):
        self.main.window.hide()
        self.main.window_app.hide()
        self.main.window_loading.hide()
        Gtk.main_quit()
    def show(self,arg):
        arg.show_all()
    def hide(self,arg):
        arg.hide()
    def MainWindow(self, arg):
        self.main.brand.set_from_file(self.main.json["logo"])

        if(self.main.net_controller.isNetworkConnected() == True):
            if(self.main.net_controller.isFlathubEnabled(self.main.progress) == True):
                self.main.window.show_all()
                self.main.netwarning.hide()
                self.main.button_install.set_sensitive(True)
                self.main.cancel_install.show()
            else:
                self.main.installFlathub(self.main.window)
                self.main.button_install.set_sensitive(False)
                self.main.cancel_install.hide()
        else:
            self.main.netwarning.show() 
    def AppWindow(self, arg):
        if(self.main.net_controller.isNetworkConnected() == True):
            if(self.main.net_controller.isFlathubEnabled(self.main.progress) == True):
                self.main.window_app.show_all()
                self.main.netwarning.hide()
                self.main.button_install.set_sensitive(True)
                self.main.cancel_install.show()
            else:
                self.main.installFlathub(self.main.window_app)
                self.main.button_install.set_sensitive(False)
                self.main.cancel_install.hide()
            self.main.button_install.set_sensitive(True)
            self.main.netwarning1.hide()
        else:
            self.main.netwarning1.show()
            self.main.button_install.set_sensitive(False)

        if(self.main.net_controller.isAppInstaled(self.main.exec_name) == True):
            self.main.button_install.hide()
            self.main.button_remove.show()
            self.main.button_open.show()
        else:
            self.main.button_remove.hide()
            self.main.button_open.hide()
            self.main.button_install.show()
        

    def ListWindow(self, arg):
        if(self.main.net_controller.isNetworkConnected() == True):
            if(self.main.net_controller.isFlathubEnabled(self.main.progress) == True):
                self.main.window_list.show_all()
                self.main.netwarning2.hide()
                self.main.cancel_install.show()
            else:
                self.main.installFlathub(self.main.window_list)
                self.main.cancel_install.hide()
            self.main.netwarning2.hide()
        else:
            self.main.netwarning2.show()

    
        



