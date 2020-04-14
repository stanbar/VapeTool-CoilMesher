from flask import Flask, render_template, redirect, url_for, send_file, request
from coil import normalcoil, serialize_geom, generate_mesh


app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'


@app.errorhandler(404)
def page_not_found(e):
    return "page not found\n"


@app.route('/return-file/', methods=['GET'])
def returnFile():
    try:
        return send_file('coil.obj', attachment_filename='coil.obj')
    except:
        return "error return-file\n"


@app.route('/generate-mesh', methods=['GET', 'POST'])
def generateMesh():
    if not request.is_json:
        return "false\n"
    else:
        wraps = request.json.get('wraps')
        innerDiameter = request.json.get('innerDiameter')
        wireDiameter = request.json.get('wireDiameter')
        legsLength = request.json.get('legsLength')
        
        return "JSON ok\n"


@app.route('/', methods=['GET', 'POST'])
def index():
    #generate_mesh(normalcoil(5, 3.2, 0.322, 15))
    return redirect(url_for('generateMesh'))
