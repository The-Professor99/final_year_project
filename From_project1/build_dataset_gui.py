# from .build_face_dataset import start_capture
import sys
from pandas import DataFrame
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc



class MainWindow(qtw.QWidget):
    def __init__(self):
        """MainWindow constructor"""
        super().__init__()
        # main UI code goes here
        self.setWindowTitle("Class Attendance | Face Recognition")
        self.resize(600, 600)
        main_layout = qtw.QVBoxLayout()
        grid_layout = qtw.QGridLayout()
        
        tab_widget = qtw.QTabWidget()
        main_layout.addWidget(tab_widget)
        container = qtw.QWidget(self)
        container.setLayout(grid_layout)
        container2 = qtw.QWidget(self)
        container2.setLayout(main_layout)
        tab_widget.addTab(container, "Build Face Dataset")
        tab_widget.addTab(container2, "Main App")
        
#         self.student_form = qtw.QGroupBox("Student's Details")
#         self.capturebutton = qtw.QPushButton("Capture Face")
# #         setLayout(main_layout)
#         main_layout.addWidget(self.student_form)
#         main_layout.addWidget(self.capturebutton)
        
        form_layout = qtw.QFormLayout()
        self.student_form.setLayout(form_layout)
        self.course_code = qtw.QLineEdit(self, placeholderText="eg. EEE501", clearButtonEnabled=True, maxLength=6)
        self.surname = qtw.QLineEdit(self)
        self.first_name = qtw.QLineEdit(self)
        self.other_names = qtw.QLineEdit(self)
        self.mat_no = qtw.QLineEdit(self)
        self.email = qtw.QLineEdit(self)
        form_layout.addRow("Course Title", self.course_code)
        form_layout.addRow("Surname", self.surname)
        form_layout.addRow("First Name", self.first_name)
        form_layout.addRow("Other Names", self.other_names)
        form_layout.addRow("Matriculation Number", self.mat_no)
        form_layout.addRow("Email Address", self.email)
        
#         self.capturebutton.clicked.connect(self.capture_biometrics)
               
        # End of main UI code
        self.show()
        
    def capture_biometrics(self):
        student_surname = self.surname.text()
        student_first_name = self.first_name.text()
        student_other_names = self.other_names.text()
        course = self.course_code.text()
        matric_num = self.mat_no.text()
        email_add = self.email.text()
        name = student_surname + " " + student_first_name + " " + student_other_names
        if all([student_surname, student_first_name, student_other_names, matric_num]):
#             start_capture(name, matric_num)
            print(name, matric_num)
        else:
            print("Couldn't process, all fields not filled")
        
        
if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec())