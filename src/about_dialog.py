# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QDialog
from PyQt5 import uic
from .resources.resources import ABOUT_DIALOG_FORM


class AboutDialog(QDialog):
    """
    About Dialog

    """
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        uic.loadUi(ABOUT_DIALOG_FORM, self)
        self.closePushButton.clicked.connect(self.close)

