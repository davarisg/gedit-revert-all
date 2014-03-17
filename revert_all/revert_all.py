# Revert-All Gedit plugin
#
# Description: This Gedit plugin will revert all of your window's
#              open tabs to the last saved version.

from gi.repository import GObject, Gtk, Gedit

UI_XML = """
<ui>
    <menubar name="MenuBar">
        <menu name="FileMenu" action="File">
            <placeholder name="FileOps_4">
                <menuitem name="Revert All" action="RevertAll"/>
            </placeholder>
        </menu>
    </menubar>
</ui>
"""

class RevertAll(GObject.Object, Gedit.WindowActivatable):
    __gtype_name__ = "RevertAll"
    window = GObject.property(type=Gedit.Window)

    def __init__(self):
        GObject.Object.__init__(self)

    # This function will get called when a user activates the
    # plugin.
    # Add the necessary UI for the plugin to show up on the menu
    # and the callback function.
    def _add_ui(self):
        manager = self.window.get_ui_manager()
        self._actions = Gtk.ActionGroup("revert_actions")
        self._actions.add_actions([
            (
               'RevertAll',
               '',
               'Revert All',
               None,
               'Revert all tabs',
               self.on_revert_all
             )
        ])
        manager.insert_action_group(self._actions)
        self._ui_merge_id = manager.add_ui_from_string(UI_XML)
        manager.ensure_update()

    # This function gets called when a user disables the plugin.
    # Remove the ui from the menu
    def _remove_ui(self):
        manager = self.window.get_ui_manager()
        manager.remove_ui(self._ui_merge_id)
        manager.remove_action_group(self._actions)
        manager.ensure_update()

    def do_activate(self):
        self._add_ui()

    def do_deactivate(self):
        self._remove_ui()

    def do_update_state(self):
        pass

    # Callback function to revert all tabs
    # Close and reload all tabs and skip untitled documents
    def on_revert_all(self, action, data=None):
        window = self.window
        documents = window.get_documents()

        for document in documents:
            if (document.is_untitled()): continue

            tab = window.get_tab_from_location(document.get_location())

            window.close_tab(tab)
            window.create_tab_from_location(
                document.get_location(),
                None,
                0,
                0,
                False,
                True
            )
