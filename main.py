# First we will adjust your Flask application to handle image uploads and processing

from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from PIL import Image
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'product_image' not in request.files or 'logo_image' not in request.files:
            return redirect(request.url)

        product_image_file = request.files['product_image']
        logo_image_file = request.files['logo_image']

        if product_image_file.filename == '' or logo_image_file.filename == '':
            return redirect(request.url)

        if product_image_file and allowed_file(product_image_file.filename) and allowed_file(logo_image_file.filename):
            product_filename = secure_filename(product_image_file.filename)
            logo_filename = secure_filename(logo_image_file.filename)
            
            product_image_path = os.path.join(app.config['UPLOAD_FOLDER'], product_filename)
            logo_image_path = os.path.join(app.config['UPLOAD_FOLDER'], logo_filename)
            product_image_file.save(product_image_path)
            logo_image_file.save(logo_image_path)

            # Here you could redirect to a page where they can choose positioning, for this
            # example we will just add the logo to the top-left of the product image and serve it
            output_path = os.path.join(app.config['UPLOAD_FOLDER'], "merged_" + product_filename)
            merge_images(product_image_path, logo_image_path, output_path)
            return redirect(url_for('uploaded_file', filename="merged_" + product_filename))
    return render_template('upload.html')

# Function to merge images
def merge_images(canta_path, logo_path, output_path):
    canta = Image.open(canta_path)
    logo = Image.open(logo_path)
    logo.thumbnail((100, 100)) # You may want to make this dynamic or allow the user to set it.
    canta.paste(logo, (50, 50), logo) # For simplicity, pasting it at (50, 50)
    canta.save(output_path)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)


<!-- index.html -->
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>Ürününüz üzerine gelmesini istediğiniz logoyu yükleyiniz </title>
</head>
<body>
    <h2>Product Image Upload</h2>
    <form action="/upload" method="post" enctype="multipart/form-data">
        <label for="product_image">Ürününüz üzerine gelmesini istediğiniz logoyu yükleyiniz</label>
        <input type="file" name="product_image" accept="image/*"><br><br>
        <label for="logo_image">Ürününüz üzerine gelmesini istediğiniz logoyu yükleyiniz</label>
        <input type="file" name="logo_image" accept="image/*"><br><br>
        <input type="submit" value="Fotoğrafları yükleyiniz">
    </form>
</body>
</html>
          
          <!-- upload.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Logonuzu ürün Üzerinde Yerleştirin</title>
</head>
<body>
    <h2>Logonuzu ürün Üzerinde Yerleştirin</h2>
    <p>Lütfen logonuzu ürünün üzerinde gelmesini istediğiniz yere yerleştiriniz.</p>
    <!-- The code to allow logo placement by the user would go here -->
</body>
</html>
