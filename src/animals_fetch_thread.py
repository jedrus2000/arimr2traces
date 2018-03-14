# -*- coding: utf-8 -*-
from PyQt5.QtCore import QThread, pyqtSignal

from .arimr_data import *


class AnimalFetchThread(QThread):
    """
    QThread for retrieving data from website

    """
    animal_fetched = pyqtSignal("PyQt_PyObject", name='animalFetched')
    arimr_login_failed = pyqtSignal(name='arimrLoginFailed')
    animals_fetching_finished = pyqtSignal(bool, name='animalsFetchingFinished')
    set_progress_value = pyqtSignal(int, name='setProgressValue')

    def __init__(self, animal_ids_list, username, password):
        """
        Gets animal id's list, username and password to website

        :param animal_ids_list:
        :param username:
        :param password:
        """
        QThread.__init__(self)
        self.animal_ids_list = animal_ids_list
        self.username = username
        self.password = password

    def __del__(self):
        self.wait()

    def run(self):
        """
        launches website data extractor, logins and gets animal data one by one

        :return:
        """
        arimr_data_extractor = ArimrDataExtractor()
        if arimr_data_extractor.login(self.username, self.password):
            cnt = 0
            finish_result = True
            for animal in arimr_data_extractor.get_animals_from_ids_list(self.animal_ids_list):
                self.animal_fetched.emit(animal)
                cnt += 1
                self.set_progress_value.emit(cnt)
                self.sleep(2)
                if self.isInterruptionRequested():
                    finish_result = False
                    break
            self.animals_fetching_finished.emit(finish_result)
        else:
            self.arimr_login_failed.emit()
