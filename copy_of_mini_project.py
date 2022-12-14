# -*- coding: utf-8 -*-
"""Copy of Mini_Project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1z5cXwA8XWVS1x1N6RA6XRazP40COKNmE

# **Introduction to Data Science Workshop Mini-Project**
"""

# Import libraries
import io
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn import tree
from sklearn import metrics

# Load dataset
dataset = pd.read_csv('./chicago_dataset.csv')
dataset.head()

"""
### **Part 1: Descriptive Statistics**
Computing Mean, Median, and Quartiles
"""

def computeStats():
    # Compute the mean of your assigned variable
    print(dataset["Below Poverty Level"].mean())
    
    # Compute the median of your assigned variable
    print(dataset["Below Poverty Level"].median())
    
    # Compute the first, second, and third quartile of your assigned variable
    print(dataset["Below Poverty Level"].quantile([0.25,0.50,0.75]))
    
    # Compute all descriptive statistics for Chicago's community areas
    dataset.describe()


"""
### **Part 2: Data Visualization**
Making Bar Charts, Scatter Plots, and Boxplots
"""

# Sort dataset by assigned variable
dataset = dataset.sort_values("Below Poverty Level")
dataset.head()


def plot_figures():
    '''
    Makes a plot of Below poverty Level category vs all other categories

    Returns
    -------
    None.

    '''
    plt.figure(figsize=(20,5)) # Set figure size (if needed)
    for column in dataset.columns:
        if column != "Below Poverty Level":
            plt.figure(figsize=(20,5))
            ax = sns.barplot(x = column, y ="Below Poverty Level", data = dataset, ci = None) # Make bar chart
            ax.set(title ="Plot of " + column + " vs below poverty level", xlabel = column, ylabel ="Below Poverty Level") # Set chart title and axis labels
            ax.tick_params(axis='x', rotation=90) # Rotate x-axis labels (if needed)
            plt.show()

    # Make scatter plot of assigned variable vs all other categories
    for column in dataset.columns:
        if column != "Below Poverty Level":
            ax = sns.scatterplot(x = column, y ="Below Poverty Level", data = dataset) # Make scatter plot
            ax.set(title ="Plot of " + column + " vs Below Poverty Level", xlabel =column , ylabel ="Below Poverty Level") # Set chart title and axis labels
            plt.show()

    # Make box plot of your assigned variable
    ax = sns.boxplot(y ="Below Poverty Level", data = dataset) # Make box plot
    ax.set(title ="Below Poverty Level BoxPlot", ylabel ="Below Poverty Level")
    plt.show()

"""### **Part 3: Classification**
Training and Testing Decision Trees

**Create class label**
"""

            # mini excercise
def miniExcercise():
    True_list = [1,1,0,1,0,0,1,1,0,0]
    Predicted_list = [1,1,0,0,1,0,1,0,1,1]

    # build our matrix 
    # Test for our predictions 
    confusion_matrix = metrics.confusion_matrix(True_list, Predicted_list)
    accuracy = metrics.accuracy_score(True_list, Predicted_list)

    print(accuracy)
    print(1 - accuracy)

# Create class label for your assigned variable (based on chosen cut-off value)
def create_class_label (row):
    cutoff = 27.0
    if row["Below Poverty Level"] > cutoff:
        return 1 # value of assigned variable > cutoff
    return 0 # value of assigned varlue <= cutoff

dataset['Class Label'] = dataset.apply(lambda row: create_class_label (row), axis = 1)
dataset.head()

"""**Divide the dataset into a training set (75% of the data) and a test set (25% of the data).**"""

# Partition dataset into training and test sets
# columns = [column for column in dataset.columns[1:] if column != "Below Poverty Level"]
# x_train, x_test, y_train, y_test = train_test_split(dataset[columns],
#                                                     dataset["Class Label"],
#                                                     test_size = 0.25,
#                                                     random_state = 1)

x_train, x_test, y_train, y_test = train_test_split(dataset[["Teen Birth Rate",  "Crowded Housing" , "Unemployment", "No High School Diploma"]],
                                                    dataset["Class Label"],
                                                    test_size = 0.25,
                                                    random_state = 1)  # (predictors, class, test size, random state)

"""**<u>Using the training set</u>, build a decision tree to predict the class label based on the predictors.**"""

# Build decision tree
model = tree.DecisionTreeClassifier()
model.fit(x_train, y_train) # (predictors, class)

# Plot decision tree
# plt.figure(figsize = (15,15)) # Set figure size (if needed)
# tree.plot_tree(model, feature_names = columns,      # feature_names indicates the names of the predictors
#                class_names = ["<= 27.0", ">27.0"],               # class_names indicates the names of the classes
#                filled = True, impurity = False)

plt.figure(figsize = (15,15)) # Set figure size (if needed)
tree.plot_tree(model, feature_names = ["Teen Birth Rate",  "Crowded Housing" , "Unemployment", "No High School Diploma"],      # feature_names indicates the names of the predictors
                class_names = ["<= 27.0", ">27.0"],               # class_names indicates the names of the classes
                filled = True, impurity = False)
plt.show()
# IMPORTANT: class names must be given in ascending order

"""**Evaluate the performance of this decision tree <u>on the test set</u>.** """

# Predict class labels for test set
y_pred = model.predict(x_test)
print(y_pred) # Print predicted class labels

# Plot confusion matrix
conf_matrix = metrics.confusion_matrix(y_test, y_pred) # Create confusion matrix
sns.heatmap(conf_matrix, annot = True, fmt = ".3f", square = True, cmap = plt.cm.Blues) # Plot confusion matrix
plt.ylabel('True') # Set y-axis label
plt.xlabel('Predicted') # Set x-axis label
plt.title('Confusion matrix') # Set chart title
plt.tight_layout()

# Compute evaluation metrics
print(metrics.accuracy_score(y_test, y_pred)) # Compute accuracy
print(1 - metrics.accuracy_score(y_test, y_pred)) # Compute error
