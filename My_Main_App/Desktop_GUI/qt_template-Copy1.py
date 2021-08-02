import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc

class MainWindow(qtw.QWidget):
    def __init__(self):
        """MainWindow constructor"""
        super().__init__()
        # main UI code goes here
        self.setWindowTitle("Build Face Dataset")
        self.resize(600, 600)
        self.calendar = qtw.QCalendarWidget()
        self.event_list = qtw.QListWidget(toolTip="This is my widget")
        self.event_title = qtw.QLineEdit()
        self.event_category = qtw.QComboBox()
        self.event_time = qtw.QTimeEdit(qtc.QTime(8, 0))
        self.allday_check = qtw.QCheckBox("All Day")
        self.event_detail = qtw.QTextEdit()
        self.add_button = qtw.QPushButton("Add/Update")
        self.del_button = qtw.QPushButton("Delete")
        
        self.event_category.addItems(
            ["Select category...", "New...", "Work", "Meeting", "Doctor", "Family"]
        )
        self.event_category.model().item(0).setEnabled(False) # disables the first category

        main_layout = qtw.QHBoxLayout()
        self.setLayout(main_layout)
        main_layout.addWidget(self.calendar)
        
        self.calendar.setSizePolicy(
            qtw.QSizePolicy.Expanding,
            qtw.QSizePolicy.Expanding
        )
        
        right_layout = qtw.QVBoxLayout()
        main_layout.addLayout(right_layout)
        right_layout.addWidget(qtw.QLabel("Events on Date"))
        right_layout.addWidget(self.event_list)
        
        self.event_list.setSizePolicy(
            qtw.QSizePolicy.Expanding,
            qtw.QSizePolicy.Expanding
        )
        
        event_form = qtw.QGroupBox("Event")
        right_layout.addWidget(event_form)
        event_form_layout = qtw.QGridLayout()
        event_form.setLayout(event_form_layout)
        
        event_form_layout.addWidget(self.event_title, 1,1,1,3)
        event_form_layout.addWidget(self.event_category, 2, 1)
        event_form_layout.addWidget(self.event_time, 2, 2)
        event_form_layout.addWidget(self.allday_check, 2, 3)
        event_form_layout.addWidget(self.event_detail, 3, 1, 1, 3)
        event_form_layout.addWidget(self.add_button, 4, 2)
        event_form_layout.addWidget(self.del_button, 4, 3)
        
        # slots and signals
        self.quitbutton = qtw.QPushButton("Quit", clicked=self.close)
#         self.quitbutton.clicked.connect(self.close)
        self.layout().addWidget(self.quitbutton)
        self.entry1 = qtw.QLineEdit()
        self.entry2 = qtw.QLineEdit()
        self.layout().addWidget(self.entry1)
        self.layout().addWidget(self.entry2)
#         self.entry1.textChanged.connect(self.entry2.setText)
#         self.entry2.textChanged.connect(print)
        self.entry1.editingFinished.connect(lambda: print("Editing Finished"))
        self.entry2.returnPressed.connect(self.entry1.editingFinished)
        
        self.badbutton = qtw.QPushButton("Bad")
        self.layout().addWidget(self.badbutton)
        self.badbutton.clicked.connect(lambda: self.needs_args(1, 8, 2))
        
        
        # End of main UI code
        self.show()
        
if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec())