from flask import Flask, request, send_file
from flask_cors import CORS, cross_origin
from PIL import Image, PngImagePlugin
import io
import json
import base64

app = Flask(__name__)
CORS(app)  # This enables CORS for all domains and routes. For production, restrict this appropriately.

@app.route('/upload', methods=['POST'])
@cross_origin()  # This decorator enables CORS specifically for this route if needed.
def upload_image():
    try:
        file = request.files['image']
        metadata = request.form.get('metadata', '{}')
        metadata = json.loads(metadata)

        image = Image.open(file.stream)
        encrypted_metadata = base64.b64encode(json.dumps(metadata).encode()).decode()

        info = PngImagePlugin.PngInfo()
        info.add_text('metadata', encrypted_metadata)
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG', pnginfo=info)
        img_byte_arr.seek(0)

        return send_file(img_byte_arr, mimetype='image/png')
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
