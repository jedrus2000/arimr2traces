# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QDialog
from PyQt5 import uic

from .resources.resources import FETCHING_DATA_PROGRESS_DIALOG_FORM


class FetchingDataProgressDialog(QDialog):
    """
    Progress dialog while fetching data

    """
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        uic.loadUi(FETCHING_DATA_PROGRESS_DIALOG_FORM, self)
        self.cancelButton.clicked.connect(self.reject)

    def setProgressValue(self, value):
        self.progressBar.setValue(value)
        if value == self.progressBar.maximum():
            self.accept()
