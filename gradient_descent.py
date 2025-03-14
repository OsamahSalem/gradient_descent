# -*- coding: utf-8 -*-
"""gradient_descent.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1mX0_HDNYzLFBdujVdY_6U6vdBi1rkrJz
"""

import pandas as pd
file_path = "/content/housing.csv"
df = pd.read_csv(file_path)
df.info(), df.head()

from sklearn.preprocessing import LabelEncoder, StandardScaler

# Label Encoding
categorical_columns = ['mainroad', 'guestroom', 'basement', 'hotwaterheating',
                       'airconditioning', 'prefarea', 'furnishingstatus']

label_encoders = {}
for col in categorical_columns:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le  # Save encoders

# features and target variable
X = df.drop(columns=['price'])
y = df['price'].values.reshape(-1, 1)

# Normalize for better gradient descent convergence
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# bias
import numpy as np

X_scaled = np.c_[np.ones(X_scaled.shape[0]), X_scaled]  # bias
X_scaled.shape, y.shape

import matplotlib.pyplot as plt
def compute_cost(X, y, theta):
    m = len(y)
    predictions = X.dot(theta)
    cost = (1 / (2 * m)) * np.sum((predictions - y) ** 2)
    return cost

# Batch Gradient Descent
def batch_gradient_descent(X, y, theta, alpha, iterations):
    m = len(y)
    cost_history = []

    for _ in range(iterations):
        gradients = (1 / m) * X.T.dot(X.dot(theta) - y)
        theta -= alpha * gradients
        cost_history.append(compute_cost(X, y, theta))

    return theta, cost_history

# Stochastic Gradient Descent
def stochastic_gradient_descent(X, y, theta, alpha, iterations):
    m = len(y)
    cost_history = []

    for _ in range(iterations):
        for i in range(m):
            xi = X[i, :].reshape(1, -1)
            yi = y[i]
            gradients = xi.T.dot(xi.dot(theta) - yi)
            theta -= alpha * gradients
        cost_history.append(compute_cost(X, y, theta))

    return theta, cost_history

# Mini-Batch Gradient Descent
def mini_batch_gradient_descent(X, y, theta, alpha, iterations, batch_size):
    m = len(y)
    cost_history = []

    for _ in range(iterations):
        indices = np.random.permutation(m)
        X_shuffled, y_shuffled = X[indices], y[indices]

        for i in range(0, m, batch_size):
            X_batch = X_shuffled[i:i + batch_size]
            y_batch = y_shuffled[i:i + batch_size]

            gradients = (1 / batch_size) * X_batch.T.dot(X_batch.dot(theta) - y_batch)
            theta -= alpha * gradients

        cost_history.append(compute_cost(X, y, theta))

    return theta, cost_history

# Momentum Gradient Descent
def momentum_gradient_descent(X, y, theta, alpha, iterations, beta=0.9):
    m = len(y)
    cost_history = []
    velocity = np.zeros_like(theta)

    for _ in range(iterations):
        gradients = (1 / m) * X.T.dot(X.dot(theta) - y)
        velocity = beta * velocity + alpha * gradients
        theta -= velocity
        cost_history.append(compute_cost(X, y, theta))

    return theta, cost_history

theta_init = np.zeros((X_scaled.shape[1], 1))
alpha = 0.01
iterations = 200
batch_size = 32

# Train models
theta_bgd, cost_bgd = batch_gradient_descent(X_scaled, y, theta_init.copy(), alpha, iterations)
theta_sgd, cost_sgd = stochastic_gradient_descent(X_scaled, y, theta_init.copy(), alpha, iterations)
theta_mbgd, cost_mbgd = mini_batch_gradient_descent(X_scaled, y, theta_init.copy(), alpha, iterations, batch_size)
theta_mgd, cost_mgd = momentum_gradient_descent(X_scaled, y, theta_init.copy(), alpha, iterations)

# Plot cost function
plt.figure(figsize=(10, 6))
plt.plot(cost_bgd, label="Batch GD")
plt.plot(cost_sgd, label="Stochastic GD")
plt.plot(cost_mbgd, label="Mini-Batch GD")
plt.plot(cost_mgd, label="Momentum GD")
plt.xlabel("Iterations")
plt.ylabel("Cost Function (MSE)")
plt.title("Comparison of Gradient Descent Algorithms")
plt.legend()
plt.grid(True)
plt.show()