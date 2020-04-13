from flask import Flask, render_template, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms import IntegerField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap


app = Flask(__name__)
app.config['SECRET_KEY'] = 'jakis ciag znakow'
bootstrap = Bootstrap(app)


class NameForm(FlaskForm):
    option = IntegerField('Insert option: ', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        session['option'] = form.option.data
        if session['option'] is None:
            session['known'] = False
        else:
            session['known'] = True
        session['option'] = form.option.data
        return redirect(url_for('index'))
    return render_template(
            'index.html',
            form=form,
            option=session.get('option'), known=session.get('known', False)
            )


















