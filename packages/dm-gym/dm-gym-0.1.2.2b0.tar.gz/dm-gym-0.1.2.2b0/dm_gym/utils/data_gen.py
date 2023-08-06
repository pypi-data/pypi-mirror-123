import math
from statistics import mean

import random

import numpy as np
import pandas as pd

from copy import deepcopy

import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression
from sklearn.cluster import MeanShift


class data_gen_clustering():

    def __init__(self):
        pass

    def param_init(self, n, k, num_records, parameter_means=[], parameter_sd=[]):
        error = ""
        error_code = 0

        if(n <= 0):
            error_code = 1
            error = "number of features has to be greater than or equal to 1"
        
        elif(k <= 0):
            error_code = 6
            error = "number of clusters has to be greater than or equal to 1"

        elif(len(parameter_means) > 0 and len(parameter_means) != n):
            error_code = 2
            error = "parameters means specified are not of correct length"
            
        elif(len(parameter_means) > 0 and len(parameter_means[0]) != k):
            error_code = 3
            error = "parameters means specified are not of correct length"

        elif(len(parameter_sd) > 0 and len(parameter_sd) != n):
            error_code = 4
            error = "parameters std deviation specified are not of correct length"

        elif(len(parameter_sd) > 0 and len(parameter_sd[0]) != k):
            error_code = 5
            error = "parameters std deviation specified are not of correct length"

        if(error_code == 0):
            self.n = n
            self.k = k
            self.num_records = num_records

            if(len(parameter_means) == n):
                self.parameter_means = parameter_means
            else:
                self.parameter_means = []
                for i in range(n):
                    l = (np.arange(k) * k).tolist()
                    np.random.shuffle(l)
                    self.parameter_means.append(l)

            if(len(parameter_sd) == n):
                self.parameter_sd = parameter_sd
            else:
                self.parameter_sd = (np.ones((n, k))).tolist()

        return error, error_code, self.parameter_means, self.parameter_sd

    def gen_data(self):
            
        final_data = []
        
        for i in range(self.k):
            temp_data = []
            for j in range(self.n):
                data = np.random.normal(self.parameter_means[j][i], self.parameter_sd[j][i], int(self.num_records/self.k))
                temp_data.append(data)
            final_data = final_data + np.transpose(np.array(temp_data)).tolist()
        
        columns = list(range(1,self.n+1))
        self.df = pd.DataFrame(data=final_data, columns=columns)

        return self.df
    

    def gen_model(self, data):

        X = data.to_numpy()

        model = MeanShift(bandwidth=2)

        reg = model.fit(X)
        
        model_labels = reg.labels_
        
        final_data = deepcopy(data)
        final_data['Class'] = model_labels
        
        centroids = model.cluster_centers_
        
        centroids = [tuple(coords) for coords in centroids]
            
        return final_data, centroids
    
class data_gen_LR():

    def __init__(self):
        pass

    def param_init(self, n, r2, num_records, parameter_vals=[], parameter_means=[], parameter_sd=[]):
        error = ""
        error_code = 0

        if(n <= 0):
            error_code = 1
            error = "number of features has to be greater than or equal to 1"

        elif(len(parameter_vals) > 0 and len(parameter_vals) != n+1):
            error_code = 3
            error = "parameters specified are not of correct length"

        elif(len(parameter_means) > 0 and len(parameter_means) != n):
            error_code = 4
            error = "parameters means specified are not of correct length"

        elif(len(parameter_sd) > 0 and len(parameter_sd) != n):
            error_code = 5
            error = "parameters std deviation specified are not of correct length"

        elif(r2 > 1 or r2 < 0.1):
            error_code = 2
            error = "r2 value has to be in the range (0.1 , 1)"

        if(error_code == 0):
            self.n = n
            self.r2 = r2
            self.num_records = num_records

            if(len(parameter_vals) == n+1):
                self.parameter_vals = parameter_vals
            else:
                self.parameter_vals = (np.random.randint(
                    low=-10, high=10, size=n+1)).tolist()

            if(len(parameter_means) == n):
                self.parameter_means = parameter_means
            else:
                self.parameter_means = (np.zeros(n)).tolist()

            if(len(parameter_sd) == n):
                self.parameter_sd = parameter_sd
            else:
                self.parameter_sd = (np.ones(n)).tolist()

        return error, error_code

    def gen_features(self):

        data = []

        for i in range(self.n):
            feature = np.random.normal(
                0, 1, self.num_records).tolist()
            data.append(feature)

        return data

    def gen_target(self, X):

        y = self.parameter_vals[0]

        for i in range(self.n):
            y = y + self.parameter_vals[i+1] * X[i]

        return y

    def gen_target_with_noise(self, Y, e):

        new_Y = []

        for y in Y:
            new_Y.append(y + np.random.normal(0, e/math.sqrt(self.r2)))

        return new_Y

    def gen_std_data(self):

        data = np.array(self.gen_features())

        Y = []
        for i in range(self.num_records):

            X = []
            for j in range(self.n):
                X.append(data[j][i])

            Y.append(self.gen_target(X))

        e = self.expected_noise(Y)
        Y = self.gen_target_with_noise(Y, e)

        data = data.tolist()
        data.append(Y)
        data = np.array(data)
        data = data.T
        data = data.tolist()

        columns = np.arange(1, self.n+1).tolist()
        columns.append('Y')

        self.df = pd.DataFrame(data=data, columns=columns)

        return self.df

    def gen_data(self):

        data = np.array(self.gen_features())

        for i in range(self.n):
            data[i] = data[i] * self.parameter_sd[i] + self.parameter_means[i]

        Y = []
        for i in range(self.num_records):

            X = []
            for j in range(self.n):
                X.append(data[j][i])

            Y.append(self.gen_target(X))

        e = self.expected_noise(Y)
        Y = self.gen_target_with_noise(Y, e)

        data = data.tolist()
        data.append(Y)
        data = np.array(data)
        data = data.T
        data = data.tolist()

        columns = np.arange(1, self.n+1).tolist()
        columns.append('Y')

        self.df = pd.DataFrame(data=data, columns=columns)

        return self.df

    def expected_noise(self, Y):
        e = (1 - self.r2)/self.num_records

        temp = 0
        y_mean = mean(Y)

        for i in range(self.num_records):
            temp = temp + (Y[i] - y_mean)**2

        e = e * temp
        e = math.sqrt(e)

        return e

    def gen_model(self, data):

        X = data.drop(columns=['Y']).to_numpy()
        Y = data['Y'].to_numpy()

        model = LinearRegression()

        reg = model.fit(X, Y)

        model_r2 = reg.score(X, Y)
        model_coef = reg.coef_
        model_intercept = reg.intercept_

        return model_r2, model_coef, model_intercept
