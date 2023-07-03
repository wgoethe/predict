#@@@@@@@@@Made by Goethe@@@@@@@@##

#########################################################################################################################################################
import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, SimpleRNN, LSTM
from sklearn.metrics import mean_squared_error
import math
import matplotlib.pyplot as plt
import tkinter as tk

#load the excel file and get the last col and row
df = pd.read_excel('1.xlsx')

last_column_index = df.shape[1] - 1
last_row_index = df.shape[0] - 1

#attributes MPR, CORRIDOR, CRR, LIQUIDITY RATIO
MAX_ATTRIBUTE = 4

MAX_NAME = 20

MAX_DATA = 50

TYPE = 3

#array of name
arr_name=[]

#array of data
arr2_data = []

#Check the name in the array and if new, append it into the array - if exist, return the index of it
def in_name(str):
    flag = arr_name.__contains__(str)
    if flag == True:
        return True, arr_name.index(str)
    else:
        arr_name.append(str)
        return False, arr_name.__len__() - 1

#Check as if str is a NAN
def is_NAN(str):
    if str == "nan":
        return True
    else:
        return False

#Check as if str is a MPR
def is_MPR(str):
    if str == "MPR":
        return True
    else:
        return False

#Convert the str into the pre-defined value
def convert(str):
    if str.__contains__("Raise") == True | str.__contains__("raise") :
        return 0
    elif str.__contains__("Retain") == True | str.__contains__("retain"):
        return 1
    elif str.__contains__("Reduce") == True | str.__contains__("reduce"):
        return 2
    else:
        return 3
    
#Convert x into an one-dimesnional array
def convert_M(x):
    if x == 0:
        return [1, 0, 0]
    elif x == 1:
        return [0, 1, 0]
    elif x == 2:
        return [0, 0, 1]


#Get the pre-data for analyzing from an excel file
for i in range(0, last_column_index + 1):
    string = str(df.iloc[0:1, i:i + 1].values[0][0])
    # print(string)
    if is_MPR(string) == True:
        for row in range(1, last_row_index + 1):
            new_data = []
            name_index = 0
            is_new = False
            for col in range(i - 1, i + MAX_ATTRIBUTE):
                cell = str(df.iloc[row:row + 1, col:col + 1].values[0][0])
                if col == i - 1:
                    if is_NAN(cell) == True:
                        break
                    name_info = in_name(cell)
                    name_index = name_info[1]
                    is_new = name_info[0]
                    if is_new == False:
                        arr2_data.append([])
                elif col == i - 1 + MAX_ATTRIBUTE:
                    if is_NAN(cell) == False:
                        new_data.append(convert(cell))
                        arr2_data[name_index].append(new_data)
                    else:
                        break      
                else:
                    if is_NAN(cell) == False:
                        new_data.append(convert(cell))
                    else:
                        break


###################################Select###################################
data = []

for i in range(len(arr2_data[0])):
    data.append(convert_M(arr2_data[0][i][0]))

# print(data)


#Extract the data_x and data_y from the given data
    #@{dat}@ raw data
    #@{TIME_STEPS}@ time steps

def get_XY(dat, TIME_STEPS):
    dat = np.array(dat)
    Y_ind = np.arange(TIME_STEPS, len(dat), TIME_STEPS)
    Y = dat[Y_ind]
    rows_x = len(Y)
    X = dat[range(TIME_STEPS*rows_x)]
    X = np.reshape(X, (rows_x, TIME_STEPS, TYPE))    
    return X, Y
 
#Create the RNN 
    #@{hidden_units}@ number of the units in the hidden layer
    #@{dense_units}@ number of the units in the output layer
    #@{input_shape}@ dimension of the inputs
    #@{activation}@ the array of the activate functions

def create_RNN(hidden_units, dense_units, input_shape, activation):
    model = Sequential()
    model.add(LSTM(hidden_units, input_shape=input_shape, activation=activation[0]))
    model.add(Dense(units=dense_units, activation=activation[1]))
    model.compile(loss='mean_squared_error', optimizer='adam')
    return model
 
# def print_error(trainY, testY, train_predict, test_predict):    
#     # Error of predictions
#     train_rmse = math.sqrt(mean_squared_error(trainY, train_predict))
#     test_rmse = math.sqrt(mean_squared_error(testY, test_predict))
#     # Print RMSE
#     print('Train RMSE: %.3f RMSE' % (train_rmse))
#     print('Test RMSE: %.3f RMSE' % (test_rmse))    
 
# Plot the result
# def plot_result(trainY, testY, train_predict, test_predict):
#     actual = np.append(trainY, testY)
#     predictions = np.append(train_predict, test_predict)
#     rows = len(actual)
#     plt.figure(figsize=(15, 6), dpi=80)
#     plt.plot(range(rows), actual)
#     plt.plot(range(rows), predictions)
#     plt.axvline(x=len(trainY), color='r')
#     plt.legend(['Actual', 'Predictions'])
#     plt.xlabel('Observation number after given time steps')
#     plt.ylabel('Votes')
#     plt.title('Actual and Predicted Values. The Red Line Separates The Training And Test Examples')
 
TIME_STEPS = 10 



 
# Create model and train
model = create_RNN(hidden_units=3, dense_units=TYPE, input_shape=(TIME_STEPS,TYPE), 
                   activation=['tanh', 'softmax'])



for i in range(len(data) - TIME_STEPS):
    train_data = data[i: i + TIME_STEPS + 1]
    trainX, trainY = get_XY(train_data, TIME_STEPS)
    model.fit(trainX, trainY, epochs=20, batch_size=1, verbose=2)
 
test_data = np.array(data[-TIME_STEPS:])
test_data = np.reshape(test_data, (1, TIME_STEPS, TYPE)) 

# make predictions
train_predict = model.predict(test_data)

print(train_predict)