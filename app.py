from flask import Flask,jsonify,request
import extractify as ext
from pdf2image import convert_from_path
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# To run python file without re-running the flask command
def before_request():
    app.jinja_env.cache = {}
app.before_request(before_request)

# Routes
@app.route('/')
def home():
    ext.load()
    return 'Dukh Dard Kasht Pidha'


@app.route('/api')
def api():
    ext.load()
    json = request.json
    return jsonify(ext.generate(json))
    
@app.route('/pdf_converter')
def pdftoimg():
    if(request.method == "POST"):
        pdf = request.FILES['pdf_name']
        with open('./static/tempfiles/temp.pdf', 'wb+') as destination:
            for chunk in pdf.chunks():
                destination.write(chunk)
        images = convert_from_path('./static/tempfiles/temp.pdf')
        for i in range(len(images)):
            # Save pages as images in the pdf
            images[i].save('./static/tempfiles/temp' +
                           str(i) + '.jpg', 'JPEG')
        return jsonify({'status': 'success'})
    return jsonify({'status': 'failure'})

# init
if __name__ == '__main__':
    app.run(debug=True)


