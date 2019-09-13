

def calculate_bmr(data):
    bmr = 9.99*data[0] + 6.25*data[1] - 4.92*data[2]
    if data[3] == 'M':
        bmr += 5
    else:
        bmr -= 161
    return bmr


def activities_energy(activities, hours):
    energy = 0
    for activity, time in activities, hours:
        energy += activity * time
    return energy


def return_energy_of_meal(products):
    ''' products = [name, proteins, carbos, fats] '''
    sum = 0
    for name, proteins, carbos, fats in products:
        sum = sum + proteins * 4 + carbos * 4 + fats * 9
    return sum

