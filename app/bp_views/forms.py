from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, SelectField
from wtforms.validators import InputRequired


class EntryForm(FlaskForm):
    content = TextAreaField(
        'Content',
        [InputRequired('Entry content required.')]
    )
    submit = SubmitField('Submit')


class EntriesForm(FlaskForm):
    year = SelectField('Year')
    month = SelectField('Month')
    submit = SubmitField('Submit')