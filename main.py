import gi
import sys
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib, Gdk
import argparse

from datetime import datetime

class ClockWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Mirror Clock")

        self.label = Gtk.Label()
        self.label.set_justify(Gtk.Justification.CENTER)
        
        self.format = "%A %B %d, %I:%M:%S %p"

        self.on_timeout(None)

        self.timeout_id = GLib.timeout_add_seconds(1, self.on_timeout, None)
        
        self.add(self.label)

    def on_timeout(self, user_data):
        n = datetime.now()

        self.label.set_text(n.strftime(self.format))

        return True

def main(args):
    get_styles()
    window = ClockWindow()
    # window.override_background_color()
    window.set_app_paintable(True)
    window.set_decorated(False)
    window.set_visual(window.get_screen().get_rgba_visual())
    window.connect("destroy", Gtk.main_quit)
    window.show_all()

    if not args.geometry is None:
        if not window.parse_geometry(args.geometry):
            print('geometry "{}" not parsed.')


    try:
        Gtk.main()
    except KeyboardInterrupt:
        pass
    
    print('shutting down')

def get_styles():
    css = b"""
    label { 
        font-size: 100px;
        font-family: Carlito; 
        color: white;
        text-shadow: grey;
    }
    GtkLayout {
       background-color: transparent;
    }

    /*
    GtkViewport {
        background-color: transparent;
    }
    */
    """

    style_provider = Gtk.CssProvider()
    style_provider.load_from_data(css)

    context = Gtk.StyleContext()
    screen = Gdk.Screen.get_default()

    context.add_provider_for_screen(
        screen,
        style_provider,
        Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--geometry", help="X windows geometry parameter")

    args = parser.parse_args()
    main(args)