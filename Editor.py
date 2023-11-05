from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtNetwork import *
import datetime

from Data import dataProcessing
from imageP import imageProcessing
class EditorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Editeur")
        self.data = dataProcessing()
        self.image = imageProcessing()
        self.init_editor()
        self.show()

    def init_editor(self):
        self.setCentralWidget(QWidget(self))
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)
        self.setFixedSize(700, 900)

        #metadata
        self.file_info_label = QLabel()
        self.layout.addWidget(self.file_info_label) 

        #edit field
        self.text_edit = QTextEdit()
        self.central_widget.layout().addWidget(self.text_edit)

        #save button setup in edit mode
        self.button_save_file = QPushButton("Save")
        self.button_save_file.clicked.connect(self.save_file)

        options = QFileDialog.Options()
        file_dialog = QFileDialog(self, options=options)
        file_dialog.setWindowTitle('Open File')
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.setNameFilter('All Files (*)')
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                file_path = selected_files[0]
                if self.image.isImg(file_path):
                    self.file_info_label.setText(self.data.file_info(file_path))
                    self.text_edit.setText(str(self.image.exifdata(file_path)))
                else :
                    self.central_widget.layout().addWidget(self.button_save_file)
                    self.file_info_label.setText(self.data.file_info(file_path))                                   
                    self.text_edit.setPlainText(self.data.hexdump(file_path))
                    self.current_file_path = file_path

    def save_file(self):
        if self.current_file_path:
            bytes = self.data.reverse_hexdump(self.text_edit.toPlainText())
            try:
                with open(self.current_file_path, 'wb') as file:
                    file.write(bytes)
                print("File saved successfully.")
                self.successlabel = QLabel( datetime.datetime.now().strftime("%H:%M:%S : ") + "File saved successfully.")
                self.central_widget.layout().addWidget(self.successlabel)
            except Exception as e:
                print(f"An error occurred while saving the file: {str(e)}")
        else:
            print("No file path provided for saving.")
