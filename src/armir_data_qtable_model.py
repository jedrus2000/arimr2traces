# -*- coding: utf-8 -*-
from PyQt5.QtCore import QAbstractTableModel, Qt, QVariant, QModelIndex
from typing import List

from .animal import Animal
from .armir_data import save_report_file, save_traces_file

header = ['Nr stada', 'Nr identyfikatora', 'Status pobierania danych', 'Nr paszportu', 'Status paszportu',
          'Wiek (m)', 'Gatunek',
          'Plec', 'Rasa', 'Typ użytkowy', 'Status', 'Data urodzenia', 'Stan zdarzeń']


class ArmirDataModel(QAbstractTableModel):
    """
    Model of ARiMR data for QTable view

    """
    def __init__(self, parent=None):
        super(ArmirDataModel, self).__init__(parent)
        self.armir_data: List[Animal] = list()

    def resetModel(self):
        self.setData(list())

    def setData(self, armir_data):
        self.beginResetModel()
        self.armir_data = armir_data
        self.endResetModel()

    def addRow(self, animal):
        armir_data_count = len(self.armir_data)
        self.beginInsertRows(QModelIndex(), armir_data_count, armir_data_count)
        self.armir_data.append(animal)
        self.endInsertRows()
        # autoresize after first fow
        if armir_data_count == 0:
            self.parent().resizeColumnsToContents()

    def rowCount(self, parent):
        return len(self.armir_data)

    def columnCount(self, parent):
        return len(header)

    def data(self, index, role):
        if not index.isValid() or role != Qt.DisplayRole:
            return None

        # return qGray(self.modelImage.pixel(index.column(), index.row()))
        column = index.column()
        return self.animalDataAsList(index.row())[column]

    def animalDataAsList(self, row_id):
        animal = self.armir_data[row_id]
        return [animal.herd_id, animal.animal_id, animal.process_status, animal.passport_id,
                animal.passport_status,
                animal.age_in_months(), animal.species, animal.sex, animal.breed,
                animal.typ_uzyt, animal.status, animal.birth_date, animal.get_animal_events_states_text()]

    def headerData(self, section, orientation, role):
        #if role == Qt.SizeHintRole:
        #    return QSize(1, 1)

        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return QVariant(header[section])

        if role == Qt.DisplayRole and orientation == Qt.Vertical:
            return QVariant(str(section+1))

    def saveReportFile(self, file_name):
        save_report_file(file_name, self.armir_data)

    def saveTracesFile(self, file_name):
        save_traces_file(file_name, self.armir_data)
