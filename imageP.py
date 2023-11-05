
import imghdr, json, requests
from io import BytesIO
from PIL import Image, ExifTags

# Contient les fonctions d'identification des images et de récupération des données exif en local et à distance
class imageProcessing():
    def isImg(self,file_path):
        try:
            Image.open(file_path)
        except IOError:
            return False
        return True
 
    def isRemoteImg(self,url):
        try:
            response = requests.head(url)
            if response.status_code == 200:
                content_type = response.headers.get('Content-Type')
                if content_type and content_type.startswith('image/'):
                    return True
                response = requests.get(url)
                if response.status_code == 200:
                    image_data = response.content
                    image_format = imghdr.what(None, h=image_data)
                    if image_format:
                        print(f"Image format detected as {image_format} based on the response content.")
                        return True
        except requests.exceptions.RequestException:
            pass
        print("The URL does not point to a valid image.")
        return False
 
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
        
    def remoteExifdata(self,response):
        try:
            response.raise_for_status()
            image = Image.open(BytesIO(response.content))
            if hasattr(image, '_getexif'):
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
            else:
                return "Exif data not found in the image."
        except requests.exceptions.RequestException as e:
            return f"Error while making the request: {str(e)}"
        except (IOError, AttributeError, KeyError, Exception) as e:
            return f"Error while reading Exif data: {str(e)}"
