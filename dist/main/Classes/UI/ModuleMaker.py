from PyQt5 import QtWidgets, uic
import os
from Classes.UI.MC_UI import MultipleChoiceUI
from PyQt5.QtWidgets import QMessageBox
from Classes.EquationLoader import EquationLoader


class ModuleMaker(QtWidgets.QMainWindow):
    def __init__(self):
        super(ModuleMaker, self).__init__()
        # new_RTMW = RichTextMainWindow()
        self.loading_window = None
        self.cwd = os.getcwd()
        self.equation_file_location = self.cwd + "\\Equation_Loader_Spreadsheet.csv"
        self.latex_image_dir = self.cwd + "\\local_equation_images"
        uic.loadUi(self.cwd + "\\Classes\\UI\\Builder.ui", self)
        self.equation_loader = EquationLoader(self.equation_file_location, self.latex_image_dir)
        self.setWindowTitle("Module Maker")
        self.method_dict = None
        self.question_frame_dictionary = {}
        self.show()
        self.lineEdits_list = [self.teacher_id_lineEdit, self.randomization_seed_lineEdit, self.assignment_id_lineEdit,
                               self.student_id_lineEdit]
        # link functions
        self.lock_pushButton.clicked.connect(self.lock_line_edits)
        self.multiple_choice_random_pushButton.clicked.connect(lambda: self.question_load('mc'))
        self.delete_selected_pushButton.clicked.connect(self.delete_selected)

    def delete_selected(self):
        delete_row = self.built_questions_listWidget.currentRow()
        current_item = self.built_questions_listWidget.currentItem()
        delete_text = None
        delete_item = None
        if current_item:
            delete_text = current_item.text()
        if delete_text:
            delete_item = self.question_frame_dictionary[delete_text]
        if delete_item:
            deleted_parent_layout = delete_item.parent.layout()
            deleted_parent_layout.removeWidget(delete_item.question_frame)
            delete_item.question_frame.deleteLater()
            del self.question_frame_dictionary[delete_text]
            self.built_questions_listWidget.takeItem(delete_row)

    def lock_line_edits(self):
        for lineEdits in self.lineEdits_list:
            lineEdits.setEnabled(not lineEdits.isEnabled())

    def load_mc_window(self):
        self.loading_window = MultipleChoiceUI(self)

    def question_load(self, q_type):
        if not self.method_dict and not self.loading_window:
            self.method_dict = {'mc': self.load_mc_window}
        self.method_dict[q_type]()

    def get_hash_string(self):
        hash_string = ""
        for lineEdit_object in self.lineEdits_list:
            building_string = lineEdit_object.text()
            if building_string == "":
                message = QtWidgets.QMessageBox()
                message.setText("One of the required elements for creating a repeatable randomization was empty.",
                                "\n Check the inputs on the main page and try again.")
                message.setWindowTitle("Hashing Error")
                message.setStandardButtons(QMessageBox.Ok)
                message.exec()
                return
            if hash_string == "":
                hash_string = building_string
            else:
                hash_string += " " + building_string
        if hash_string and hash_string != "":
            return hash_string
        else:
            message = QtWidgets.QMessageBox()
            message.setText("One or more of the required elements for creating a repeatable randomization was empty.",
                            "\n Check the inputs on the main page and try again.")
            message.setWindowTitle("Hashing Error")
            message.setStandardButtons(QMessageBox.Ok)
            message.exec()
            return
