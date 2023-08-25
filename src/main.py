import gi
import json
import time
from threading import Thread
from netmanager import NetManager 
from handler import SignalsController
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, Gio, Gdk

class Store(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)

        self.net_controller = NetManager()

        self.builder = Gtk.Builder()
        self.builder.add_from_file("/usr/share/own-store/resources/ui/main.ui")
        self.builder.connect_signals(SignalsController(self))
        
        self.t2 = None
        self.exec_name = None
        self.window = self.builder.get_object("main")
        self.window_app = self.builder.get_object("appinfo")
        self.window_loading = self.builder.get_object("loading")
        self.window_list = self.builder.get_object("applist")

        self.brand = self.builder.get_object("brand")
        self.grid = self.builder.get_object("rec_grid")
        self.cat_grid = self.builder.get_object("cat_grid")
        self.box_list = self.builder.get_object("box_list")
        self.netwarning = self.builder.get_object("netwarning")
        self.netwarning1 = self.builder.get_object("netwarning1")
        self.netwarning2 = self.builder.get_object("netwarning2")
        self.app_container = self.builder.get_object("app_container")
        self.app_icon = self.builder.get_object("app_icon")
        self.app_name = self.builder.get_object("app_name")
        self.app_description = self.builder.get_object("app_description")
        self.button_network = self.builder.get_object("net_button")
        self.button_network1 = self.builder.get_object("net_button1")
        self.button_network2 = self.builder.get_object("net_button1")
        self.button_more_apps = self.builder.get_object("button_more_apps")
        self.button_open = self.builder.get_object("button_open")
        self.button_remove = self.builder.get_object("button_remove")
        self.button_install = self.builder.get_object("button_install")
        self.installing_label = self.builder.get_object("installing_name")
        self.progress = self.builder.get_object("progress")
        self.cancel_install = self.builder.get_object("cancel_install")

        self.json = self.get_metadata()
        self.get_theme()
        self.create_main_apps_icons()
        self.get_apps_by_category()

        self.window.connect("delete-event", Gtk.main_quit)
        self.window_app.connect("delete-event", Gtk.main_quit)
        self.window_loading.connect("delete-event", Gtk.main_quit)
        self.button_remove.connect("clicked", self.on_remove_clicked)
        self.button_install.connect("clicked", self.on_install_clicked)
        self.button_open.connect("clicked", self.on_open_clicked)
        self.button_network.connect("clicked", self.net_controller.openGnomeNetwork)
        self.button_network1.connect("clicked", self.net_controller.openGnomeNetwork)
        self.button_network2.connect("clicked", self.net_controller.openGnomeNetwork)
        self.button_more_apps.connect("clicked", self.net_controller.openGnomeSoftware)
        self.cancel_install.connect("clicked", self.cancelProcess)

        self.window.show_all()
            

    def get_metadata(self):
        with open('/usr/share/own-store/src/metadata.json') as file:
            return json.load(file)

    def get_theme(self):
        settings = Gtk.Settings.get_default()
        theme_name = settings.get_property('gtk-theme-name')
        if(theme_name == "Adwaita"):
            self.theme = "bgwhite" 
        else:
            self.theme = "bgblack"


    def installFlathub(self, window):
        def install_process():
            success = self.net_controller.installFlathub(self.progress, self.installing_label)
            if success:
                time.sleep(1)
                window.show()
                self.window_loading.hide()
            else:
                # Handle the case where installation failed
                print("Installation failed, check the error message.")

        def loading_window():
            window.hide()
            self.window_loading.show()
        t1 = Thread(target=loading_window)
        t1.start()
        t1.join()
        self.t2 = Thread(target=install_process)
        self.t2.start()

    def cancelProcess(self, button):
        self.net_controller.cancelProcess(self.t2)

    def create_main_apps_icons(self):
        for i,apps in enumerate(self.json["apps"]):
            if(i == 10):
                break;
            row = i % 2
            col = i // 2
            vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
            vbox.set_name(self.theme)
            image = Gtk.Image()
            pixbuf = GdkPixbuf.Pixbuf.new_from_file(apps["icon"])  # Replace "image.png" with your image file path
            scaled_pixbuf = pixbuf.scale_simple(60, 60, GdkPixbuf.InterpType.BILINEAR)
            image.set_from_pixbuf(scaled_pixbuf)

            event_box = Gtk.EventBox()  # Create an EventBox
            event_box.add(vbox)
            event_box.connect("button-press-event", self.on_app_clicked, apps["name"], pixbuf, apps["exec"], apps["description"])  # Connect the "button-press-event" signal to a callback function<<
            self.grid.attach(event_box, col, row , 1, 1)
            label = Gtk.Label()
            label.set_text(apps["name"])
            vbox.pack_start(image, False, False, 0)
            vbox.pack_start(label, False, False, 0)

    def get_apps_by_category(self):
        for i,cat in enumerate(self.json["categories"]):
            row = i % 2
            col = i // 2
            vbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
            vbox.set_name(self.theme)
            event_box = Gtk.EventBox()  # Create an EventBox
            event_box.add(vbox)
            if cat == "More Apps":
                event_box.connect("button-press-event", self.on_more_apps_clicked)
            else:
                event_box.connect("button-press-event", self.on_cat_clicked, self.json["apps"], cat )  
            self.cat_grid.attach(event_box, col, row , 1, 1)
            label = Gtk.Label()
            label.set_text(cat)
            vbox.pack_start(label, True, False, 0)

    def on_app_clicked(self, event_box, event, name, pixbuf, exec_name, description):
        self.app_container.set_name(self.theme)
        self.exec_name = exec_name
        self.name = name
        scaled_pixbuf = pixbuf.scale_simple(100, 100, GdkPixbuf.InterpType.BILINEAR)
        self.app_icon.set_from_pixbuf(scaled_pixbuf)
        self.window_app.set_title(name)
        self.app_name.set_text(name)
        self.app_description.set_text(description)
        self.window_app.show_all()

    def on_cat_clicked(self, event_box, event,json, cat_name):
        children = self.box_list.get_children()
        for child in children:
            self.box_list.remove(child)
        for apps in json:
            if cat_name in apps["category"]:
                hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
                vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
                hbox.set_name(self.theme)
                event_box = Gtk.EventBox()
                event_box.add(hbox)
                pixbuf = GdkPixbuf.Pixbuf.new_from_file(apps["icon"])
                event_box.connect("button-press-event", self.on_app_clicked, apps["name"], pixbuf, apps["exec"], apps["description"])  # Connect the "button-press-event" signal to a callback function<<
                self.box_list.pack_start(event_box, True, True, 0)

                image = Gtk.Image()
                scaled_pixbuf = pixbuf.scale_simple(60, 60, GdkPixbuf.InterpType.BILINEAR)
                image.set_from_pixbuf(scaled_pixbuf)

                label = Gtk.Label()
                label.set_name("title_label")
                label.set_text(apps["name"])
                label.set_halign(Gtk.Align.START)

                description = Gtk.Label()
                description.set_text(self.set_max_label_text(apps["description"]))
                description.set_halign(Gtk.Align.START)

                hbox.pack_start(image, False, False, 0)
                hbox.pack_start(vbox, False, False, 10)
                vbox.pack_start(label, False,False, 0)
                vbox.pack_start(description, False, False, 0)

        self.window_list.set_title(cat_name)
        self.window_list.show_all()
    
    def on_more_apps_clicked(self, event_box, event):
        self.net_controller.openGnomeSoftware("foo")

    def set_max_label_text(self,text):
        max_chars = 80
        if len(text) > max_chars:
            break_line = text[:40] + "\n"
            truncated_text = break_line + text[40:max_chars] + "..."  # Add ellipsis if truncated
            return truncated_text
        else:
            break_line = text[:40] + "\n"
            custom_text = break_line + text[40:max_chars]
            return custom_text

    def on_remove_clicked(self, button):
        success = self.net_controller.removeApp(self.exec_name)
        if success == True:
            self.window_app.hide()
            self.window.show()
        else:
            pass

    def on_install_clicked(self, button):
        def install_process():
            success = self.net_controller.installApp(self.exec_name, self.progress, self.installing_label, self.name)
            if success:
                self.window_app.show()
                self.window_loading.hide()
            else:
                # Handle the case where installation failed
                print("Installation failed, check the error message.")
        def loading_window():
            self.window_app.hide()
            self.window_loading.show()

        t1 = Thread(target=loading_window)
        t1.start()
        t1.join()
        self.t2 = Thread(target=install_process)
        self.t2.start()

    def on_open_clicked(self, button):
        success = self.net_controller.openApp(self.exec_name)
        if success:
            print("Performing additional actions...")
        else:
            print("Uninstallation failed, check the error message.")


win = Store()
css_provider = Gtk.CssProvider()
css_provider.load_from_path('/usr/share/own-store/resources/style.css')
screen = Gdk.Screen.get_default()
style_context = Gtk.StyleContext()
style_context.add_provider_for_screen(screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

Gtk.main()

