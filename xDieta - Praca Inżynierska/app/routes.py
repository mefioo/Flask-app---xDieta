from flask import render_template, url_for, flash, redirect, session
from app.forms import Registration, Login, Data_edit, Change_password, Add_activities, Edit_activities, Add_diet, \
    Delete_diet, Change_rights, Delete_account, Add_activity_Admin, Change_password_Admin, Add_meal, Add_product, \
    Add_product_to_meal, Delete_meal, Delete_ingredient
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
        if rights[0] == 1 or rights[0] == 2:
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
        if 'logged_in' in session:
            rights = find.find_rights_by_username(session['username'])
            if rights[0] == 2:
                return f(*args, **kwargs)
            else:
                flash("Nie masz odpowiednich praw, by odwiedzić tę stronę.", "danger")
                if 'logged_in' in session:
                    return redirect(url_for('main_logged_in'))
                else:
                    return redirect(url_for('main'))
        else:
            return redirect(url_for('login'))
    return wrap


@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=20)







@app.route('/')
@app.route('/main')
def main():
    if 'logged_in' in session:
        return redirect(url_for('main_logged_in'))
    return render_template('main.html', title='Strona główna')

@app.route('/main_logged_in')
@login_required
def main_logged_in():
    perm = find.find_rights_by_username(session['username'])
    diets = find.find_diet_by_username(session['username'])
    if diets == []:
        data = 'no_diets'
    else:
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
                meal_energy = meal_energy + macro[0] * 4 * weight / 100 + macro[1] * 4 * weight / 100 + macro[
                    2] * 9 * weight / 100
            for row in ingredients:
                weight = int(row[1] * per_meal_energy / meal_energy)
                if weight == 0:
                    weight = 1
                ingr = (find.find_ingredient_name_by_id(row[0]), weight)
                info.append(ingr)
            tmp_tab = (tmp, info)
            data.append(tmp_tab)
    return render_template('main_logged_in.html', title='Strona główna', data=data, perm=perm[0])


@app.route('/account')
@login_required
def account():
    perm = find.find_rights_by_username(session['username'])
    data = find.find_by_username(session['username'])
    return render_template('account.html', title='Konto', data=data, perm=perm[0])


@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    perm = find.find_rights_by_username(session['username'])
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
    return render_template('change_password.html', title='Zmień hasło', form=form, perm=perm)


@app.route('/edit_data', methods=['GET', 'POST'])
@login_required
def edit_data():
    perm = find.find_rights_by_username(session['username'])
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
    return render_template('edit_data.html', title='Edytuj dane', form=form, data=data, perm=perm[0])

@app.route('/about_logged_in')
@login_required
def about_logged_in():
    perm = find.find_rights_by_username(session['username'])
    return render_template('about_logged_in.html', title='O autorze', perm=perm[0])

@app.route('/activities')
@login_required
def activities():
    perm = find.find_rights_by_username(session['username'])
    data = find.find_for_table('aktywnosci')
    return render_template('activities.html', title='Aktywności', data=data, perm=perm[0])

@app.route('/users_activities')
@login_required
def users_activities():
    perm = find.find_rights_by_username(session['username'])
    data = find.find_activities_by_username(session['username'])
    return render_template('users_activities.html', title='Moje aktywności', data=data, perm=perm[0])

@app.route('/user_add_activity', methods=['GET', 'POST'])
@login_required
def user_add_activity():
    perm = find.find_rights_by_username(session['username'])
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
    return render_template('user_add_activity.html', title='Dodaj aktywność', form=form, perm=perm[0])

