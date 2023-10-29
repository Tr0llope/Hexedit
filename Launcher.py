import sys
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtNetwork import *
from Editor import EditorWindow
from Visualizer import VisualizerWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Menu principal")
        self.setFixedSize(700, 1000)
        self.init_menu()
        self.init_toolbar()

        #toolbar
    def init_toolbar(self):
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        edit_action = QAction('Edit', self)
        visualize_action = QAction('Visualize', self)
        toolbar.addAction(edit_action)
        toolbar.addAction(visualize_action)
        #link toolbar to functions
        edit_action.triggered.connect(self.edit_file)
        visualize_action.triggered.connect(self.visualize_file)

    def init_menu(self):
        self.setCentralWidget(QWidget(self))
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        
        
        self.logo = QPixmap("doc/hexedit.png")
        self.logo = self.logo.scaledToWidth(600)

        self.logo_label = QLabel()
        self.logo_label.setPixmap(self.logo)
        self.logo_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.layout.addWidget(self.logo_label)
        self.logo_label.setAlignment(Qt.AlignCenter)

    def edit_file(self):
        self.second_window = EditorWindow()
        self.second_window.show()

    def visualize_file(self):
        self.third_window = VisualizerWindow()
        self.third_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.setStyleSheet("background-color: #FFFFFF;")
    main_window.show()
    sys.exit(app.exec())
