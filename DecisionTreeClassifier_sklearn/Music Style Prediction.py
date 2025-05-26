
"""
Created on Thu Aug 22 17:02:45 2024

@author: timofeevam
"""

import pandas as pd
#import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib 
from sklearn import tree
import pydotplus
from IPython.display import Image

music_data = pd.read_csv('music.csv')

'''
# to explore the data 
print(music_data)
print(music_data.describe()) # Basic data information
print(music_data.values) # First several rows of the data
'''


# To train the model 
X = music_data.drop(columns=['genre']) # create framework without 'genre' colunm
Y = music_data['genre']
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.2) # best practise is train/test = 80/20
model = DecisionTreeClassifier()
model.fit(X_train.values, Y_train)

# To save the trained model
joblib.dump(model, 'model_trained.joblib')

# To visualise the model
tree.export_graphviz(model, out_file = 'Graph_music_model.dot', feature_names=['age', 'gender'],
                     class_names = sorted(Y_train.unique()), label = 'all',
                     rounded = True, filled = True)

with open('Graph_music_model.dot', 'r') as file:
    dot_data = file.read()

graph = pydotplus.graph_from_dot_data(dot_data) # Converts the DOT data into a graph object
image = graph.create_png() # Converts the graph into a PNG image

with open("Graph_music_model.png", "wb") as f:
    f.write(image)



# To load the saved trained model and further input the arguments
model = joblib.load('model_trained.joblib')

prediction = model.predict([[21,1],[22,0]]) # input: 21 old man, 22 old women
print(prediction)


'''
#To predict accuracy based on the available Test data
prediction = model.predict(X_test)
score = accuracy_score(Y_test, prediction)
print(score)
'''