@app.route('/user_edit_activities', methods=['GET', 'POST'])
@login_required
def user_edit_activities():
    perm = find.find_rights_by_username(session['username'])
    form = Edit_activities()
    info = []
    choices = find.find_activities_by_username(session['username'])
    for name, id, kcal in choices:
        data = (name, name)
        info.append(data)
    form.name.choices = info
    if form.name.choices == []:
        flash('Nie można edytować aktywności, gdyż żadne nie zostały dodane.', 'danger')
        return redirect(url_for('users_activities'))
    if form.validate_on_submit():
        id = find.find_id_by_activity_name(form.name.data)
        if form.time.data == None:
            delete.delete_user_activity(session['username'], id)
            flash('Pomyślnie usunięto aktywność', 'success')
        else:
            update.update_user_activity(session['username'], id, form.time.data)
            flash('Pomyślnie edytowano aktywność', 'success')
        return redirect(url_for('users_activities'))
    return render_template('user_edit_activities.html', title='Edytuj aktywności', form=form, perm=perm[0])


@app.route('/diets', methods=['GET', 'POST'])
@login_required
def diets():

    perm = find.find_rights_by_username(session['username'])
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
        personal_data = find.find_weight_height_sex_age(session['username'])
        for row in personal_data:
            if row is None:
                flash(
                    'Uzupełnij swoje dane personalne, by móc wygenerować dietę. Potrzebne wartości to: waga, wzrost, płeć oraz wiek.',
                    'danger')
                return redirect(url_for('edit_data'))
        diets = find.find_number_of_diets_added_during_one_day(session['username'])
        if len(diets) <= 6:
            insert.insert_diet_with_random_meals(session['username'])
            flash('Pomyślnie dodano dietę!', 'success')
            return redirect(url_for('diets'))
        else:
            flash('Maksymalna liczba dziennych generacji nowych diet wynosi 7. Usuń jedną z wygenerowanych dzisiaj diet, by móc dodać kolejną.', 'danger')

    return render_template('diets.html', title='Moje diety', data=data, form=form, perm=perm[0])


@app.route('/user_delete_diet', methods=['GET', 'POST'])
@login_required
def user_delete_diet():
    perm = find.find_rights_by_username(session['username'])
    form = Delete_diet()
    choices = []
    info = find.find_diet_id_by_username(session['username'])
    for row in info:
        tmp = (str(row[0]), str(row[0]))
        choices.append(tmp)
    form.id.choices = choices
    if form.id.choices == []:
        flash('Nie można usunąć diet, gdyż żadne nie zostały dodane.', 'danger')
        return redirect(url_for('diets'))
    if form.validate_on_submit():
        delete.delete_user_diet(session['username'], form.id.data)
        flash('Pomyślnie usunięto dietę!', 'success')
        return redirect(url_for('diets'))

    return render_template('user_delete_diet.html', title='Usuń dietę', form=form, perm=perm[0])

@app.route('/products_meals')
@login_required
def products_meals():
    perm = find.find_rights_by_username(session['username'])
    personal_data = find.find_weight_height_sex_age(session['username'])
    for row in personal_data:
        if row is None:
            flash(
                'Uzupełnij swoje dane personalne, by móc przeglądać bazę posiłków i produktów. Potrzebne wartości to: waga, wzrost, płeć oraz wiek.',
                'danger')
            return redirect(url_for('edit_data'))
    data = find.find_meals_and_ingredients_for_table(session['username'])

    return render_template('products_meals.html', title='Baza produktów i posiłków', data=data, perm=perm[0])

@app.route('/products')
@login_required
def products():
    perm = find.find_rights_by_username(session['username'])
    personal_data = find.find_weight_height_sex_age(session['username'])
    for row in personal_data:
        if row is None:
            flash(
                'Uzupełnij swoje dane personalne, by móc przeglądać bazę posiłków i produktów. Potrzebne wartości to: waga, wzrost, płeć oraz wiek.',
                'danger')
            return redirect(url_for('edit_data'))
    data = find.find_for_table('produkty')

    return render_template('products.html', title='Baza produktów', data=data, perm=perm[0])

@app.route('/contact_logged_in')
@login_required
def contact_logged_in():
    perm = find.find_rights_by_username(session['username'])
    return render_template('contact_logged_in.html', title='Kontakt', perm=perm[0])


