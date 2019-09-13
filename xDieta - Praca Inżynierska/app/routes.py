from flask import render_template, url_for, flash, redirect, session
from app.forms import Registration, Login, Data_edit, Change_password, Add_activities, Edit_activities, Add_diet, Delete_diet
from app import app
from app.database_connection import MySQLfind, MySQLinsert, MySQLupdate, MySQLdelete
from datetime import timedelta
from passlib.hash import sha256_crypt

from functools import wraps
from app import algorythm as algorythm


find = MySQLfind
insert = MySQLinsert
update = MySQLupdate
delete = MySQLdelete


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("By uzyskać dostęp do tej strony musisz być zalogowany.", "danger")
            return redirect(url_for('login'))
    return wrap

def specialist_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        rights = find.find_rights_by_username(session['username'])
        if rights[0] == 1:
            return f(*args, **kwargs)
        else:
            flash("Nie masz odpowiednich praw, by odwiedzić tę stronę.", "danger")
            if 'logged_in' in session:
                return redirect(url_for('main_logged_in'))
            else:
                return redirect(url_for('main'))
    return wrap

def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        rights = find.find_rights_by_username(session['username'])
        if rights[0] == 2:
            return f(*args, **kwargs)
        else:
            flash("Nie masz odpowiednich praw, by odwiedzić tę stronę.", "danger")
            if 'logged_in' in session:
                return redirect(url_for('main_logged_in'))
            else:
                return redirect(url_for('main'))
    return wrap


@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=20)







@app.route('/')
@app.route('/main')
def main():
    if 'logged_in' in session:
        return render_template('main_logged_in.html', title='Strona główna')
    return render_template('main.html', title='Strona główna')

@app.route('/main_logged_in')
@login_required
def main_logged_in():
    diets = find.find_diet_by_username(session['username'])
    diet = diets[0]
    data = []
    personal_data = find.find_weight_height_sex_age(session['username'])
    bmr = algorythm.calculate_bmr(personal_data)
    activities = find.find_activities_by_username(session['username'])
    daily_energy = bmr + find.find_working_routine(session['username'])
    for name, hours, energy in activities:
        daily_energy += hours * energy / 7
    per_meal_energy = daily_energy / 5
    for i in range(1, 6):
        info = []
        tmp = find.find_meal_name_by_id(diet[i])
        ingredients = find.find_ingredients_in_meal_by_id(diet[i])
        meal_energy = 0
        for ingredient, weight in ingredients:
            macro = MySQLfind.find_pcf_in_product_by_id(ingredient)
            meal_energy = meal_energy + macro[0] * 4 * weight / 100 + macro[1] * 4 * weight / 100 + macro[2] * 9 * weight / 100
        for row in ingredients:
            weight = int(row[1] * per_meal_energy / meal_energy)
            if weight == 0:
                weight = 1
            ingr = (find.find_ingredient_name_by_id(row[0]), weight)
            info.append(ingr)
        tmp_tab = (tmp, info)
        data.append(tmp_tab)
    return render_template('main_logged_in.html', title='Strona główna', data=data)


@app.route('/account')
@login_required
def account():
    data = find.find_by_username(session['username'])
    return render_template('account.html', title='Konto', data=data)


@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = Change_password()
    if form.validate_on_submit():
        if sha256_crypt.verify(str(form.old.data), find.find_password_by_username(session['username'])):
            if form.old.data == form.new.data:
                flash('Zmiana hasła zakończona niepowodzeniem. Hasła powinny się od siebie różnić.', 'danger')
            else:
                new = sha256_crypt.encrypt(str(form.new.data))
                update.update_password(session['username'], new)
                flash('Zmiana hasła zakończona sukcesem.', 'success')
                return redirect(url_for('main_logged_in'))
        else:
            flash('Podane stare hasło jest niepoprawne.', 'danger')
    return render_template('change_password.html', title='Zmień hasło', form=form)


@app.route('/edit_data', methods=['GET', 'POST'])
@login_required
def edit_data():
    form = Data_edit()
    data = find.find_by_username(session['username'])
    if form.validate_on_submit():
        if form.name.data == '':
            form.name.data = '.'
        if form.surname.data == '':
            form.surname.data = '.'
        account = [form.name.data, form.surname.data, form.age.data, form.weight.data, form.height.data, form.sex.data, form.working_routine.data]
        update.update_user_data(session['username'], account)
        flash('Edycja danych zakończona sukcesem!', 'success')
        return redirect(url_for('main_logged_in'))
    return render_template('edit_data.html', title='Edytuj dane', form=form, data=data)

@app.route('/about_logged_in')
@login_required
def about_logged_in():
    return render_template('about_logged_in.html', title='O autorze')

@app.route('/activities')
@login_required
def activities():
    data = find.find_for_table('aktywnosci')
    return render_template('activities.html', title='Aktywności', data=data)

@app.route('/users_activities')
@login_required
def users_activities():
    data = find.find_activities_by_username(session['username'])
    return render_template('users_activities.html', title='Moje aktywności', data=data)

