# -*- coding: utf-8 -*-
"""Final Uterine Corpus Endometrial Carcinoma.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1XKhMHYKOC6oiQ1nzE8qL1-vED7bDUR0X
"""

import pandas as pd
import numpy as np

df=pd.read_csv("/content/Uterine Corpus Endometrial Carcinoma.csv")
# Display basic information about the dataset
print("Original Dataset Info:")
print(df.info())

df.head()

columns_to_drop_na = ['Disease Free Status', 'MSIsensor Score']
df = df.dropna(subset=columns_to_drop_na)

# Display information after cleaning
print("\nCleaned Dataset Info:")
print(df.info())

# Display the number of null values in each column
null_counts = df.isnull().sum()
print("Null Values in Each Column:")
print(null_counts)

# Display the total number of null values in the entire DataFrame
total_nulls = df.isnull().sum().sum()
print("\nTotal Null Values in the DataFrame:", total_nulls)

df['Mutation Count'].fillna(df['Mutation Count'].mean(), inplace=True)
df['Fraction Genome Altered'].fillna(df['Fraction Genome Altered'].mean(), inplace=True)
df['Diagnosis Age'].fillna(df['Diagnosis Age'].median(), inplace=True)
df['MSI MANTIS Score'].fillna(df['MSI MANTIS Score'].mean(), inplace=True)

df['Race Category'].fillna('Unknown', inplace=True)
df['Subtype'].fillna('Unknown', inplace=True)

# Display the number of null values in each column after cleaning
cleaned_null_counts = df.isnull().sum()
print("Null Values in Each Column After Cleaning:")
print(cleaned_null_counts)

# Display the total number of null values in the entire DataFrame after cleaning
total_cleaned_nulls = df.isnull().sum().sum()
print("\nTotal Null Values in the DataFrame After Cleaning:", total_cleaned_nulls)

df.head()

import matplotlib.pyplot as plt
import seaborn as sns

# Summary statistics
summary_stats = df.describe()
print("Summary Statistics:")
print(summary_stats)

# Visualize the distribution of 'Diagnosis Age'
plt.figure(figsize=(10, 6))
sns.histplot(df['Diagnosis Age'], bins=20, kde=True)
plt.title('Distribution of Diagnosis Age')
plt.xlabel('Diagnosis Age')
plt.ylabel('Frequency')
plt.show()

# Create a new feature 'Age Group' based on 'Diagnosis Age'
df['Age Group'] = pd.cut(df['Diagnosis Age'], bins=[0, 40, 60, 80, 100], labels=['0-40', '41-60', '61-80', '81-100'])

# Encode categorical variables using one-hot encoding
df_encoded = pd.get_dummies(df, columns=['Race Category', 'Subtype'], drop_first=True)
df_encoded

# Correlation matrix
correlation_matrix = df.corr()
print("Correlation Matrix:")
print(correlation_matrix)

# Pairplot for selected numerical features
sns.pairplot(df[['Mutation Count', 'Fraction Genome Altered', 'Diagnosis Age']])
plt.show()



# Assuming df is your original DataFrame
# Extract information from 'Overall Survival Status'
df['IsLiving'] = df['Overall Survival Status'].apply(lambda x: 1 if 'LIVING' in x else 0)

# Extract information from 'Disease Free Status'
df['IsDiseaseFree'] = df['Disease Free Status'].apply(lambda x: 1 if 'DiseaseFree' in x else 0)
df['IsAliveOrDeadTumorFree'] = df['Disease Free Status'].apply(lambda x: 1 if 'ALIVE OR DEAD TUMOR FREE' in x else 0)

df

import seaborn as sns
import matplotlib.pyplot as plt

# Correlation matrix
correlation_matrix = df.corr()

# Plotting the correlation heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)
plt.title('Correlation Heatmap of Numerical Features')
plt.show()

import seaborn as sns
import matplotlib.pyplot as plt

# Count plot for 'Disease-specific Survival status' with a different color palette
plt.figure(figsize=(8, 6))
sns.countplot(x='Disease-specific Survival status', data=df, palette='viridis')  # Change 'viridis' to your desired color palette
plt.title('Class Count in Disease-specific Survival Status')
plt.xlabel('Disease-specific Survival Status')
plt.ylabel('Count')
plt.show()

# Subset of selected features
selected_features = ['Cancer Type Detailed', 'Mutation Count', 'Fraction Genome Altered',
                     'Diagnosis Age', 'MSI MANTIS Score', 'MSIsensor Score', 'Subtype',
                     'Tumor Type', 'Disease-specific Survival status']

selected_df = df[selected_features]

# Boxplot for continuous variables
plt.figure(figsize=(15, 10))
sns.boxplot(data=selected_df[['Mutation Count', 'Fraction Genome Altered', 'Diagnosis Age', 'MSI MANTIS Score', 'MSIsensor Score']])
plt.title('Boxplot of Selected Numerical Features')
plt.show()

# Violin plot for 'Diagnosis Age'
plt.figure(figsize=(8, 6))
sns.violinplot(x='Disease-specific Survival status', y='Diagnosis Age', data=df, palette='husl')
plt.title('Violin Plot of Diagnosis Age by Survival Status')
plt.xlabel('Disease-specific Survival Status')
plt.ylabel('Diagnosis Age')
plt.show()

from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
import seaborn as sns
import matplotlib.pyplot as plt

# Assume selected_df is your original DataFrame
X = selected_df.drop('Disease-specific Survival status', axis=1)
y = selected_df['Disease-specific Survival status']

# Select categorical columns
categorical_columns = ['Cancer Type Detailed', 'Subtype', 'Tumor Type']

