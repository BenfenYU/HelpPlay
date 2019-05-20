from sklearn.externals import joblib

def get_future_waitTime(data):
    model_dir = './models/BuzzLightyearPlanetRescue.joblib'
    natureNum = int(data[0])
    beforeTwo = int(data[1])
    before = int(data[2])
    values = [natureNum,beforeTwo,before]

    reg = joblib.load(model_dir)
    y_pre = reg.predict(values)

    return y_pre