import json
import numpy as np

with open('data/car_models.json') as jsondata:
    car_models = json.loads(jsondata.read())
    jsondata.close()

with open('data/models_cat_list.txt') as f:
    raw_data = f.read()
    f.close()

with open('data/cities_cat_list.txt') as f:
    raw_cities = f.read()
    f.close()


raw_data = raw_data.replace('\'', '')
raw_data = raw_data.replace('[', '')
raw_data = raw_data.replace(']', '')
model_names = raw_data.split(', ')

# X in [mileage, year, models dummies]
#X = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
mileages_lst = ['under 500', 'under 10,000', 'under 20,000', 'under 40,000', 'under 60,000', 'under 80,000', 'under 100,000',
            'under 130,000', 'under 160,000', 'above 200,000']

prices_lst = ['under $2000', 'under $4,000', 'under $6,000', 'under $8,000', 'under $10,000', 'under $15,000', 'under $20,000',
            'under $40,000', 'under $60,000', 'any price']

#This is a short list instead of using keys to get full list
maker_lst = ['acura', 'aston martin', 'audi', 'bentley', 'bmw', 'buick', 'cadillac', 'chevrolet', 
            'chrysler', 'dodge', 'ford', 'gmc', 'honda', 'hummer', 'hyundai', 'infiniti', 'isuzu',
            'jaguar', 'jeep', 'kia', 'land rover', 'lexus', 'lincoln', 'lotus', 'maserati', 'maybach',
            'mazda', 'mercedes-benz', 'mercury', 'mini', 'mitsubishi', 'nissan', 'panoz', 'pontiac', 
            'saab', 'saturn', 'scion', 'subaru', 'suzuki', 'toyota', 'volkswagen',
            'volvo'] 

def get_cars_names():
    return car_models

def get_cities_names():
    temp = raw_cities.replace('\'', '')
    temp = temp.replace('[', '')
    temp = temp.replace(']', '')
    return temp.split(', ')

def get_default_X(size=23):
    return np.zeros(size)

def loadyears():
    return [x for x in range(2016, 1900, -1)]
#    return [x for x in xrange(1900, 2016)]

def load_manufactures():
    return maker_lst
#    return car_models.keys()

def load_models(maker):
    return car_models[maker]    

def load_conditions():
    return ['new', 'excellent', 'great', 'good', 'fair']

def load_prices():
    return prices_lst

def load_mileages():
    return mileages_lst

def get_mileages_est(mileage):
    ret = mileage.split()
    val = int(ret[1])

def get_X_values(year, maker, model, condition, mileage):
    if maker == 'toyota':
        year_val = int(year)
        models = load_models(maker)
        idx =  models.index(model)
        ret = mileage.replace(',', '').split()
        mileage_val = al = int(ret[1])
        Y = get_default_X(23)
        Y[0] = mileage_val
        Y[1] = year_val
        Y[idx+2] = 1
        #print Y
    return Y

def get_X_values_generic(year, maker, model, condition, mileage):
    year_val = int(year)
    maker_cat_idx = maker_lst.index(maker)
    models_cat_idx = model_names.index(str(model))
    ret = mileage.replace(',', '').split()
    mileage_val = al = int(ret[1])
    #[year, condition, fuel, size, odmeter, len_description, model]  //7
    #type total 13
    #model total 44

    price_delta = [6451, 27306, 47879, 69355]

    Y = get_default_X(64)
    Y[4] = mileage_val
    Y[0] = year_val
    Y[6] = models_cat_idx
    Y[5] = 200
    Y[21+maker_cat_idx] = 1
    print mileage_val, year_val, models_cat_idx, maker_cat_idx
    print Y
    return Y

    #if __name__=='__main__':
