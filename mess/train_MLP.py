'''
 MLP多层感知器，一种监督学习算法，它可以学习用于分类或回
 归的非线性函数。 与逻辑回归不同的是，在输入层和输出层之
 间，可以有一个或多个非线性层，称为隐藏层。
'''

from sklearn.neural_network import MLPClassifier,MLPRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.externals import joblib
import matplotlib.pyplot as plt
import numpy as np

fileName = './data/train_BuzzLightyearPlanetRescue.txt'
model_dir = './models/BuzzLightyearPlanetRescue.joblib'

X ,y = [],[]
with open(fileName,'r') as fp:
    for line in fp:
        data = line.split(',')
        natureNum = int(data[0])
        beforeTwo = int(data[1])
        before = int(data[2])
        wait_time = int(data[3])

        X.append([natureNum,beforeTwo,before])
        y.append(wait_time)

clf = MLPClassifier(solver='lbfgs', alpha=1e-5,
                    hidden_layer_sizes=(30, ),
                    random_state=1)
reg = MLPRegressor(solver='lbfgs', alpha=1e-5,
                    hidden_layer_sizes=(30, ),
                    random_state=1)
scaler = StandardScaler()
scaler.fit(X)
X = scaler.transform(X)

X_train, X_test, y_train, y_test = train_test_split(X, y)

clf.fit(X_train,y_train)
reg.fit(X_train,y_train)
clfAccurace = clf.score(X_test,y_test)
regAccurace = reg.score(X_test,y_test)
print('clf精度为{}，regression精度为{}'.format(clfAccurace,regAccurace))

joblib.dump(reg, model_dir) 

