from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class createTask(FlaskForm):
    taskName = StringField('Task Name',validators=[DataRequired, Length(min=3)])