from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtNetwork import *
import requests

from Data import dataProcessing
from imageP import imageProcessing
class VisualizerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Visualiseur")
        self.url = None
        self.get_url()
        self.show()

    def init_visualizor(self):
        self.data = dataProcessing()
        self.image = imageProcessing()
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
        #https://github.com/Tr0llope/Pile_RPL/blob/master/CalcUI.java
        #https://github.com/ianare/exif-samples/blob/master/jpg/Canon_40D.jpg
        #Error while reading Exif data: cannot identify image file <_io.BytesIO object at 0x7fe709223c90>


        response = requests.get(self.url)
        if response.status_code == 200:
            if self.image.isRemoteImg(self.url):
                self.file_info_label.setText(self.data.remote_file_info(self.url))
                self.text_edit.setPlainText(str(self.image.remoteExifdata(response)))
            else :
                self.file_info_label.setText(self.data.remote_file_info(self.url)) 
                self.text_edit.setText(self.data.remote_hexdump(self.url))
        else:
            print(response.status_code)
            self.file_info_label.setText("Failed to fetch the remote file.")

    def get_url(self):
        dialog = QInputDialog(self)
        if dialog.exec_():
            self.url = dialog.textValue()
        self.init_visualizor()

#Sources: https://www.geoffreybrown.com/blog/a-hexdump-program-in-python/