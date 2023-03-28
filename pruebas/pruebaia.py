import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from datetime import datetime

# Cargar los datos del archivo CSV utilizando la biblioteca pandas.
df = pd.read_csv('ventas.csv')

# Convertir la fecha a un número.
df['Fecha'] = [datetime.strptime(d, '%Y-%m-%d').timestamp() for d in df['Fecha']]

# Dividir los datos en conjuntos de entrenamiento y prueba.
X = df.iloc[:, 1].values.reshape(-1, 1) # La columna de ventas es nuestra variable independiente
y = df.iloc[:, 2].values.reshape(-1, 1) # La columna de fecha es nuestra variable dependiente
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# Entrenar un modelo de regresión lineal utilizando los datos de entrenamiento.
regressor = LinearRegression()
regressor.fit(X_train, y_train)

# Realizar predicciones utilizando los datos de prueba.
y_pred = regressor.predict(X_test)

# Visualizar los resultados de la predicción en un gráfico.
plt.scatter(X_test, y_test, color='red')
plt.plot(X_test, y_pred, color='blue')
plt.title('Ventas vs Fecha')
plt.xlabel('Ventas')
plt.ylabel('Fecha')
plt.show()

# Imprimir el coeficiente de determinación (R^2) del modelo.
print('Coeficiente de determinación (R^2):', regressor.score(X_test, y_test))
