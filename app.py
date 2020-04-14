from flask import Flask, render_template, redirect, url_for, send_file
from flask_wtf import FlaskForm
from wtforms import SubmitField
from flask_bootstrap import Bootstrap
from coil import normalcoil, serialize_geom, generate_mesh


app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
bootstrap = Bootstrap(app)


class NameForm(FlaskForm):
    submit = SubmitField('Submit')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


@app.route('/return-file/', methods=['GET'])
def returnFile():
    try:
        return send_file('coil.obj', attachment_filename='coil.obj')
    except:
        return render_template('404.html')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        generate_mesh(normalcoil(5, 3.2, 0.322, 15))
        return redirect(url_for('returnFile'))
        
    return render_template('index.html', form=form)
