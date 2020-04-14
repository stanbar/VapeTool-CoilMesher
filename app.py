from flask import Flask, redirect, url_for, send_file, request, Response
from coil import normalcoil, generate_mesh


app = Flask(__name__)


@app.errorhandler(404)
def page_not_found(e):
    return Response(status=404)


def returnFile():
    try:
        return send_file('coil.obj', attachment_filename='coil.obj')
    except:
        return response(status=500)


@app.route('/generate-mesh', methods=['GET', 'POST'])
def generateMesh():
    if not request.is_json:
        return Response(status=400)
    else:
        wraps = request.json.get('wraps')
        innerDiameter = request.json.get('innerDiameter')
        wireDiameter = request.json.get('wireDiameter')
        legsLength = request.json.get('legsLength')
        generate_mesh(normalcoil(wraps, innerDiameter, wireDiameter, legsLength))
        return returnFile()


@app.route('/', methods=['GET', 'POST'])
def index():
    return redirect(url_for('generateMesh'))
