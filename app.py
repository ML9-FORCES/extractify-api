from flask import Flask,jsonify,request
import extractify as ext
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# To run python file without re-running the flask command
def before_request():
    app.jinja_env.cache = {}
app.before_request(before_request)


# Routes
@app.route('/api')
def api():
    ext.load()
    json = request.json
    return jsonify(ext.generate(json))

# init
if __name__ == '__main__':
    app.run(debug=True)


