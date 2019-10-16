from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FloatField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange, Optional



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
    age = FloatField('Wiek*', validators=[DataRequired(), NumberRange(min=15, max=110)])
    weight = FloatField('Waga*', validators=[DataRequired(), NumberRange(min=30, max=250)])
    height = FloatField('Wzrost*', validators=[DataRequired(), NumberRange(min=120, max=250)])
    sex = SelectField('Płeć*', choices=[('K', 'Kobieta'), ('M', 'Mężczyzna')])
    working_routine = SelectField('Tryb pracy', choices=[('1', 'Brak ruchu'), ('2', 'Nieduża ilość ruchu'),
                                                         ('3', 'Średnia ilość ruchu'), ('4', 'Duża ilość ruchu'),
                                                         ('5', 'Praca w ciągłym ruchu')])
    submit = SubmitField('Zmień dane')


class Change_password(FlaskForm):
    old = PasswordField('Stare hasło', validators=[DataRequired()])
    new = PasswordField('Nowe hasło', validators=[DataRequired()])
    confirm = PasswordField('Potwierdź nowe hasło', validators=[DataRequired(), EqualTo('new')])
    submit = SubmitField('Zmień hasło')


class Add_activities(FlaskForm):
    name = SelectField('Nazwa aktywności', choices=[])
    time = FloatField('Ilość godzin w tygodniu', validators=[DataRequired(), NumberRange(min=1, max=100)])
    submit = SubmitField('Dodaj aktywność')


class Edit_activities(FlaskForm):
    name = SelectField('Nazwa aktywności', choices=[])
    time = FloatField('Ilość godzin w tygodniu*', validators=[Optional(), NumberRange(min=1, max=100)])
    submit = SubmitField('Edytuj aktywność')


class Add_diet(FlaskForm):
    submit = SubmitField('Dodaj dietę')


class Delete_diet(FlaskForm):
    id = SelectField('Numer diety*', choices=[])
    submit = SubmitField('Usuń dietę')


class Change_rights(FlaskForm):
    username = SelectField('Nazwa użytkownika', choices=[])
    rights = SelectField('Uprawnienia', choices=[('0', '0'), ('1', '1'), ('2', '2')])
    submit = SubmitField('Zmień uprawnienia')


class Delete_account(FlaskForm):
    username = SelectField('Nazwa użytkownika', choices=[])
    submit = SubmitField('Usuń konto')


class Add_activity_Admin(FlaskForm):
    name = StringField('Nazwa aktywności', validators=[DataRequired()])
    kcal = IntegerField('Kalorie spalane w trakcie godziny wysiłku', validators=[DataRequired(), NumberRange(min=10, max=2000)])
    submit = SubmitField('Dodaj aktywność')


class Change_password_Admin(FlaskForm):
    username = SelectField('Nazwa użytkownika', choices=[])
    password = PasswordField('Nowe hasło', validators=[DataRequired()])
    submit = SubmitField('Zmień hasło')


class Add_meal(FlaskForm):
    name = StringField('Nazwa posiłku', validators=[DataRequired()])
    submit = SubmitField('Dodaj posiłek')


class Add_product(FlaskForm):
    name = StringField('Nazwa produktu', validators=[DataRequired()])
    protein = IntegerField('Białko w 100g', validators=[NumberRange(min=0, max=100)])
    fats = IntegerField('Tłuszcze w 100g', validators=[NumberRange(min=0, max=100)])
    carbos = IntegerField('Węglowodany w 100g', validators=[NumberRange(min=0, max=100)])
    submit = SubmitField('Dodaj produkt')


class Add_product_to_meal(FlaskForm):
    name = SelectField('Nazwa posiłku, do którego zostaną dodane produkty', choices=[])
    ingredient = SelectField('Numer produktu', choices=[])
    weight = IntegerField('Waga produktu', validators=[NumberRange(min=1)])
    submit = SubmitField('Dodaj produkt do posiłku')


class Delete_meal(FlaskForm):
    name = SelectField('Nazwa posiłku', choices=[])
    submit = SubmitField('Usuń posiłek')


class Delete_ingredient(FlaskForm):
    name = SelectField('Nazwa produktu', choices=[])
    submit = SubmitField('Usuń produkt')
