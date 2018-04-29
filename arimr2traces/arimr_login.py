# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QDialog
from PyQt5 import uic

from .resources.resources import ARIMR_LOGIN_DIALOG_FORM

class ARIMRLoginDialog(QDialog):
    """
    ARiMR login page

    """
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        uic.loadUi(ARIMR_LOGIN_DIALOG_FORM, self)
        self.loginLineEdit.setFocus()
