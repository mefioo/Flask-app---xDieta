from flask import Flask


app = Flask(__name__)
app.config['SECRET_KEY'] = '95a9125ed64ac9f809321cd45164ca1d'


from app import routes
