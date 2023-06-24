from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField
from wtforms.validators import InputRequired, EqualTo


class RegistrationForm(FlaskForm):
    username = StringField(
        'Username',
        [InputRequired('Please choose a username')]
    )
    password = PasswordField(
        'Password', [
            InputRequired('Please choose a password'),
            EqualTo('confirm', message='Passwords must match')
        ]
    )
    confirm = PasswordField(
        'Confirm Password',
        [InputRequired('Confirm password')]
    )
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    username = StringField(
        'Username',
        [InputRequired('Please enter your username')]
    )
    password = PasswordField(
        'Password',
        [InputRequired('Please enter your password')]
    )
    submit = SubmitField('Login')
    next = HiddenField()