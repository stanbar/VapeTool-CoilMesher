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
    wrapsForm = IntegerField('Insert wraps: (5)', validators=[DataRequired()])
    innerDiameterForm = FloatField('Insert inner diameter: (3.2)', validators=[DataRequired()])
    wireDiameterForm = FloatField('Insert wire diameter: (0.322)', validators=[DataRequired()])
    legsLengthForm = IntegerField('Insert legs length: (15)', validators=[DataRequired()])
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
        
        print(serialize_geom(
            normalcoil(form.wrapsForm.data,
						form.innerDiameterForm.data,
						form.wireDiameterForm.data,
						form.legsLengthForm.data
					    )
					)
				)
        """
        session['normalcoilResult'] = normalcoil(form.wrapsForm.data,
										form.innerDiameterForm.data,
										form.wireDiameterForm.data,
										form.legsLengthForm.data
										)
        """
        return redirect(url_for('index'))
    return render_template(
            'index.html',
            form=form,
            wrapsForm=session.get('wrapsForm'),
            innerDiameterForm=session.get('innerDiameterForm'), 
            wireDiameterForm=session.get('wireDiameterForm'), 
            legsLengthForm=session.get('legsLengthForm'), 
            normalcoilResult=session.get('normalcoilResult'),
            known=session.get('known', False)
            )
