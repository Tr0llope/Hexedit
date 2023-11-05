import os, stat, datetime, requests

# Contient les fonctions de transformation et récupération de données
class dataProcessing(object):
    # Récupère les metadata du fichier
    def file_info(self, file_path):
        try:
            file_stat = os.stat(file_path)
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

    # Récupère les metadata d'un fichier distant
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

    # Retourne le contenu d'un fichier en hexadécimal
    def hexdump(self, file_path):
            with open(file_path, 'rb') as file:
                offset = 0
                hexdump_text = ""
                while True:
                    data = file.read(16)
                    if not data:
                        break
                    hex_data = ' '.join(f'{byte:02X}' for byte in data)
                    ascii_data = ''.join(chr(byte) if 32 <= byte < 127 else '.' for byte in data)
                    hexdump_text += f'{offset:08X}: {hex_data.ljust(3 * 16)}  {ascii_data}' + '\n'
                    offset += 16
            return hexdump_text
        
    # Retourne le contenu du fichier édité en bytes
    def reverse_hexdump(self, hexdump_text):
            binary_data = bytearray()
            lines = hexdump_text.split('\n')
            for line in lines:
                parts = line.split(':')
                if len(parts) > 1:
                    hex_data = parts[1].split()
                    for hex_byte in hex_data:
                        try:
                            byte_value = int(hex_byte, 16)
                            binary_data.append(byte_value)
                        except ValueError:
                            pass
            return bytes(binary_data)

    # Retourne le contenu d'un fichier distant en héxadécimal
    def remote_hexdump(self, url):
        try:
            session = requests.Session()
            session.headers.update({'User-Agent': 'Your User Agent'})
            response = session.get(url, stream=True, headers={'Range': 'bytes=0-'})
            response.raise_for_status()

            offset = 0
            hexdump_text = ""

            for chunk in response.iter_content(chunk_size=16):
                hex_data = ' '.join(f'{byte:02X}' for byte in chunk)
                ascii_data = ''.join(chr(byte) if 32 <= byte < 127 else '.' for byte in chunk)
                hexdump_text += f'{offset:08X}: {hex_data.ljust(3 * 16)}  {ascii_data}' + '\n'
                offset += len(chunk)

            return hexdump_text
        except requests.exceptions.RequestException as e:
            return f"Error: {e}"
