import mysql.connector
import random
import datetime
import app.algorythm as algorythm


config = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'port': '3306',
    'database': 'xdieta',
    'raise_on_warnings': True,
}

link = mysql.connector.connect(**config)
cursor = link.cursor(buffered=True)


class MySQLfind:

    def find_password_by_email(email):
        cursor.execute("SELECT * FROM konta WHERE email='{}'".format(email))
        result = cursor.fetchall()
        try:
            return result[0][3]
        except Exception as e:
            pass

    def find_by_email(email):
        cursor.execute("SELECT * FROM konta WHERE email='{}'".format(email))
        result = cursor.fetchall()
        try:
            return result[0]
        except Exception as e:
            pass

    def find_by_username(username):
        cursor.execute("SELECT * FROM konta WHERE username='{}'".format(username))
        result = cursor.fetchall()
        try:
            return result[0]
        except Exception as e:
            pass

    def find_rights_by_email(email):
        cursor.execute("SELECT * FROM konta WHERE email='{}'".format(email))
        result = cursor.fetchall()
        try:
            return result[0][4]
        except Exception as e:
            pass

    def find_rights_by_username(username):
        cursor.execute("SELECT rights FROM konta WHERE username='{}'".format(username))
        result = cursor.fetchall()
        try:
            return result[0]
        except Exception as e:
            pass

    def find_username_by_email(email):
        cursor.execute("SELECT * FROM konta WHERE email='{}'".format(email))
        result = cursor.fetchall()
        try:
            return result[0][1]
        except Exception as e:
            pass

    def find_password_by_username(username):
        cursor.execute("SELECT * FROM konta WHERE username='{}'".format(username))
        result = cursor.fetchall()
        try:
            return result[0][3]
        except Exception as e:
            pass

    def find_for_table(table):
        cursor.execute("SELECT * FROM " + table)
        result = cursor.fetchall()
        try:
            return result
        except Exception as e:
            pass

    def find_activity_name_by_id(id):
        cursor.execute("SELECT nazwa_aktywnosci FROM aktywnosci WHERE id_aktywnosci='{}'".format(id))
        result = cursor.fetchall()
        try:
            return result[0]
        except Exception as e:
            pass

    def find_activity_energy_by_id(id):
        cursor.execute("SELECT spalana_energia FROM aktywnosci WHERE id_aktywnosci='{}'".format(id))
        result = cursor.fetchall()
        try:
            return result[0]
        except Exception as e:
            pass

    def find_activities_by_username(login):
        cursor.execute("SELECT * FROM wiersze_aktywnosci WHERE username='{}'".format(login))
        result = cursor.fetchall()
        data = []
        for login, id, time in result:
            activity = MySQLfind.find_activity_name_by_id(id)
            energy = MySQLfind.find_activity_energy_by_id(id)
            info = [activity[0], time, energy[0]]
            data.append(info)
        try:
            return data
        except Exception as e:
            pass

    def find_column_from_aktywnosci(column):
        cursor.execute("SELECT " + column + " FROM aktywnosci")
        result = cursor.fetchall()
        data = []
        for name in result:
            info = (name[0])
            data.append(info)
        try:
            return data
        except Exception as e:
            pass

    def find_meal_name_by_id(id):
        cursor.execute("SELECT nazwa FROM posilki WHERE id_posilku = '{}'".format(id))
        result = cursor.fetchall()
        try:
            return result[0][0]
        except Exception as e:
            pass

    def find_id_by_activity_name(name):
        cursor.execute("SELECT id_aktywnosci FROM aktywnosci WHERE nazwa_aktywnosci='{}'".format(name))
        result = cursor.fetchall()
        try:
            return result[0][0]
        except Exception as e:
            pass

    def find_diet_by_id(id):
        cursor.execute("SELECT * FROM diety WHERE id_diety = '{}'".format(id))
        result = cursor.fetchall()
        try:
            return result[0]
        except Exception as e:
            pass

    def find_diet_by_username(name):
        cursor.execute("SELECT id_diety FROM tygodniowe_diety WHERE username ='{}'".format(name))
        result = cursor.fetchall()
        diet = []
        for id in result:
            diet.append(MySQLfind.find_diet_by_id(id[0]))
        try:
            return diet
        except Exception as e:
            pass

    def find_diet_date_by_id(id):
        cursor.execute("SELECT date FROM tygodniowe_diety WHERE id_diety = '{}'".format(id))
        result = cursor.fetchall()
        try:
            return result[0]
        except Exception as e:
            pass

    def find_diet_id_by_username(username):
        cursor.execute("SELECT id_diety FROM tygodniowe_diety WHERE username = '{}'".format(username))
        result = cursor.fetchall()
        try:
            return result
        except Exception as e:
            pass

    def find_weight_height_sex_age(username):
        cursor.execute("SELECT weight, height, age, sex FROM konta WHERE username = '{}'".format(username))
        result = cursor.fetchall()
        try:
            return result[0]
        except Exception as e:
            pass

    def find_diet_id_by_meals(m1, m2, m3, m4, m5):
        cursor.execute("SELECT id_diety FROM diety WHERE posilek_1 = '{}' AND posilek_2 = '{}' AND posilek_3 = '{}'"
                       "AND posilek_4 = '{}' AND posilek_5 = '{}'".format(m1, m2, m3, m4, m5))
        result = cursor.fetchall()
        try:
            return result[0]
        except Exception as e:
            pass

    def find_ingredients_in_meals(table):
        cursor.execute("SELECT * FROM " + table)
        result = cursor.fetchall()
        try:
            return result
        except Exception as e:
            pass

    def find_ingredient_name_by_id(id):
        cursor.execute("SELECT nazwa FROM produkty WHERE id_produktu = '{}'".format(id))
        result = cursor.fetchall()
        try:
            return result[0][0]
        except Exception as e:
            pass

    def find_ingredients_in_meal_by_id(id):
        cursor.execute("SELECT id_produktu, waga_w_gramach FROM wiersze_posilkow WHERE id_posilku = '{}'".format(id))
        result = cursor.fetchall()
        try:
            return result
        except Exception as e:
            pass

    def find_working_routine(username):
        cursor.execute("SELECT working_routine FROM konta WHERE username = '{}'".format(username))
        result = cursor.fetchall()
        if result[0][0] == 1:
            return 0
        elif result[0][0] == 2:
            return 100
        elif result[0][0] == 3:
            return 200
        elif result[0][0] == 4:
            return 350
        else:
            return 500

    def find_pcf_in_product_by_id(id):
        cursor.execute("SELECT bialko_w_100g, wegle_w_100g, tluszcze_w_100g FROM produkty WHERE id_produktu = '{}'".format(id))
        result = cursor.fetchall()
        try:
            return result[0]
        except Exception as e:
            pass


    def find_meals_and_ingredients_for_table(username):
        meals = MySQLfind.find_for_table('posilki')
        personal_data = MySQLfind.find_weight_height_sex_age(username)
        bmr = algorythm.calculate_bmr(personal_data)
        activities = MySQLfind.find_activities_by_username(username)
        daily_energy = bmr + MySQLfind.find_working_routine(username)
        for name, hours, energy in activities:
            daily_energy += hours*energy/7
        per_meal_energy = daily_energy/5

        new_data = []
        for row in meals:
            info = []
            meal_energy = 0
            ingredients = MySQLfind.find_ingredients_in_meal_by_id(row[0])
            for ingredient, weight in ingredients:
                macro = MySQLfind.find_pcf_in_product_by_id(ingredient)
                meal_energy = meal_energy + macro[0] * 4 * weight/100 + macro[1] * 4 * weight/100 + macro[2] * 9 * weight/100
            for ingredient, weight in ingredients:
                tmp = (MySQLfind.find_ingredient_name_by_id(ingredient), int(weight * per_meal_energy / meal_energy))
                info.append(tmp)
            tmp2 = (row[0], MySQLfind.find_meal_name_by_id(row[0]), info)
            new_data.append(tmp2)

        try:
            return new_data
        except Exception as e:
            pass

    def find_number_of_diets_added_during_one_day(username):
        x = datetime.datetime.now()
        date = x.strftime("%Y-%m-%d")
        cursor.execute("SELECT date FROM tygodniowe_diety WHERE username = '{}' AND date = '{}'".format(username, date))
        result = cursor.fetchall()
        try:
            return result
        except Exception as e:
            pass



