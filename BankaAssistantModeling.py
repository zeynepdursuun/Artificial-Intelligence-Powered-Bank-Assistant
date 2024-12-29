# -*- coding: utf-8 -*-
"""
Created on Sat Dec 21 21:30:18 2024

@author: ZEYNEP
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.impute import SimpleImputer
from scipy import stats

# Loading the data
data = pd.read_excel('bankaverileri_smote.xlsx')

# Detecting and filling missing data
print("Number of missing values (per column):")
print(data.isnull().sum())

# Filling missing values in numerical columns using SimpleImputer
numerical_columns = data.select_dtypes(include=['float64', 'int64']).columns
imputer_numerical = SimpleImputer(strategy='mean')  # Fill with mean
data[numerical_columns] = imputer_numerical.fit_transform(data[numerical_columns])

# Filling missing values in categorical columns using SimpleImputer
categorical_columns = data.select_dtypes(include=['object']).columns
imputer_categorical = SimpleImputer(strategy='most_frequent')  # Fill with most frequent value
data[categorical_columns] = imputer_categorical.fit_transform(data[categorical_columns])

# Post-missing data handling check
print("\nPost-missing data handling check (per column):")
print(data.isnull().sum())

# Encoding categorical columns
label_encoders = {}
for column in ['Cinsiyet', 'Meslek', 'Eğitim Düzeyi', 'Medeni Durum', 'Konut', 'Araç', 'Arsa']:
    le = LabelEncoder()
    data[column] = le.fit_transform(data[column].astype(str))
    label_encoders[column] = le  # Save encoders for future use

# Defining independent variables (X) and dependent variable (y)
X = data.drop(columns=['Kredi Notu'])  # Exclude 'Kredi Notu' as independent variables
y = data['Kredi Notu']  # 'Kredi Notu' as the dependent variable

# Splitting the data into 75% training and 25% testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)

# *Feature Standardization* (Scaling)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)  # Scale training data
X_test_scaled = scaler.transform(X_test)  # Scale test data

# *Developing a Tree-Based Model* (Increasing number of trees, depth, optimizing min_samples_split, and min_samples_leaf)
random_forest_model = RandomForestRegressor(
    random_state=0, 
    n_estimators=200,  # Increase number of trees
    max_depth=10,  # Increase tree depth
    min_samples_split=5,  # Minimum samples required to split
    min_samples_leaf=2,  # Minimum samples in leaf node
    n_jobs=-1  # Utilize all CPU cores for parallel computation
)

# Training the model
random_forest_model.fit(X_train_scaled, y_train)

# Predicting credit scores using the test data
y_pred_rf = random_forest_model.predict(X_test_scaled)

# Evaluating model performance (Random Forest)
mse_rf = mean_squared_error(y_test, y_pred_rf)
r2_rf = r2_score(y_test, y_pred_rf)

print("\nRandom Forest - Test Data MSE (Standardized):", mse_rf)
print("Random Forest - Test Data R² Score (Standardized):", r2_rf)

# Creating and training a Linear Regression model
linear_model = LinearRegression()
linear_model.fit(X_train_scaled, y_train)

# Predicting credit scores using the test data
y_pred_lr = linear_model.predict(X_test_scaled)

# Evaluating model performance (Linear Regression)
mse_lr = mean_squared_error(y_test, y_pred_lr)
r2_lr = r2_score(y_test, y_pred_lr)

print("\nLinear Regression - Mean Squared Error (MSE):", mse_lr)
print("Linear Regression - R-Squared (R²) Score:", r2_lr)