@app.route('/user_add_activity', methods=['GET', 'POST'])
@login_required
def user_add_activity():
    form = Add_activities()
    info = []
    choices = find.find_column_from_aktywnosci('nazwa_aktywnosci')
    for name in choices:
        data = (name, name)
        info.append(data)
    form.name.choices = info
    if form.validate_on_submit():
        data = find.find_activities_by_username(session['username'])
        for row in data:
            if row[0] == form.name.data:
                flash('Aktywność o tej nazwie jest dodana do Twojego konta. By ją edytować przejdź do zakładki "Edytuj swoje aktywności".', 'danger')
                return redirect(url_for('users_activities'))
        id = find.find_id_by_activity_name(form.name.data)
        insert.insert_user_activity_by_user_id(session['username'], id, int(form.time.data))
        flash('Pomyślnie dodano aktywność!', 'success')
        return redirect(url_for('users_activities'))
    return render_template('user_add_activity.html', title='Dodaj aktywność', form=form)

@app.route('/user_edit_activities', methods=['GET', 'POST'])
@login_required
def user_edit_activities():
    form = Edit_activities()
    info = []
    choices = find.find_activities_by_username(session['username'])
    for name, id, kcal in choices:
        data = (name, name)
        info.append(data)
    form.name.choices = info
    if form.validate_on_submit():
        id = find.find_id_by_activity_name(form.name.data)
        if form.time.data == None:
            delete.delete_user_activity(session['username'], id)
            flash('Pomyślnie usunięto aktywność', 'success')
        else:
            update.update_user_activity(session['username'], id, form.time.data)
            flash('Pomyślnie edytowano aktywność', 'success')
        return redirect(url_for('users_activities'))
    return render_template('user_edit_activities.html', title='Edytuj aktywności', form=form)


@app.route('/diets', methods=['GET', 'POST'])
@login_required
def diets():
    diet = find.find_diet_by_username(session['username'])
    ids = find.find_diet_id_by_username(session['username'])
    data = []
    info = []
    date = []
    tmp_id = []
    tmp = 0
    for id in ids:
        info.append(find.find_diet_date_by_id(id[0]))
        tmp_id.append(id[0])

    for id in info:
        date.append(id[0])

    for id in diet:
        info = []
        info.append(tmp_id[tmp])
        for i in range(1, 6):
            ingr = find.find_ingredients_in_meal_by_id(id[i])
            info.append(find.find_meal_name_by_id(id[i]))
        info.append(date[tmp])
        data.append(info)
        tmp = tmp + 1

    form = Add_diet()
    if form.validate_on_submit():

        diets = find.find_number_of_diets_added_during_one_day(session['username'])
        if len(diets) <= 6:
            insert.insert_diet_with_random_meals(session['username'])
            flash('Pomyślnie dodano dietę!', 'success')
            return redirect(url_for('diets'))
        else:
            flash('Maksymalna liczba dziennych generacji nowych diet wynosi 7. Usuń jedną z wygenerowanych dzisiaj diet, by móc dodać kolejną.', 'danger')

    return render_template('diets.html', title='Moje diety', data=data, form=form)


@app.route('/user_delete_diet', methods=['GET', 'POST'])
@login_required
def user_delete_diet():
    form = Delete_diet()
    choices = []
    info = find.find_diet_id_by_username(session['username'])
    for row in info:
        tmp = (str(row[0]), str(row[0]))
        choices.append(tmp)
    form.id.choices = choices
    if form.validate_on_submit():
        delete.delete_user_diet(session['username'], form.id.data)
        flash('Pomyślnie usunięto dietę!', 'success')
        return redirect(url_for('diets'))

    return render_template('user_delete_diet.html', title='Usuń dietę', form=form)

@app.route('/products_meals')
@login_required
def products_meals():
    data = find.find_meals_and_ingredients_for_table(session['username'])

    return render_template('products_meals.html', title='Baza produktów i posiłków', data=data)

@app.route('/products')
@login_required
def products():
    data = find.find_for_table('produkty')

    return render_template('products.html', title='Baza produktów', data=data)

@app.route('/contact_logged_in')
@login_required
def contact_logged_in():
    return render_template('contact_logged_in.html', title='Kontakt')




@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'logged_in' in session:
        flash('Jesteś już zalogowany.', 'danger')
        return redirect(url_for('main_logged_in'))
    try:
        form = Login()
        if form.validate_on_submit():
            password = find.find_password_by_email(form.email.data)
            if form.email.data and sha256_crypt.verify(str(form.password.data), password):
                rights = find.find_rights_by_email(form.email.data)
                session['logged_in'] = True
                session['username'] = find.find_username_by_email(form.email.data)
                username = session['username']

                flash(f'Cześć {username}!', 'success')
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
                password = sha256_crypt.encrypt((str(form.password.data)))
                data = [form.username.data, form.email.data, password]
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


@app.route('/logout')
@login_required
def logout():
    username = session['username']
    session.clear()
    flash(f"Do zobaczenia {username}!", "success")
    return redirect(url_for('main'))
