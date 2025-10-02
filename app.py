import os
from flask import Flask, render_template, request, redirect, send_from_directory
from werkzeug.utils import secure_filename
from collections import Counter
import numpy as np
from PIL import Image

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_colors(image_path, num_colors=10):
    img = Image.open(image_path).convert('RGB')
    img = img.resize((200, 200))  # Resize for faster processing
    pixels = np.array(img).reshape(-1, 3)
    counts = Counter(map(tuple, pixels))
    total = sum(counts.values())

    # Sort by frequency descending
    most_common = counts.most_common(num_colors)
    results = []
    for color, count in most_common:
        hex_code = '#%02x%02x%02x' % color
        percentage = round((count / total) * 100, 2)
        results.append({"hex": hex_code, "percentage": percentage})
    return results

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            # Delete old files
            for old_file in os.listdir(app.config['UPLOAD_FOLDER']):
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], old_file))

            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            colors = get_colors(filepath)
            return render_template('result.html', colors=colors, filename=filename)
    return render_template('index.html')

# Serve uploaded files
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == "__main__":
    app.run(debug=True)