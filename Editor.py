from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtNetwork import *
import os, stat, sys, datetime, requests, json
from PIL import Image, ExifTags

class EditorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Editeur")
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
                if self.isImg(file_path):
                    self.file_info_label.setText(self.file_info(file_path))
                    self.text_edit.setText(str(self.exifdata(file_path)))
                else :
                    self.central_widget.layout().addWidget(self.button_save_file)
                    self.file_info_label.setText(self.file_info(file_path))                                   
                    self.text_edit.setPlainText(self.hexdump(file_path))
                    self.current_file_path = file_path

    def isImg(self,file_path):
        try:
            Image.open(file_path)
        except IOError:
            return False
        return True
    
    def exifdata(self, file_path):
        try:
            with Image.open(file_path) as image:
                exif_info = image._getexif()

                if exif_info:
                    exif_data = {}
                    for tag, value in exif_info.items():
                        tag_name = ExifTags.TAGS.get(tag, tag)
                        exif_data[tag_name] = value

                    exif_json = json.dumps(exif_data, default=str, indent=4)
                    with open('export.json', 'w') as export_file:
                        export_file.write(exif_json)

                    return exif_data
                else:
                    return "No Exif data found in the image."
        except (IOError, AttributeError, KeyError) as e:
            return f"Error while reading Exif data: {str(e)}"

    def file_info(self, file_path):
        try:
            # Get file statistics
            file_stat = os.stat(file_path)

            # Extract information from file_stat
            file_name = os.path.basename(file_path)
            file_size = file_stat.st_size
            file_permissions = stat.filemode(file_stat.st_mode)
            access_time = datetime.datetime.fromtimestamp(file_stat.st_atime)
            modification_time = datetime.datetime.fromtimestamp(file_stat.st_mtime)

            info = f"File Name: {file_name}\n"
            info += f"File Path: {file_path}\n"
            info += f"File Size: {file_size} bytes\n"
            info += f"File Permissions: {file_permissions}\n"
            info += f"Last Access Time: {access_time}\n"
            info += f"Last Modification Time: {modification_time}\n"
            return info

        except FileNotFoundError:
            print("File not found.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def hexdump(self, file_path, bytes_per_line=16):
        with open(file_path, 'rb') as file:
            offset = 0
            hexdump_text = ""
            while True:
                data = file.read(bytes_per_line)
                if not data:
                    break
                hex_data = ' '.join(f'{byte:02X}' for byte in data)
                ascii_data = ''.join(chr(byte) if 32 <= byte < 127 else '.' for byte in data)
                hexdump_text += f'{offset:08X}: {hex_data.ljust(3 * bytes_per_line)}  {ascii_data}' + '\n'
                offset += bytes_per_line
        return hexdump_text

    def reverse_hexdump(self, hexdump_text):
        binary_data = bytearray()
        lines = hexdump_text.split('\n')
        for line in lines:
            # Split the line into sections, excluding the offset part
            parts = line.split(':')
            if len(parts) > 1:
                hex_data = parts[1].split()
                for hex_byte in hex_data:
                    try:
                        byte_value = int(hex_byte, 16)
                        binary_data.append(byte_value)
                    except ValueError:
                        # Handle non-hex characters, such as comments
                        pass
        return bytes(binary_data)


    def save_file(self):
        if self.current_file_path:
            bytes = self.reverse_hexdump(self.text_edit.toPlainText())
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
