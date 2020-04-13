from flask import Flask, render_template, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms import IntegerField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap
from coil import normalcoil


app = Flask(__name__)
app.config['SECRET_KEY'] = 'jakis ciag znakow'
bootstrap = Bootstrap(app)


class NameForm(FlaskForm):
    wrapsForm = IntegerField('Insert wraps: ', validators=[DataRequired()])
    innerDiameterForm = IntegerField('Insert inner diameter: ', validators=[DataRequired()])
    wireDiameterForm = IntegerField('Insert wire diameter: ', validators=[DataRequired()])
    legsLengthForm = IntegerField('Insert legs length: ', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        session['wrapsForm'] = form.wrapsForm.data
        session['innerDiameterForm'] = form.innerDiameterForm.data
        session['wireDiameterForm'] = form.wireDiameterForm.data
        session['legsLengthForm'] = form.legsLengthForm.data
        if session['wrapsForm'] is None:
            session['known'] = False
        else:
            session['known'] = True
        
        session['wrapsForm'] = form.wrapsForm.data
        session['innerDiameterForm'] = form.innerDiameterForm.data
        session['wireDiameterForm'] = form.wireDiameterForm.data
        session['legsLengthForm'] = form.legsLengthForm.data
        return redirect(url_for('index'))
    return render_template(
            'index.html',
            form=form,
            wrapsForm=session.get('wrapsForm'),
            innerDiameterForm=session.get('innerDiameterForm'), 
            wireDiameterForm=session.get('wireDiameterForm'), 
            legsLengthForm=session.get('legsLengthForm'), 
            known=session.get('known', False)
            )