@app.route('/change_rights', methods=['GET', 'POST'])
@admin_required
def change_rights():
    form = Change_rights()
    choices = []
    users = find.find_all_usernames('konta')
    for user in users:
        info = (user[0], user[0])
        choices.append(info)
    form.username.choices = choices
    if form.validate_on_submit():
        update.update_user_rights(form.username.data, int(form.rights.data))
        flash(f'Zmieniono uprawnienia na {form.rights.data} dla użytkownika {form.username.data}', 'success')
        return redirect(url_for('admin'))
    return render_template('change_rights.html', title='Zmień uprawnienia', form=form)


@app.route('/add_activity_admin', methods=['GET', 'POST'])
@specialist_required
def add_activity_admin():
    perm = find.find_rights_by_username(session['username'])
    form = Add_activity_Admin()
    if form.validate_on_submit():
        insert.insert_activity(form.name.data, form.kcal.data)
        flash(f'Pomyślnie dodano aktywność {form.name.data}', 'success')
        return redirect(url_for('admin'))
    return render_template('add_activity_admin.html', title='Dodaj aktywność', form=form, perm=perm[0])


@app.route('/change_password_admin', methods=['GET', 'POST'])
@admin_required
def change_password_admin():
    form = Change_password_Admin()
    choices = []
    users = find.find_all_usernames('konta')
    for user in users:
        info = (user[0], user[0])
        choices.append(info)
    form.username.choices = choices
    if form.validate_on_submit():
        password = sha256_crypt.encrypt((str(form.password.data)))
        update.update_password(form.username.data, password)
        flash(f'Pomyślnie zmieniono hasło dla użytkownika {form.username.data}', 'success')
        return redirect(url_for('admin'))
    return render_template('change_password_admin.html', title='Zmień hasło', form=form)


@app.route('/delete_account', methods=['GET', 'POST'])
@admin_required
def delete_account():
    form = Delete_account()
    choices = []
    users = find.find_all_usernames('konta')
    for user in users:
        info = (user[0], user[0])
        choices.append(info)
    form.username.choices = choices
    if form.validate_on_submit():
        if form.username.data == session['username']:
            flash('Nie można usunąć obecnie zalogowanego konta.', 'danger')
            return redirect(url_for('admin'))
        delete.delete_user_account(form.username.data)
        flash(f'Pomyślnie usunięto konto dla użytkownika {form.username.data}', 'success')
        return redirect(url_for('admin'))
    return render_template('delete_account.html', title='Usuń konto', form=form)


@app.route('/add_meal', methods=['GET', 'POST'])
@specialist_required
def add_meal():
    perm = find.find_rights_by_username(session['username'])
    form = Add_meal()
    if form.validate_on_submit():
        names = find.find_all_names('posilki')
        form.name.data = form.name.data + '\n'
        for row in names:
            if row[0] == form.name.data:
                flash('Posiłek o tej nazwie jest już dodany do bazy danych.', 'danger')
                return redirect(url_for('admin'))
        insert.insert_meal_name(form.name.data)
        flash(f'Pomyślnie dodano posiłek o nazwie {form.name.data}', 'success')
        return redirect(url_for('admin'))
    return render_template('add_meal.html', title='Dodaj posiłek', form=form, perm=perm[0])


@app.route('/add_ingredient', methods=['GET', 'POST'])
@specialist_required
def add_ingredient():
    perm = find.find_rights_by_username(session['username'])
    form = Add_product()
    if form.validate_on_submit():
        names = find.find_all_names('produkty')
        for row in names:
            if row[0] == form.name.data:
                flash('Produkt o tej nazwie jest już dodany do bazy danych.', 'danger')
                return redirect(url_for('admin'))
        insert.insert_ingredient(form.name.data, form.protein.data, form.fats.data, form.carbos.data)
        flash(f'Pomyślnie dodano produkt o nazwie {form.name.data}', 'success')
        return redirect(url_for('admin'))
    return render_template('add_ingredient.html', title='Dodaj produkt', form=form, perm=perm[0])