class MySQLinsert:

    def insert_user(data):

        sql_query = "INSERT INTO konta (username, email, password, rights, name, surname, age, " \
                    "weight, height, sex, working_routine) VALUES ('{}', '{}', '{}', '0', NULL, NULL, NULL, NULL, NULL, NULL, '1')"\
                    .format(data[0], data[1], data[2])
        try:
            cursor.execute(sql_query)
            link.commit()
        except Exception as e:
            pass

    def insert_user_activity_by_user_id(username, activity_id, time):

        sql_query = "INSERT INTO `wiersze_aktywnosci` (`username`, `id_aktywnosci`, `liczba_godzin_w_tygodniu`)" \
                    " VALUES ('{}', '{}', '{}');".format(username, activity_id, time)
        try:
            cursor.execute(sql_query)
            link.commit()
        except Exception as e:
            pass

    def insert_weekly_diet_by_username(username, id):
        x = datetime.datetime.now()
        date = x.strftime("%Y-%m-%d")
        sql_query = "INSERT INTO tygodniowe_diety (username, id_diety, date) VALUES ('{}', '{}', '{}')".format(username, id, date)
        try:
            cursor.execute(sql_query)
            link.commit()
        except Exception as e:
            print(e)
            pass

    def insert_diet_with_random_meals(username):
        id = []
        for i in range(5):
            id.append(random.randrange(1, 900, 1))
        sql_query = "INSERT INTO diety (posilek_1, posilek_2, posilek_3, posilek_4, posilek_5) VALUES " \
                    "('{}', '{}', '{}', '{}', '{}')".format(id[0], id[1], id[2], id[3], id[4])
        try:
            cursor.execute(sql_query)
            link.commit()
            id = MySQLfind.find_diet_id_by_meals(id[0], id[1], id[2], id[3], id[4])
            MySQLinsert.insert_weekly_diet_by_username(username, id[0])
        except Exception as e:
            pass


