from flask import render_template, url_for, flash, redirect, session
from app.forms import Registration, Login, Data_edit
from app import app
from app.database_connection import MySQLfind, MySQLinsert
from datetime import timedelta

from functools import wraps


find = MySQLfind
insert = MySQLinsert


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("By uzyskać dostęp do tej strony musisz być zalogowany.", "danger")
            return redirect(url_for('login'))
    return wrap



@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=30)



@app.route('/logout')
@login_required
def logout():
    session.clear()
    flash("Zostałeś poprawnie wylogowany.", "success")
    return redirect(url_for('main'))




@app.route('/')
@app.route('/main')
def main():
    return render_template('main.html', title='Strona główna')

@app.route('/main_logged_in')
@login_required
def main_logged_in():
    return render_template('main_logged_in.html', title='Strona główna')


@app.route('/account')
@login_required
def account():
    return render_template('account.html', title='Konto')

@app.route('/edit_data', methods=['GET','POST'])
@login_required
def edit_data():
    form = Data_edit()
    if form.validate_on_submit():
        flash('Edycja danych zakończona sukcesem!', 'success')
        return redirect(url_for('main'))
    return render_template('edit_data.html', title='Edytuj dane', form=form)

@app.route('/about')
def about():
    return render_template('about.html', title='O autorze')

@app.route('/activities')
@login_required
def activities():
    return render_template('activities.html', title='Aktywności')

@app.route('/diets')
@login_required
def diets():
    return render_template('diets.html', title='Moje diety')

@app.route('/products_meals')
@login_required
def products_meals():
    return render_template('products_meals.html', title='Baza produktów i posiłków')




@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'logged_in' in session:
        flash('Jesteś już zalogowany.', 'danger')
        return redirect(url_for('main_logged_in'))
    try:
        form = Login()
        if form.validate_on_submit():
            password = find.find_password_by_email(form.email.data)
            if form.email.data and form.password.data == password:
                rights = find.find_rights_by_email(form.email.data)
                session['logged_in'] = True
                session['username'] = find.find_username_by_email(form.email.data)


                flash('Zalogowano pomyślnie!', 'success')
                return redirect(url_for('main_logged_in'))
            else:
                flash('Błędny login lub hasło. Spróbuj ponownie.', 'danger')
        return render_template('login.html', title='Login', form=form)
    except Exception as e:
        return (str(e))




@app.route('/register', methods=['GET', 'POST'])
def register():
    try:
        form = Registration()
        if form.validate_on_submit():
            email = find.find_by_email(form.email.data)
            username = find.find_by_username(form.username.data)
            if email == None and username == None:
                data = [form.username.data, form.email.data, form.password.data]
                insert.insert_user(data)
                flash(f'Konto dla użytkownika {form.username.data} zostało utworzone pomyślnie! Po zalogowaniu '
                      f'przejdź do zakładki "Moje konto" by edytować swoje dane personalne w celu optymalnego doboru diety.',
                      'success')
                return redirect(url_for('main'))
            elif email != None and username != None:
                flash('Ta nazwa użytkownika i email są już zajęte.', 'danger')
                return redirect(url_for('register'))
            elif email != None:
                flash('Ten email jest już zajęty.', 'danger')
                return redirect(url_for('register'))
            else:
                flash('Ta nazwa użytkownika jest już zajęta.', 'danger')
                return redirect(url_for('register'))
        else:
            return render_template('register.html', title='Register', form=form)
    except Exception as e:
        return (str(e))