@app.route('/add_ingredient_to_meal', methods=['GET', 'POST'])
@specialist_required
def add_ingredient_to_meal():
    perm = find.find_rights_by_username(session['username'])
    data = find.find_for_table('produkty')
    form = Add_product_to_meal()
    choices = []
    ids = []
    names = find.find_all_names('posilki')
    id = find.find_all_id_produktu('produkty')
    for row in names:
        tmp = row[0]
        if '\n' in row[0]:
            tmp = row[0].replace('\n', '')
        info = (tmp, tmp)
        choices.append(info)
    id.sort()
    for row in id:
        info = (str(row[0]), str(row[0]))
        ids.append(info)
    form.name.choices = choices

    form.ingredient.choices = ids
    if form.validate_on_submit():
        form.name.data = form.name.data + '\n'
        meal = find.find_meal_id_by_name(form.name.data)
        insert.insert_ingredient_into_meal(meal, form.ingredient.data, form.weight.data)
        flash(f'Pomyślnie dodano produkt do posiłku {form.name.data}.', 'success')
        return redirect(url_for('add_ingredient_to_meal'))
    return render_template('add_ingredient_to_meal.html', title='Dodaj produkt do posiłku', data=data, form=form, perm=perm[0])


@app.route('/delete_meal', methods=['GET', 'POST'])
@specialist_required
def delete_meal():
    perm = find.find_rights_by_username(session['username'])
    form = Delete_meal()
    choices = []
    names = find.find_all_names('posilki')
    for row in names:
        tmp = row[0]
        if '\n' in row[0]:
            tmp = row[0].replace('\n', '')
        info = (tmp, tmp)
        choices.append(info)
    form.name.choices = choices

    if form.validate_on_submit():
        form.name.data = form.name.data + '\n'
        id = find.find_meal_id_by_name(form.name.data)
        delete.delete_meal(id)
        flash(f'Pomyślnie usunięto posiłek o nazwie {form.name.data}.', 'success')
        return redirect(url_for('admin'))
    data = find.find_meals_for_table(session['username'])
    return render_template('delete_meal.html', title='Usuń posiłek', form=form, data=data, perm=perm[0])


@app.route('/delete_ingredient', methods=['GET', 'POST'])
@specialist_required
def delete_ingredient():
    perm = find.find_rights_by_username(session['username'])
    data = find.find_for_table('produkty')
    choices = []
    names = find.find_all_names('produkty')
    for row in names:
        tmp = (row[0], row[0])
        choices.append(tmp)
    form = Delete_ingredient()
    form.name.choices = choices
    if form.validate_on_submit():
        id = find.find_ingredient_id_by_name(form.name.data)
        meals_row = find.find_ingredient_in_meal_row(id)
        if len(meals_row) != 0:
            flash(f'{form.name.data} jest składnikiem przynajmniej jednego posiłku. Usuń posiłki, w których się '
                  f'on znajduje, by móc usunąć ten produkt.', 'danger')
            return redirect(url_for('delete_ingredient'))
        else:
            delete.delete_ingredient(id)
        flash(f'Pomyślnie usunięto produkt o nazwie {form.name.data}.', 'success')
        return redirect(url_for('admin'))
    return render_template('delete_ingredient.html', title='Usuń produkt', form=form, data=data, perm=perm[0])


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'logged_in' in session:
        flash('Jesteś już zalogowany.', 'danger')
        return redirect(url_for('main_logged_in'))
    try:
        form = Login()
        if form.validate_on_submit():
            password = find.find_password_by_email(form.email.data)
            if password == None:
                flash('Błędny login lub hasło. Spróbuj ponownie.', 'danger')
                return render_template('login.html', title='Login', form=form)
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
        return str(e)



@app.route('/admin')
@admin_required
def admin():
    perm = find.find_rights_by_username(session['username'])
    return render_template('admin.html', title='Strefa administratora', perm=perm[0])


@app.route('/specialist')
@specialist_required
def specialist():
    perm = find.find_rights_by_username(session['username'])
    return render_template('specialist.html', title='Strefa specjalisty', perm=perm[0])


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
