import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from designer_app import Ui_MainWindow
from dialog import Ui_SettingsDialog
from build_face_dataset import start_capture

class SettingsDialog(qtw.QDialog, Ui_SettingsDialog):
    """Dialog for setting the settings"""
    def __init__(self, settings, parent=None):
        super().__init__(parent, modal=True)
        self.setupUi(self)
#         self.setLayout(qtw.QFormLayout())
        self.settings = settings
#         self.layout().addRow(
#             qtw.QLabel("<h1>Application Settings</h1>"),
#         )

        self.show_warnings_cb.setChecked(settings.value("show_warnings", False, type=bool))
        self.prototxt_file.setText(settings.value("prototxt_file", "constants/deploy.prototxt.txt", type=str))
        self.model_file.setText(settings.value("model_file", "constants/res10_300x300_ssd_iter_140000.caffemodel", type=str))
        self.output_folder.setText(settings.value("output_folder", "changes/datasets", type=str))
        self.confidence_1.setValue(settings.value("confidence_1", 0.80, type=float))
        self.confidence_2.setValue(settings.value("confidence_2", 0.80, type=float))
    
        self.pushButton_ptf.clicked.connect(lambda: self.openFile(self.prototxt_file))
        self.pushButton_mf.clicked.connect(lambda: self.openFile(self.model_file))
        self.pushButton_opf.clicked.connect(lambda: self.openFile(self.output_folder, typ="folder"))
        self.pushButton_reset.clicked.connect(self.reset)
        
    def accept(self):
        self.settings.setValue(
            "show_warnings",
            self.show_warnings_cb.isChecked()
        )
        self.settings.setValue(
            "prototxt_file",
            self.prototxt_file.text()
        )
        self.settings.setValue(
            "model_file",
            self.model_file.text()
        )
        self.settings.setValue(
            "output_folder",
            self.output_folder.text()
        )
        self.settings.setValue(
            "confidence_1",
            self.confidence_1.value()
        )
        self.settings.setValue(
            "confidence_2",
            self.confidence_2.value()
        )
#         self.settings["show_warnings"] = self.show_warnings_cb.isChecked()
        super().accept()
    
    def reset(self):
        self.prototxt_file.setText("constants/deploy.prototxt.txt")
        self.model_file.setText("constants/res10_300x300_ssd_iter_140000.caffemodel")
        self.output_folder.setText("changes/datasets")
        self.confidence_1.setProperty("value", 0.8)
        self.confidence_2.setProperty("value", 0.8)
#         self.accept()
#         self.settings.setValue(
#             "prototxt_file",
#             self.prototxt_file.text()
#         )
#         self.settings.setValue(
#             "model_file",
#             self.model_file.text()
#         )
#         self.settings.setValue(
#             "output_folder",
#             self.output_folder.text()
#         )
#         self.settings["show_warnings"] = self.show_warnings_cb.isChecked()
#         super().accept()
    
    def openFile(self, file_returned, typ="file"):
        if typ == "file":
            filename, _ = qtw.QFileDialog.getOpenFileName(
                self,
                "Select a text file to open...",
                qtc.QDir.homePath(),
                "Text Files (*.txt) ;;Python Files (*.py) ;;All Files (*)",
                "Python Files (*.py)",
    #             qtw.QFileDialog.DontUseNativeDialog | qtw.QFileDialog.DontResolveSymlinks
            )
        else:
            filename = qtw.QFileDialog.getExistingDirectory(self, "Select Folder")
        if filename:
            try:
#                 with open(filename, "r") as fh:
#                     self.textedit.setText(fh.read())
                file_returned.setText(filename)
            except Exception as e:
                qtw.QMessageBox.critical(f"Could not load File: {e}")

class MainWindow(qtw.QMainWindow, Ui_MainWindow):
    settings = qtc.QSettings("Ihechi Festus000001", "Class Attendance | Face Recognition")
    def __init__(self):
        """MainWindow constructor"""
        super().__init__()
        self.setupUi(self)
        # Main UI code goes here
        #Icons#
        start_recognitionIcon = self.style().standardIcon(qtw.QStyle.SP_MediaPlay)
        settingsIcon = self.style().standardIcon(qtw.QStyle.SP_DialogHelpButton)
        self.actionSettings.setIcon(settingsIcon)
        self.actionStart_Recognition.setIcon(start_recognitionIcon)
        
        
        self.toolBar.addAction(self.actionStart_Recognition)
        self.toolBar.addAction(self.actionSettings)
        
        self.actionStart_Recognition.triggered.connect(self.start_recognition)
        self.actionSettings.triggered.connect(self.show_settings)
        self.capture_button.clicked.connect(self.capture_biometrics)
        
        if self.settings.value("show_warnings", True, type=bool):
            print("Yeah, workings")
            print(self.settings.value("prototxt_file"))
        # End main UI code
        self.show()
        
            
    def capture_biometrics(self):
        prototxt_file = self.settings.value("prototxt_file", "constants/deploy.prototxt.txt", type=str)
        model_file = self.settings.value("model_file", "constants/res10_300x300_ssd_iter_140000.caffemodel", type=str)
        output_folder = self.settings.value("output_folder", "changes/datasets", type=str)
        confidence_1 = self.settings.value("confidence_1", 0.8, type=float)
        
        student_surname = self.surname.text()
        student_first_name = self.first_name.text()
        student_other_names = self.other_names.text()
        course = self.course_code.text()
        matric_num = self.mat_no.text()
        email_add = self.email.text()
        name = student_surname + " " + student_first_name + " " + student_other_names
        if all([student_surname, student_first_name, student_other_names, matric_num]):
            start_capture(name, matric_num, prototxt_file, model_file, output_folder, confidence_1)
            print(name, matric_num)
        else:
            print("Couldn't process, all fields not filled")
            
        
    def show_settings(self):
        settings_dialog = SettingsDialog(self.settings, self)
        settings_dialog.exec()
        
    def start_recognition(self):
        self.statusBar().showMessage("Recognition Started!!!")
        
    
if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec())