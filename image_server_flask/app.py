from flask import Flask, request, send_from_directory, url_for, make_response, send_file
from urllib.parse import urlparse, urlunparse
from PIL import Image
import io
import os
import uuid
import environ
import logging


env = environ.Env()

app = Flask(__name__)
IMAGE_STORAGE = 'images'


def modify_url_hostname(url, new_hostname):
    """
    This function takes a URL and a new hostname as input.
    It replaces the original hostname in the given URL with the new hostname and returns the modified URL.
    """
    parsed_url = urlparse(url)
    modified_url = parsed_url._replace(netloc=new_hostname)
    return urlunparse(modified_url)


@app.route('/upload', methods=['POST'])
def upload_image():
    """
    This function handles the image upload process. It checks if a file is provided in the request,
    saves the file with a unique name, and returns the URL of the saved image with the modified hostname.
    """
    if 'file' not in request.files:
        return 'No file part', 400

    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400

    if file:
        ext = file.filename.split('.')[-1]
        filename = f"{uuid.uuid4()}.{ext}"
        os.makedirs(IMAGE_STORAGE, exist_ok=True)
        file.save(os.path.join(IMAGE_STORAGE, filename))
        image_url = url_for('serve_image', filename=filename, _external=True)
        modified_image_url = modify_url_hostname(image_url, env('LOCAL_HOST'))
        return {'url': modified_image_url}


@app.route('/images/<path:filename>')
def serve_image(filename):
    """
    This function serves the image file with the given filename. If width and height are provided as query parameters,
    it resizes the image while preserving its aspect ratio and adds transparent padding to match the requested dimensions.
    It returns the modified image or the original image as a response.
    """
    width = request.args.get('w', type=int)
    height = request.args.get('h', type=int)

    ext = filename.split('.')[-1].lower()
    mimetype_map = {'jpg': 'image/jpeg', 'jpeg': 'image/jpeg', 'png': 'image/png'}

    if width and height:
        try:
            image_path = os.path.join(IMAGE_STORAGE, filename)
            with Image.open(image_path) as img:
                # Calculate the new size while preserving the aspect ratio
                aspect_ratio = float(img.width) / float(img.height)
                new_width = width
                new_height = int(width / aspect_ratio)

                if new_height > height:
                    new_width = int(height * aspect_ratio)
                    new_height = height

                img = img.resize((new_width, new_height), Image.ANTIALIAS)

                # Create a new image with the desired dimensions and a solid background color
                new_img = Image.new('RGBA', (width, height), (0, 0, 0, 0))

                # Paste the resized image onto the new image at the center
                paste_x = (width - img.width) // 2
                paste_y = (height - img.height) // 2
                new_img.paste(img, (paste_x, paste_y))

                # Convert image to RGB mode if it's in RGBA mode
                if new_img.mode == 'RGBA':
                    new_img = new_img.convert('RGB')

                img_io = io.BytesIO()
                new_img.save(img_io, format=ext.upper(), quality=85)
                img_io.seek(0)
                response = make_response(send_file(img_io, mimetype=mimetype_map[f'{ext}']))
        except Exception as e:
            app.logger.exception(f"Error resizing image: {e}")
            return "Error resizing image", 500
    else:
        response = send_from_directory(IMAGE_STORAGE, filename)

    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=env.bool('DEBUG', default=False))
