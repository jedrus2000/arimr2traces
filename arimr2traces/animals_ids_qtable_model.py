# -*- coding: utf-8 -*-
from PyQt5.QtCore import QAbstractTableModel, Qt, QVariant


class AnimalIDsModel(QAbstractTableModel):
    """
    Model of IDs for IDs Table View

    """
    def __init__(self, parent=None):
        super(AnimalIDsModel, self).__init__(parent)
        self.listOfAnimalsIDs = list()

    def setData(self, animals_ids_list):
        self.beginResetModel()
        self.listOfAnimalsIDs = animals_ids_list
        self.endResetModel()

    def rowCount(self, parent):
        return len(self.listOfAnimalsIDs)

    def columnCount(self, parent):
        return 1

    def data(self, index, role):
        if not index.isValid() or role != Qt.DisplayRole:
            return None

        # return qGray(self.modelImage.pixel(index.column(), index.row()))
        return self.listOfAnimalsIDs[index.row()]

    def headerData(self, section, orientation, role):
        #if role == Qt.SizeHintRole:
        #    return QSize(1, 1)

        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return QVariant("Nr id.")

        if role == Qt.DisplayRole and orientation == Qt.Vertical:
            return QVariant(str(section+1))


