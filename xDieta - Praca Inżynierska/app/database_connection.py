import mysql.connector



config = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'port': '3306',
    'database': 'xdieta',
    'raise_on_warnings': True,
}

link = mysql.connector.connect(**config)
cursor = link.cursor()


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

    def find_username_by_email(email):
        cursor.execute("SELECT * FROM konta WHERE email='{}'".format(email))
        result = cursor.fetchall()
        try:
            return result[0][1]
        except Exception as e:
            pass

class MySQLinsert:

    def insert_user(data):

        sql_query = "INSERT INTO konta (username, email, password, rights, name, surname, age, " \
                    "weight, height, sex) VALUES ('{}', '{}', '{}', '0', NULL, NULL, NULL, NULL, NULL, NULL)"\
                    .format(data[0], data[1], data[2])
        try:
            cursor.execute(sql_query)
            link.commit();
        except Exception as e:
            print(e)
            pass