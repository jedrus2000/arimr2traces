#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, \
    QDesktopWidget, QMessageBox
from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from .animal import *
from .animals_ids_qtable_model import *
from .arimr_data_qtable_model import *
from .animals_fetch_thread import AnimalFetchThread
from .about_dialog import AboutDialog
from .arimr_login import ARIMRLoginDialog
from .fetching_data_progress_dialog import FetchingDataProgressDialog
from .resources.resources import MAIN_WINDOW_FORM, APP_XPM_ICON


class App(QMainWindow):
    """
    Main Application window

    """
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        uic.loadUi(MAIN_WINDOW_FORM, self)
        self.setWindowIcon(QIcon(APP_XPM_ICON))
        #
        self.resetOrInitData()
        self.idNumbersTableView.setModel(self.animalIDsModel)
        self.arimrDataTableView.setModel(self.arimrModel)
        #
        self.actionAboutProgram.triggered.connect(self.actionAboutProgram_click)
        self.actionExit.triggered.connect(self.close)
        #
        self.menubar.addAction(self.actionAboutProgram)
        self.menubar.addAction(self.actionExit)
        #
        self.readIDsPushButton.clicked.connect(self.readIDsPushButton_on_click)
        self.getDataFromARIMRPushButton.clicked.connect(self.getDataFromARIMRPushButton_on_click)
        self.saveDataPushButton.clicked.connect(self.saveDataPushButton_on_click)
        #
        self.setComponentsBeforeIDsLoaded()
        self.center()
        self.show()

    def resetOrInitData(self):
        '''
        resets or inits all data fields

        :return:
        '''
        self.dataNeedSave = False
        self.animalIDsFileName = ''
        self.tracesFileName = ''
        self.reportFileName = ''
        self.animalIDsModel = AnimalIDsModel(self)
        self.arimrModel = ArimrDataModel(self.arimrDataTableView)


    def center(self):
        '''
        Center window on desktop upon start

        :return:
        '''
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def setComponentsBeforeIDsLoaded(self):
        '''
        Sets controlers state before IDs list is loaded, so everything is disabled
        :return:
        '''
        self.getDataFromARIMRPushButton.setEnabled(False)
        self.arimrDataTableView.setEnabled(False)
        self.saveReportCheckBox.setEnabled(False)
        self.saveTracesCheckBox.setEnabled(False)
        self.saveDataPushButton.setEnabled(False)

    def enableAndSetControlsForARIMRDataDownload(self):
        self.getDataFromARIMRPushButton.setEnabled(True)
        self.arimrDataTableView.setEnabled(True)
        self.saveReportCheckBox.setEnabled(True)
        self.saveTracesCheckBox.setEnabled(True)

    def createReportAndTracesFileNames(self):
        if not self.animalIDsFileName:
            return

        file_name_without_ext = os.path.splitext(self.animalIDsFileName)[0]
        path, file = os.path.split(os.path.abspath(file_name_without_ext))
        self.reportFileName = os.path.join(path, file+'_report.xlsx')
        self.tracesFileName = os.path.join(path, file+'_traces.csv')

    def loadAnimalsIDsListFromFile(self, file_name):
        '''
        Loads animals IDs list from file_name.
        Returns true on success

        :param file_name:
        :return:
        '''
        try:
            self.animalIDsModel.setData(read_list_of_ids(file_name))
            return True
        except OSError as e:
            return False

    def saveData(self):
        try:
            if self.saveTracesCheckBox.isChecked():
                self.tracesFileName = self.saveFileAsWithDialog('Zapisz plik w formacie TRACES', self.tracesFileName)
                if self.tracesFileName:
                    self.arimrModel.saveTracesFile(self.tracesFileName)

            if self.saveReportCheckBox.isChecked():
                self.reportFileName = self.saveFileAsWithDialog('Zapisz plik raportu w formacie Excela', self.reportFileName)
                if self.reportFileName:
                    self.arimrModel.saveReportFile(self.reportFileName)

            self.dataNeedSave = False
        except IOError as e:
            self.showErrorMsgBox('Błąd zapisu danych.',
                         'Wystąpił błąd zapisu danych : '+str(e))


    def checkAndAskForSavingData(self):
        if self.dataNeedSave and self.showYesNoMsgBox('', 'Dane nie są zapisane. Czy zapisać ?') == QMessageBox.Yes:
            self.saveData()


    def saveFileAsWithDialog(self, title, default_file_name_path):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, title, default_file_name_path,
                                                  "wszystkie pliki (*)", options=options)
        return fileName

    def showErrorMsgBox(self, title, text):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Critical)
        msg.setText(text)
        msg.setWindowTitle(title)
        msg.exec()

    def showYesNoMsgBox(self, title, text):
        return QMessageBox.question(self, title, text, QMessageBox.No, QMessageBox.Yes)

    #
    # events
    #
    def closeEvent(self, event):
        self.checkAndAskForSavingData()
        event.accept()


    @pyqtSlot()
    def actionAboutProgram_click(self):
        ab = AboutDialog(self)
        ab.show()

    @pyqtSlot()
    def readIDsPushButton_on_click(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "Wskaż plik z listą nr ident. zwierząt",
                                                   "", "All Files (*)", options=options)
        if file_name and self.loadAnimalsIDsListFromFile(file_name):
            self.animalIDsFileName = file_name
            self.createReportAndTracesFileNames()
            self.enableAndSetControlsForARIMRDataDownload()

    @pyqtSlot()
    def getDataFromARIMRPushButton_on_click(self):
        self.checkAndAskForSavingData()

        dlg = ARIMRLoginDialog(self)
        res = dlg.exec()

        if res:
            # reset old data before fetching new
            self.arimrModel.resetModel()
            #
            self.fdd = FetchingDataProgressDialog(self)
            self.fdd.progressBar.setRange(0, len(self.animalIDsModel.listOfAnimalsIDs))
            self.fdd.progressBar.setValue(0)

            username = dlg.loginLineEdit.text()
            password = dlg.passwordLineEdit.text()

            self.fetch_thread = AnimalFetchThread(self.animalIDsModel.listOfAnimalsIDs,
                                                  username, password)

            self.fetch_thread.set_progress_value.connect(self.fdd.setProgressValue)
            self.fetch_thread.animal_fetched.connect(self.animalFetched)
            self.fetch_thread.arimr_login_failed.connect(self.arimrLoginFailed)
            self.fetch_thread.animals_fetching_finished.connect(self.animalsFetchingFinished)
            self.fetch_thread.start()
            fdd_res = self.fdd.exec()
            # check if user clicked cancel button
            if not fdd_res:
                self.fetch_thread.requestInterruption()
            self.dataNeedSave = True
            self.saveDataPushButton.setEnabled(True)

    def animalsFetchingFinished(self, result):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)

        if result:
            msg.setText('Pobieranie danych o zwierzętach zakończone.')
            msg.setWindowTitle('Pobieranie zakończone.')
        else:
            msg.setText('Pobieranie danych o zwierzętach przerwane.')
            msg.setWindowTitle('Pobieranie przerwane.')
        msg.exec()

    def animalFetched(self, animal):
        self.arimrModel.addRow(animal)

    def arimrLoginFailed(self):
        self.showErrorMsgBox('Błąd logowania.', 'Wystąpił błąd logowania. Sprawdź poprawność danych logowania.')
        self.fdd.close()

    @pyqtSlot()
    def saveDataPushButton_on_click(self):
        self.saveData()


def main():
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

