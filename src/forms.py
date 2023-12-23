from flask import request
from flask_wtf import FlaskForm
from wtforms import TextAreaField, BooleanField
from wtforms.validators import Length

class NewMemoryForm(FlaskForm):
    prompt = TextAreaField('Prompt', validators=[Length(min=1)])
    answer = TextAreaField('Answer', validators=[Length(min=1)])
    training_status = BooleanField('Training Status', default=True)