# Create a column transformer for one-hot encoding
preprocessor = ColumnTransformer(
    transformers=[
        ('onehot', OneHotEncoder(), categorical_columns)
    ],
    remainder='passthrough'
)

# Create a pipeline with preprocessing and SMOTE
pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('smote', SMOTE(random_state=42))
])

# Fit and transform the data using the pipeline
X_resampled, y_resampled = pipeline.named_steps['smote'].fit_resample(pipeline.named_steps['preprocessor'].fit_transform(X), y)

plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
y.value_counts().plot.pie(autopct='%1.1f%%', colors=['skyblue', 'salmon'], labels=None)
plt.title('Class Distribution Before SMOTE')

plt.subplot(1, 2, 2)
y_resampled.value_counts().plot.pie(autopct='%1.1f%%', colors=['skyblue', 'salmon'], labels=None)
plt.title('Class Distribution After SMOTE')


plt.show()

from sklearn.preprocessing import StandardScaler

X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import LabelEncoder

# Function to create a more complex neural network model
def create_complex_model(input_dim):
    model = Sequential()
    model.add(Dense(128, input_dim=input_dim, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(32, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(16, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(1, activation='sigmoid'))
    return model

# Function to compile the model
def compile_model(model):
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

# Instantiate LabelEncoder
le = LabelEncoder()

# Fit and transform labels
y_train_encoded = le.fit_transform(y_train)

# Create and compile the more complex model
input_dim = X_train_scaled.shape[1]
complex_model = create_complex_model(input_dim)
compiled_complex_model = compile_model(complex_model)

# Display model summary
compiled_complex_model.summary()

def create_different_activation_model(input_dim):
    model = Sequential()
    model.add(Dense(128, input_dim=input_dim, activation='elu'))
    model.add(Dropout(0.5))
    model.add(Dense(64, activation='elu'))
    model.add(Dropout(0.5))
    model.add(Dense(32, activation='elu'))
    model.add(Dropout(0.5))
    model.add(Dense(16, activation='elu'))
    model.add(Dropout(0.5))
    model.add(Dense(1, activation='sigmoid'))
    return model

different_activation_model = create_different_activation_model(input_dim)
compiled_different_activation_model = compile_model(different_activation_model)
compiled_different_activation_model.summary()

import numpy as np

# Assuming X_train_scaled and y_train_encoded are already defined

# Fit the model and track training history
history = compiled_complex_model.fit(
    X_train_scaled, np.array(y_train_encoded),
    epochs=50,
    batch_size=16,
    validation_split=0.3,
    verbose=1
)

import matplotlib.pyplot as plt

# Assuming 'history' is the object returned by model.fit

# Plot training and validation accuracy
plt.figure(figsize=(12, 4))

# Plot Accuracy
plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model Accuracy over Epochs')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend(['Train', 'Validation'], loc='upper left')
plt.ylim(0, 1)  # Set y-axis limits from 0 to 1 (0% to 100%)

# Plot Loss
plt.subplot(1, 2, 2)
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model Loss over Epochs')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend(['Train', 'Validation'], loc='upper left')

plt.tight_layout()
plt.show()

#FNN
def create_simple_model(input_dim):
    model = Sequential()
    model.add(Dense(64, input_dim=input_dim, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(32, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(1, activation='sigmoid'))
    return model

# Assuming X_train_scaled, y_train_encoded, and input_dim are already defined
simple_model_fnn = create_simple_model(input_dim)
compiled_simple_model_fnn = compile_model(simple_model_fnn)

history_simple_fnn = compiled_simple_model_fnn.fit(
    X_train_scaled, np.array(y_train_encoded),
    epochs=150,
    batch_size=16,
    validation_split=0.3,
    verbose=1
)

from tensorflow.keras.layers import LSTM

def create_lstm_model(input_dim, sequence_length):
    model = Sequential()
    model.add(LSTM(64, input_shape=(sequence_length, input_dim), activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(32, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(1, activation='sigmoid'))
    return model

# Assuming X_train_scaled, y_train_encoded, and input_dim are already defined
sequence_length = 6  # Adjust this to your desired sequence length

# Create and compile the LSTM model
lstm_model = create_lstm_model(input_dim, sequence_length)
compiled_lstm_model = compile_model(lstm_model)

# Reshape X_train_scaled for LSTM input
new_shape = (X_train_scaled.shape[0] // sequence_length, sequence_length, input_dim)
X_train_lstm = X_train_scaled[:new_shape[0] * sequence_length, :].reshape(new_shape)

# Train the LSTM model
history_lstm_model = compiled_lstm_model.fit(
    X_train_lstm,
    np.array(y_train_encoded),
    epochs=50,
    batch_size=16,
    validation_split=0.3,
    verbose=1
)

import matplotlib.pyplot as plt

# Assuming history_simple_50_epochs, history_lstm_50_epochs, and history_cnn_50_epochs are defined

# Plotting Accuracy for Simple FNN
plt.figure(figsize=(12, 4))

plt.subplot(1, 3, 1)
plt.plot(history_simple_fnn.history['accuracy'], label='Train')
plt.plot(history_simple_fnn.history['val_accuracy'], label='Validation')
plt.title('FNN Accuracy over Epochs ')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend(loc='upper left')
plt.ylim(0, 1)

# Plotting Accuracy for LSTM
plt.subplot(1, 3, 2)
plt.plot(history_lstm_model.history['accuracy'], label='Train')
plt.plot(history_lstm_model.history['val_accuracy'], label='Validation')
plt.title('LSTM Accuracy over Epochs ')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend(loc='upper left')
plt.ylim(0, 1)

