# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QDialog
from PyQt5 import uic


class ARIMRLoginDialog(QDialog):
    """
    ARiMR login page

    """
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        uic.loadUi('./forms/arimr_login_dialog.ui', self)
        self.loginLineEdit.setFocus()
