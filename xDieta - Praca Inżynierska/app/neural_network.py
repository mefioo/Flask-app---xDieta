from keras.models import Sequential, load_model
from keras.layers import Dense, Input
from app.routes import dictionary as dict
from keras.optimizers import Adam
from app.database_connection import MySQLfind
import numpy



def train_types(meals, inp):
    X = numpy.zeros((meals, inp))
    Y = numpy.zeros((meals, 3))
    hidden = 10
    outp = 3
    i = 0

    meals = MySQLfind.find_meals_for_table('')
    for id, name, list in meals:
        for prod_name, weight in list:
            number = dict[prod_name]
            X[i, number] = 1
        i = i + 1

    types = MySQLfind.find_type_of_meals('posilki')
    i = 0
    for col in types:
        Y[i, col[0] - 1] = 1
        i = i + 1

    model = Sequential()

    model.add(Dense(hidden, input_dim=inp, activation='sigmoid'))
    model.add(Dense(outp, activation='linear'))
    optimizer = Adam()
    model.compile(loss='mean_squared_error', optimizer=optimizer, metrics=['accuracy'])
    model.fit(X, Y, verbose=0, epochs=500)
    model.save('model.h5')

def predict_type(X):
    model = load_model('model.h5')
    result = model.predict(X)
    return result



