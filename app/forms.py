from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField,PasswordField, BooleanField, SubmitField, FloatField,\
    TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, \
    Length
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class AddForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    hourly_pay = FloatField('hourly_pay', validators=[DataRequired()])
    hours_worked = FloatField('hours_worked', validators=[DataRequired()])
    allowance = FloatField('allowance', validators=[DataRequired()])
    deduction = FloatField('deduction', validators=[DataRequired()])
    submit = SubmitField('Add')

class UpdateForm(FlaskForm):
    id = IntegerField('id' ,validators=[DataRequired()])
    name = StringField('name')
    hourly_pay = FloatField('hourly_pay')
    hours_worked = FloatField('hours_worked')
    allowance = FloatField('allowance')
    deduction = FloatField('deduction')
    submit = SubmitField('Update')

class DeleteForm(FlaskForm):
    id = IntegerField('id' ,validators=[DataRequired()])
    submit = SubmitField('Delete')