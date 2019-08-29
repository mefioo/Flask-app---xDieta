from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FloatField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange

class Registration(FlaskForm):
    username = StringField('Nazwa użytkownika', validators=[DataRequired(), Length(min=5, max=15)])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Hasło', validators=[DataRequired()])
    password_confirmation = PasswordField('Potwierdź hasło', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Zarejetruj')

class Login(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Hasło', validators=[DataRequired()])
    submit = SubmitField('Zaloguj')

class Data_edit(FlaskForm):
    name = StringField('Imię', validators=[Length(max=20)])
    surname = StringField('Nazwisko', validators=[Length(max=30)])
    age = FloatField('Wiek*', validators=[DataRequired(), NumberRange(min=1, max=110)])
    weight = FloatField('Waga*', validators=[DataRequired(), NumberRange(min=30, max=250)])
    height = FloatField('Wzrost*', validators=[DataRequired(), NumberRange(min=120, max=250)])
    sex = SelectField('Płeć*', choices=[('K', 'Kobieta'), ('M', 'Mężczyzna')])
    submit = SubmitField('Zmień dane')