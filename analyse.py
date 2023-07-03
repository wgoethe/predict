
import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, SimpleRNN, LSTM
from sklearn.metrics import mean_squared_error
import math
import matplotlib.pyplot as plt

TYPE = 3

MAX_ATTRIBUTE = 4

TIME_STEPS = 3

class Analyse():
    def __init__(self):
        self.file_path = None
        self.arr_name = []
        self.arr_data = []

    def setExcel(self, str):
        self.file_path = str
        self.loadData()

    def getExcel(self):
        return self.file_path

    #Check the name in the array and if new, append it into the array - if exist, return the index of it
    
    def in_name(self, str):
        flag = self.arr_name.__contains__(str)
        if flag == True:
            return True, self.arr_name.index(str)
        else:
            self.arr_name.append(str)
            return False, self.arr_name.__len__() - 1

    #Check as if str is a NAN

    def is_NAN(self, str):
        if str == "nan":
            return True
        else:
            return False
        
    #Check as if str is a MPR

    def is_MPR(self, str):
        if str == "MPR":
            return True
        else:
            return False

    #Convert the str into the pre-defined value

    def convert(self, str):
        if str.__contains__("Raise") == True | str.__contains__("raise") :
            return 0
        elif str.__contains__("Retain") == True | str.__contains__("retain"):
            return 1
        elif str.__contains__("Reduce") == True | str.__contains__("reduce"):
            return 2
        else:
            return 1
        
    #Convert x into an one-deimensional array
        
    def convert_M(self, x):
        if x == 0:
            return [1, 0, 0]
        elif x == 1:
            return [0, 1, 0]
        elif x == 2:
            return [0, 0, 1]

    #Load all data from the excel file
    
    def loadData(self):
        df = pd.read_excel(self.file_path)
        last_column_index = df.shape[1] - 1
        last_row_index = df.shape[0] - 1

        for i in range(0, last_column_index + 1):
            string = str(df.iloc[0:1, i:i + 1].values[0][0])
            # print(string)
            if self.is_MPR(string) == True:
                for row in range(1, last_row_index + 1):
                    new_data = []
                    name_index = 0
                    is_new = False
                    for col in range(i - 1, i + MAX_ATTRIBUTE):
                        cell = str(df.iloc[row:row + 1, col:col + 1].values[0][0])
                        if col == i - 1:
                            if self.is_NAN(cell) == True:
                                break
                            name_info = self.in_name(cell)
                            name_index = name_info[1]
                            is_new = name_info[0]
                            if is_new == False:
                                self.arr_data.append([])
                        elif col == i - 1 + MAX_ATTRIBUTE:
                            if self.is_NAN(cell) == False:
                                new_data.append(self.convert(cell))
                                self.arr_data[name_index].append(new_data)
                            else:
                                break      
                        else:
                            if self.is_NAN(cell) == False:
                                new_data.append(self.convert(cell))
                            else:
                                break


    def get_names(self):
        return self.arr_name
    
    def get_XY(self, dat, TIME_STEPS):
        dat = np.array(dat)
        Y_ind = np.arange(TIME_STEPS, len(dat), TIME_STEPS)
        Y = dat[Y_ind]
        rows_x = len(Y)
        X = dat[range(TIME_STEPS*rows_x)]
        X = np.reshape(X, (rows_x, TIME_STEPS, TYPE))    
        return X, Y
    
    def create_RNN(self, hidden_units, dense_units, input_shape, activation):
        model = Sequential()
        model.add(LSTM(hidden_units, input_shape=input_shape, activation=activation[0]))
        model.add(Dense(units=dense_units, activation=activation[1]))
        model.compile(loss='mean_squared_error', optimizer='adam')
        return model

    def predict(self, index, iter):
        data = []

        for i in range(len(self.arr_data[index])):
            data.append(self.convert_M(self.arr_data[index][i][iter]))

        print(data)

        model = self.create_RNN(hidden_units = 3, dense_units = TYPE, input_shape=(TIME_STEPS,TYPE), activation=['tanh', 'softmax'])
    
        # for i in range(len(data) - TIME_STEPS):
        #     train_data = data[i: i + TIME_STEPS + 1]
        #     trainX, trainY = self.get_XY(train_data, TIME_STEPS)
        #     model.fit(trainX, trainY, epochs=10, batch_size=1, verbose=2)

        trainX, trainY = self.get_XY(data, TIME_STEPS)
        model.fit(trainX, trainY, epochs=100, batch_size=1, verbose=2)
    
        test_data = np.array(data[-TIME_STEPS:])
        test_data = np.reshape(test_data, (1, TIME_STEPS, TYPE)) 

        # make predictions
        train_predict = model.predict(test_data)

        return train_predict