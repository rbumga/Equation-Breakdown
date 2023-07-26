from PyQt5.QtCore import *
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QMessageBox

try:
    from Classes.UI.MC_Response import MC_Response
    from Classes.UI.PreviewFrameMC import PreviewFrameMC
    from HelperScripts.RepeatableRandom import repeatable_random
    from wordprocessor.wordprocessor import MainWindow as RichTextMainWindow
except Exception as e:
    print(e)
import os


class MultipleChoiceUI(QtWidgets.QMainWindow):
    def __init__(self, parent):
        super(MultipleChoiceUI, self).__init__()
        self.parent = parent
        self.cwd = os.getcwd()
        uic.loadUi(self.cwd + "\\Classes\\UI\\MCAttributes.ui", self)
        self.setWindowTitle("Multiple Choice Construction")
        self.dictated_response_count_spinBox.valueChanged.connect(self.change_response_dictated)
        self.total_responses_count_spinBox.valueChanged.connect(self.change_response_total)
        self.submit_pushButton.clicked.connect(self.submit_button_action)
        self.mc_response_list = []
        self.response_frame_layout = QVBoxLayout()
        self.all_response_frame.setLayout(self.response_frame_layout)
        self.returned_html = None
        for i in range(self.dictated_response_count_spinBox.value()):
            new_mc_response = MC_Response(self.all_response_frame, i)
            self.mc_response_list.append(new_mc_response)
        self.show()
        self.edit_textEdit_pushButton.clicked.connect(self.open_text_editor)

        #     Testing language
        question_title = self.question_title_lineEdit.setText("1.1 Displacement of a car")
        question_text = self.question_text_textEdit.setPlainText("A car travels east along a straight road at a "
                                                                 "constant velocity of 18 m/s. After 5.0s, "
                                                                 "it accelerates uniformly for 4.0s, reaching a "
                                                                 "velocity of 24 m/s. For the next 6.0s, "
                                                                 "the car proceeds with uniform motion. Determine the "
                                                                 "car's displacement for the 15.0s trip.")
        first_mc_answer = self.mc_response_list[0].response_lineEdit.setText("320")


    def open_text_editor(self):
        self.question_text_textEdit.setEnabled(False)
        self.returned_html = None
        try:
            sent_html = self.question_text_textEdit.toHtml()
            new_rtmw = RichTextMainWindow(self, sent_html)
        except exception as e:
            print("Richtext Editor Exception: {}".format(e))

    def close_text_editor(self):
        if self.returned_html:
            self.question_text_textEdit.clear()
            self.question_text_textEdit.insertHtml(self.returned_html)
            self.returned_html = None
            self.question_text_textEdit.setEnabled(True)

    def change_response_dictated(self):
        self.clear_layout(self.all_response_frame.layout())
        dictated_response_count = int(self.dictated_response_count_spinBox.value())
        self.mc_response_list.clear()
        target_layout = self.all_response_frame.layout()
        for i in range(dictated_response_count):
            new_mc_response = MC_Response(self.all_response_frame, i)
            self.mc_response_list.append(new_mc_response)
        self.all_response_frame.setLayout(target_layout)
        total_response_value = self.total_responses_count_spinBox.value()
        if dictated_response_count >= total_response_value:
            self.total_responses_count_spinBox.setValue(dictated_response_count)

    def change_response_total(self):
        total_response_value = self.total_responses_count_spinBox.value()
        dictated_response_count = int(self.dictated_response_count_spinBox.value())
        if total_response_value < dictated_response_count:
            self.dictated_response_count_spinBox.setValue(self.total_responses_count_spinBox.value())

    def clear_layout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())

    def submit_button_action(self):
        new_MC_preview = None
        solution_unit = None
        solution_value = None
        question_title = self.question_title_lineEdit.text()
        question_text = self.question_text_textEdit.toPlainText()
        question_text_html = self.question_text_textEdit.toHtml()
        hint_text = self.hints_lineEdit.text()
        solution_text = self.solution_lineEdit.text()
        answer_lines = []
        answer_units = []
        for response in self.mc_response_list:
            answer_lines.append(response.response_lineEdit.text())
            answer_units.append(response.units_comboBox.currentText())

        none_answer_check = all(x in ["", None] for x in answer_lines)
        none_units_check = all(x in ["", None] for x in answer_units)
        none_check = all(x in ["", None] for x in [question_title, question_text])

        total_response_list_tuples = []
        total_response_count = self.total_responses_count_spinBox.value()
        question_hash_string = self.parent.get_hash_string() + " " + question_title
        whole_numbers = self.whole_number_checkBox.checkState()
        if whole_numbers == 2:
            whole_numbers = True
        else:
            whole_numbers = False
        variance_value = self.minimum_randomization_doubleSpinBox.value() * .01

        for i in range(len(self.mc_response_list)):
            total_response_list_tuples.append((self.mc_response_list[i].response_lineEdit.text(),
                                               self.mc_response_list[i].units_comboBox.currentText(),
                                               self.mc_response_list[i].feedback_lineEdit.text()))
            if i == 0:
                solution_unit = self.mc_response_list[i].units_comboBox.currentText()
                solution_value = self.mc_response_list[i].response_lineEdit.text()
            else:
                pass

        try_int_check = None
        try:
            solution_check = int(solution_value)
            if solution_value.isdigit():
                try_int_check = True
            else:
                try_int_check = False
        except Exception as e:
            try_int_check = False

        try_float_check = None
        try:
            float(solution_value)
            if solution_value.isdigit():
                try_float_check = False
            else:
                try_float_check = True
        except:
            try_float_check = False

        response_diff = total_response_count - len(self.mc_response_list)
        if response_diff >= 0 and (try_float_check or try_int_check):
            passed_solution_value = None
            if try_int_check:
                passed_solution_value = int(solution_value)
            else:
                passed_solution_value = float(solution_value)
            new_values = repeatable_random(question_hash_string, variance_value, passed_solution_value, response_diff,
                                           whole_numbers)
            for randomized_value in new_values:
                total_response_list_tuples.append((randomized_value, solution_unit, ""))

        elif response_diff >= 0 and not (try_float_check or try_int_check):
            message = QtWidgets.QMessageBox()
            message.setText("The format of the answer supplied did not support randomization. Please supply answers "
                            "up to the total response value.")
            message.setWindowTitle("Answers Not Supplied")
            message.setStandardButtons(QMessageBox.Ok)
            message.exec()
            return

        duplicate_check = (len(self.parent.built_questions_listWidget.findItems(question_title, Qt.MatchExactly)) >= 1)

        if not none_check and not none_answer_check and not none_units_check and not duplicate_check:
            new_mc_preview = PreviewFrameMC(self.parent.expanding_preview_frame, question_title,
                                            question_text_html, total_response_list_tuples, solution_value, solution_unit,
                                            hint_text, solution_text)
            self.parent.question_frame_dictionary[question_title] = new_mc_preview
            self.parent.built_questions_listWidget.addItem(question_title)
            self.parent.loading_window = None
            self.close()
        else:
            message = QtWidgets.QMessageBox()
            message_text = "There was an error submitting this MC question, please view your inputs and try again."
            if duplicate_check:
                message_text += "\n Your question duplicated another question's title."
            message.setText(message_text)
            message.setWindowTitle("Submission Error")
            message.setStandardButtons(QMessageBox.Ok)
            message.exec()

    def cancel_button_action(self):
        self.parent.loading_window = None
        self.close()
