from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtNetwork import *
import os, requests, json, imghdr
from io import BytesIO
from PIL import Image, ExifTags

class VisualizerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Visualiseur")
        self.url = None
        self.get_url()
        self.show()

    def init_visualizor(self):
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


        response = requests.get(self.url)
        if response.status_code == 200:
            if self.isImg(self.url):
                self.file_info_label.setText(self.remote_file_info(self.url))
                self.text_edit.setPlainText(str(self.exifdata(self.url)))
            else :
                self.file_info_label.setText(self.remote_file_info(self.url)) 
                print("Not an image")                                  
                self.text_edit.setText(self.remote_hexdump(self.url))
        else:
            self.file_info_label.setText("Failed to fetch the remote file.")


    def get_url(self):
        dialog = QInputDialog(self)
        if dialog.exec_():
            self.url = dialog.textValue()
        self.init_visualizor()
    
    def isImg(self,file_path):
        image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff', '.ico')
        url = self.url.lower()
        return any(url.endswith(ext) for ext in image_extensions)
    
    def exifdata(self, file_path):
        try:
            response = requests.get(file_path)
            response.raise_for_status()
            image = Image.open(BytesIO(response.content))
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

    def remote_file_info(self, file_url):
        response = requests.head(file_url)
        if response.status_code == 200:
            file_name = os.path.basename(file_url)
            file_size = response.headers.get('Content-Length')
            file_type = response.headers.get('Content-Type')
            file_permissions = response.headers.get('Allow')
            file_modified = response.headers.get('Last-Modified')
            file_info = f"File name: {file_name}\nFile path: {file_url}\nFile size: {file_size} bytes\nFile type: {file_type}\nFile permissions: {file_permissions}\nLast modified: {file_modified}"
            return file_info
        else:
            return "Failed to fetch the remote file."

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

    def remote_hexdump(self, url, bytes_per_line=16):
        try:
            session = requests.Session()
            session.headers.update({'User-Agent': 'Your User Agent'})  # Replace with your user agent

            # Send a GET request to get the content directly without HEAD request
            response = session.get(url, stream=True, headers={'Range': 'bytes=0-'})
            response.raise_for_status()  # Check for errors in the response

            offset = 0
            hexdump_text = ""

            for chunk in response.iter_content(chunk_size=bytes_per_line):
                hex_data = ' '.join(f'{byte:02X}' for byte in chunk)
                ascii_data = ''.join(chr(byte) if 32 <= byte < 127 else '.' for byte in chunk)
                hexdump_text += f'{offset:08X}: {hex_data.ljust(3 * bytes_per_line)}  {ascii_data}' + '\n'
                offset += len(chunk)

            return hexdump_text
        except requests.exceptions.RequestException as e:
            return f"Error: {e}"


#Sources: https://www.geoffreybrown.com/blog/a-hexdump-program-in-python/