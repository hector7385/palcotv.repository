# -*- coding: utf-8 -*-
# Licence: GPL v.3 http://www.gnu.org/licenses/gpl.html
# This is an XBMC addon for demonstrating the capabilities
# and usage of PyXBMCt framework.

import os
import xbmc, xbmcaddon, xbmcgui
from pyxbmct.addonwindow import *

_addon = xbmcaddon.Addon()
_addon_path = _addon.getAddonInfo('path')


class MyAddon(AddonDialogWindow):

    def __init__(self, title=''):
        super(MyAddon, self).__init__(title)
        self.setGeometry(350, 400, 9, 4)
        self.set_active_controls()
        # Connect a key action (Backspace) to close the window.
        self.connect(ACTION_NAV_BACK, self.close)

    def set_active_controls(self):
	int_label = Label('Elige canal a buscar:', alignment=ALIGN_CENTER)
	self.placeControl(int_label, 0, 0, 1, 3)        
        #
        self.list_item_label = Label('', textColor='0xFF808080')
        self.placeControl(self.list_item_label, 1, 1)
        # List
        self.list = List()
        self.placeControl(self.list, 2, 0, 4, 3)
        # Add items to the list
        items = ['Item %s' % i for i in range(1, 8)]
        self.list.addItems(items)
        # Connect the list to a function to display which list item is selected.
        self.connect(self.list, lambda: xbmc.executebuiltin('Notification(Note!,%s selected.)' %
                                            self.list.getListItem(self.list.getSelectedPosition()).getLabel()))
        # Connect key and mouse events for list navigation feedback.
        self.connectEventList(
            [ACTION_MOVE_DOWN, ACTION_MOVE_UP, ACTION_MOUSE_WHEEL_DOWN, ACTION_MOUSE_WHEEL_UP, ACTION_MOUSE_MOVE],
            self.list_update)

        # Button
        self.button = Button('Ok!')
        self.placeControl(self.button, 7, 3)
        # Connect control to close the window.
        self.connect(self.button, self.close)

    def list_update(self):
        # Update list_item label when navigating through the list.
        try:
            if self.getFocus() == self.list:
                self.list_item_label.setLabel(self.list.getListItem(self.list.getSelectedPosition()).getLabel())
            else:
                self.list_item_label.setLabel('')
        except (RuntimeError, SystemError):
            pass

    def setAnimation(self, control):
        # Set fade animation for all add-on window controls
        control.setAnimations([('WindowOpen', 'effect=fade start=0 end=100 time=500',),
                                ('WindowClose', 'effect=fade start=100 end=0 time=500',)])



def main():
    window = MyAddon('Agenda deportiva TV')
    window.doModal()

if __name__ == '__main__':
    main()