class MySQLupdate:

    def update_user_data(login, data):
        sql_query = "UPDATE konta SET name = '{}', surname ='{}', age = '{}', weight = '{}', height = '{}'," \
                    " sex = '{}', working_routine = '{}' WHERE username = '{}'".format(*data, login)
        try:
            cursor.execute(sql_query)
            link.commit()
        except Exception as e:
            pass

    def update_password(login, data):
        sql_query = "UPDATE konta SET password = '{}' WHERE username = '{}'".format(data, login)
        try:
            cursor.execute(sql_query)
            link.commit()
        except Exception as e:
            pass

    def update_user_activity(username, id, time):
        sql_query = "UPDATE wiersze_aktywnosci SET liczba_godzin_w_tygodniu = '{}' WHERE username = '{}' " \
                    "AND id_aktywnosci = '{}'".format(time, username, id)
        try:
            cursor.execute(sql_query)
            link.commit()
        except Exception as e:
            pass




class MySQLdelete:

    def delete_user_activity(username, id):
        sql_query = "DELETE FROM wiersze_aktywnosci WHERE username='{}' AND id_aktywnosci = '{}'".format(username, id)
        try:
            cursor.execute(sql_query)
            link.commit()
        except Exception as e:
            pass

    def delete_weekly_diet(username, id):
        sql_query = "DELETE FROM tygodniowe_diety WHERE username = '{}' AND id_diety = '{}'".format(username, id)
        try:
            cursor.execute(sql_query)
            link.commit()
        except Exception as e:
            pass

    def delete_user_diet(username, id):
        MySQLdelete.delete_weekly_diet(username, id)
        sql_query = "DELETE FROM diety WHERE id_diety = '{}'".format(id)
        try:
            cursor.execute(sql_query)
            link.commit()
        except Exception as e:
            pass


