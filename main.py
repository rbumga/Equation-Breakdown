from PyQt5 import QtWidgets, uic, QtGui
import sys
from Classes.UI.ModuleMaker import ModuleMaker

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ModuleMaker()
    window.setWindowTitle("Module Maker")
    app.exec_()


if __name__ == '__main__':
    main()