import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class GUI(Gtk.Window):
    def __init__(self, method):
        Gtk.Window.__init__(self)

        self.method = method
        # Initinal window data
        self.set_title("Project Link")
        self.set_border_width(10)
        self.set_size_request(350, 200)
        self.set_resizable(False)

        # Navbar icon
        self.set_icon_from_file(r'Documents\Other\projectlink_sm_icon.png')

        # Box
        vbox = Gtk.VBox()
        self.add(vbox)

        # Label
        username_label = Gtk.Label("Welcome to Project Link!")
        vbox.pack_start(username_label, True, True, 0)

        # Username input
        self.username_input = Gtk.Entry()
        self.username_input.set_text("iyonatan")
        vbox.pack_start(self.username_input, True, True, 0)

        # Password input
        self.pwd_input = Gtk.Entry()
        self.pwd_input.set_text("123456")
        self.pwd_input.set_visibility(False)
        vbox.pack_start(self.pwd_input, True, True, 0)

        # Login button
        self.button = Gtk.Button(label="Login")
        self.button.connect("clicked", self.method)
        vbox.pack_start(self.button, True, True, 0)

        # Link button
        label = Gtk.Label()
        label.set_markup("<a href=\"http://projectlink.net23.net\" title=\"Go to Project Link website\">Register</a>")

    def loading(self, wait=False):
        if wait:
            self.button.set_sensitive(False)
            self.button.set_label("Wait")
        else:
            self.button.set_sensitive(True)
            self.button.set_label("Login")


