# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QDialog
from PyQt5 import uic


class AboutDialog(QDialog):
    """
    About Dialog

    """
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        uic.loadUi('./forms/about_dialog.ui', self)
        self.closePushButton.clicked.connect(self.close)

