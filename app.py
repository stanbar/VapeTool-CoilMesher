from flask import Flask, render_template, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, FloatField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap
from coil import normalcoil, serialize_geom


app = Flask(__name__)
app.config['SECRET_KEY'] = 'jakis ciag znakow'
bootstrap = Bootstrap(app)


class NameForm(FlaskForm):
    submit = SubmitField('Submit')


legsLength = 15
innerDiameter = 3.2
wireDiameter = 0.322
outerDiameter = 0.322
wraps = 5


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        print(serialize_geom(
            normalcoil(wraps, innerDiameter, wireDiameter, legsLength))
            )
        return redirect(url_for('index'))
    return render_template( 'index.html',
        form=form, known=session.get('known', False))
