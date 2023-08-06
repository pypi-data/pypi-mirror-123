#-------------------------------------------------------------------------------
# Name:        dialogs
# Author:      d.fathi
# Created:     20/03/2015
# Update:      02/10/2021
# Copyright:   (c) pyams 2021
# Web:         www.PyAMS.org
# Licence:     unlicense
#-------------------------------------------------------------------------------


from PyQt5 import QtCore, QtGui, QtWidgets
from collections import deque
import os




#-------------------------------------------------------------------------------
# class Ui_DialogImportPart: intrface of dialog for import symbols.
#-------------------------------------------------------------------------------

class Ui_DialogImportPart(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(396, 389)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.treeView = QtWidgets.QTreeView(Dialog)
        self.treeView.setObjectName("treeView")
        self.verticalLayout.addWidget(self.treeView)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.listView = QtWidgets.QListView(Dialog)
        self.listView.setObjectName("listView")
        self.verticalLayout_2.addWidget(self.listView)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Directory"))
        self.label_2.setText(_translate("Dialog", "Symbols"))


#-------------------------------------------------------------------------------
# class dialogImportPart:  dialog for import symbols.
#-------------------------------------------------------------------------------

class dialogImportPart:
    def __init__(self):
        self.w = QtWidgets.QDialog()

        self.pathLib='';

        self.ui = Ui_DialogImportPart()
        self.ui.setupUi(self.w)
        self.dirModel = QtWidgets.QFileSystemModel()
        self.dirModel.setRootPath(QtCore.QDir.rootPath())
        self.dirModel.setFilter(QtCore.QDir.NoDotAndDotDot | QtCore.QDir.AllDirs)

        self.fileModel = QtWidgets.QFileSystemModel()
        self.fileModel.setNameFilters(["*.sym"])
        self.fileModel.setNameFilterDisables(False)

        self.ui.treeView.setModel(self.dirModel)
        self.ui.listView.setModel(self.fileModel)

        self.ui.treeView.clicked.connect(self.treeClicked)
        self.ui.listView.clicked.connect(self.listClicked)

        self.ui.treeView.hideColumn(1)
        self.ui.treeView.hideColumn(2)
        self.ui.treeView.hideColumn(3)
        self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False);



    def setPath(self,path):
        self.ui.treeView.setRootIndex(self.dirModel.index(path))
        self.ui.listView.setRootIndex(self.fileModel.index(path))

    def treeClicked(self, index):
        path = self.dirModel.fileInfo(index).absoluteFilePath()
        self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False);
        self.ui.listView.setRootIndex(self.fileModel.setRootPath(path))

    def listClicked(self, index):
        path = self.fileModel.fileInfo(index).absoluteFilePath()
        self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False);
        if path!='':
            root, ext = os.path.splitext(path)
            if(ext=='.sym'):
                self.file=path;
                self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(True);

    def show(self):
        self.w.show()




#-------------------------------------------------------------------------------
# class Ui_DialogListSignalsParamaters: intrface of dialog List of Signals
#                                         &Paramaters.
#-------------------------------------------------------------------------------

class Ui_DialogListSignalsParamaters(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(449, 510)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.treeView = QtWidgets.QTreeView(Dialog)
        self.treeView.setObjectName("treeView")
        self.verticalLayout.addWidget(self.treeView)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))

def getImage(value):
    if value['type']=='paramater':
        return ":image/paramsignals/param.png"
    elif (value['type']=='signal')and (value['description']=='voltage')and (value['dir']=='out'):
         return ":image/paramsignals/vout.png"
    elif (value['type']=='signal')and (value['description']=='voltage')and (value['dir']=='in'):
         return ":image/paramsignals/vin.png"
    elif (value['type']=='signal')and (value['dir']=='out'):
         return ":image/paramsignals/iout.png"
    elif (value['type']=='signal')and (value['dir']=='in'):
         return ":image/paramsignals/iin.png"

#-------------------------------------------------------------------------------
# class dialogListSignalsParamaters:  dialog List of Signals
#                                         & Paramaters.
#-------------------------------------------------------------------------------
class dialogListSignalsParamaters:
    def __init__(self,data):
        self.w = QtWidgets.QDialog()

        self.path='';
        self.pathLib='';

        self.ui = Ui_DialogListSignalsParamaters()
        self.ui.setupUi(self.w)
        self.model = QtGui.QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['Name'])#, 'Type', 'Description'
      #  self.model.resizeSection(0, 42);
        self.ui.treeView.setModel(self.model)
        self.ui.treeView.header().resizeSection(0, 150);#setStyleSheet("QTreeView::item { width: 100px }")
        self.ui.treeView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.ui.treeView.clicked.connect(self.treeClicked)
        self.importData(data)
        self.ui.treeView.expandAll()
        self.pos='None'
        self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False);

    def treeClicked(self, index):
        row=index.row()
        column=index.column()
        data=index.data()
        if len(data.split('.'))>1:
           self.pos=data
           self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(True);
        else:
           self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False);

    def importData(self, data, root=None):
        self.model.setRowCount(0)
        if root is None:
            root = self.model.invisibleRootItem()
        seen = {}   # List of  QStandardItem
        values = deque(data)
        while values:
            value = values.popleft()
            if value['unique_id'] == 1:
                parent = root
            else:
                pid = value['parent_id']
                if pid not in seen:
                    values.append(value)
                    continue
                parent = seen[pid]
            unique_id = value['unique_id']
            parent.appendRow([
                QtGui.QStandardItem(QtGui.QIcon(getImage(value)),value['short_name'])
               # QStandardItem(value['type']),
               # QStandardItem(value['description'])
            ])
            seen[unique_id] = parent.child(parent.rowCount() - 1)
            #seen[unique_id].QStandardItem(QIcon("4.bmp"))

    def show(self):
        self.w.show()


#-------------------------------------------------------------------------------
# __main__: test Dialog
#-------------------------------------------------------------------------------
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dialog = dialogImportPart()
    dialog.show()
    sys.exit(app.exec_())
