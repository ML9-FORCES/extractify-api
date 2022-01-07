from flask import Flask,jsonify,request
import extractify as ext
from pdf2image import convert_from_path
from flask_cors import CORS
import base64

app = Flask(__name__)
CORS(app)

# To run python file without re-running the flask command
def before_request():
    app.jinja_env.cache = {}
app.before_request(before_request)

# Routes
@app.route('/api',methods = ['GET','POST'])
def api():
    if(request.method=="GET"):
        ext.load()
        json = request.json
        return jsonify(ext.generate(json))
        
    if(request.method=="POST"):   
        ext.load()
        json = request.json
        return jsonify(ext.generate(json))
    
@app.route('/pdf_converter',methods = ['POST'])
def pdftoimg():
    if(request.method == "POST"):
        pdf = request.files['pdf']
        with open('./static/tempfiles/temp.pdf', 'wb+') as destination:
            for chunk in pdf:
                destination.write(chunk)
        images = convert_from_path('./static/tempfiles/temp.pdf')
        for i in range(len(images)):
            # Save pages as images in the pdf
            images[i].save('./static/tempfiles/temp' +
                           str(i) + '.jpg', 'JPEG')
        with open("./static/tempfiles/temp0.jpg", "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
            return jsonify({'status': str(encoded_string.decode("utf-8"))})
    return jsonify({'status': 'failure'})

# init
if __name__ == '__main__':
    app.run(debug=True)


