# Author: Kamil Kornatowski
# Author: Adrian Paczewski

"""
To run program install
pip install pandas
pip install matplotlib
pip install seaborn
pip install sklearn

Research: Predicting the quality of white wines on a scale given chemical measures of each wine

Data {x}:
- Fixed acidity
- Volatile acidity
- Citric acid
- Residual sugar
- Chlorides
- Free sulfur dioxide
- Total sulfur dioxide
- Density
- pH
- Sulphates
- Alcohol

Data reference {x}:
* https://archive.ics.uci.edu/ml/datasets/Wine+Quality

Data {y}:
- Quality

"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import svm

# parsing csv file data
args_x = ["fixed acidity", "volatile acidity", "citric acid", "residual sugar", "chlorides",
          "free sulfur dioxide", "total sulfur dioxide", "density", "pH", "sulphates", "alcohol"]

data = pd.read_csv('winequality-white.csv', delimiter=';',
                   names=["fixed acidity", "volatile acidity", "citric acid", "residual sugar", "chlorides",
                          "free sulfur dioxide", "total sulfur dioxide", "density", "pH", "sulphates", "alcohol",
                          "quality"])
data.head()

sns.pairplot(data, x_vars=args_x, y_vars=['quality'], kind="reg")

plt.show()
print('Data correlation')
print(data.corr())

X = data[args_x]
y = data['quality']

# Fit the SVM model with different kernel types
svc_linear = svm.SVC(kernel="linear").fit(X.values, y)
svc_poly = svm.SVC(kernel="poly").fit(X.values, y)
svc_rbf = svm.SVC(kernel="rbf").fit(X.values, y)
svc_sigmoid = svm.SVC(kernel="sigmoid").fit(X.values, y)

fixed_acidity = 6.2
volatile_acidity = 0.45
citric_acid = 0.26
residual_sugar = 4.4
chlorides = 0.063
free_sulfur_dioxide = 63
total_sulfur_dioxide = 206
density = 0.994
pH = 3.27
sulphates = 0.52
alcohol = 9.8

print(f"Quality of white wine with given chemical measures \n"
      f" * fixed acidity = {fixed_acidity},\n"
      f" * volatile acidity = {volatile_acidity}, \n"
      f" * citric acid = {citric_acid},\n"
      f" * residual sugar = {residual_sugar},\n"
      f" * chlorides = {chlorides},\n"
      f" * free sulfur dioxide = {free_sulfur_dioxide},\n"
      f" * total sulfur dioxide = {total_sulfur_dioxide},\n"
      f" * density = {density},\n"
      f" * pH = {pH},\n"
      f" * sulphates = {sulphates},\n"
      f" * alcohol = {alcohol},\n"
      f"is equal : \n")

print(f"Linear kernel type: ",
      svc_linear.predict([[fixed_acidity, volatile_acidity, citric_acid, residual_sugar, chlorides,
                           free_sulfur_dioxide, total_sulfur_dioxide, density, pH, sulphates, alcohol]]))
print("Poly kernel type: ",
      svc_poly.predict([[fixed_acidity, volatile_acidity, citric_acid, residual_sugar, chlorides,
                         free_sulfur_dioxide, total_sulfur_dioxide, density, pH, sulphates,
                         alcohol]]))
print("Rbf kernel type: ",
      svc_rbf.predict([[fixed_acidity, volatile_acidity, citric_acid, residual_sugar, chlorides,
                        free_sulfur_dioxide, total_sulfur_dioxide, density, pH, sulphates,
                        alcohol]]))
print("Sigmoid kernel type: ",
      svc_sigmoid.predict([[fixed_acidity, volatile_acidity, citric_acid, residual_sugar, chlorides,
                            free_sulfur_dioxide, total_sulfur_dioxide, density, pH, sulphates, alcohol]]))