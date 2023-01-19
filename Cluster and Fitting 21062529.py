# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 12:46:00 2023

@author: Puneet
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy as sts
from sklearn.cluster import KMeans
import seaborn as sns
from sklearn import preprocessing
import scipy.optimize as opts

"""Reading manipulating file with country name
and returning a dataframe and transpose of the dataframe as return"""
def dataFrame(file_name, col, value1,countries):
    # Reading Data for dataframe
    df = pd.read_csv(file_name, skiprows = 4)
    # Grouping data with col value
    df1 = df.groupby(col, group_keys = True)
    #retriving the data with the all the group element
    df1 = df1.get_group(value1)
    #Reseting the index of the dataframe
    df1 = df1.reset_index()
    #Storing the column data in a variable
    a = df1['Country Name']
    # cropping the data from dataframe
    df1 = df1.iloc[countries,3:]
    df1 = df1.drop(columns=['Indicator Name', 'Indicator Code'])
    df1.insert(loc=0, column='Country Name', value=a)
    #Dropping the NAN values from dataframe Column wise
    df1= df1.dropna(axis = 1)
    #transposing the index of the dataframe
    df2 = df1.set_index('Country Name').T
    #returning the normal dataframe and transposed dataframe
    return df1, df2

# years using for the data analysis

# countries which are using for data analysis
countries = [35, 55, 81, 109]
'''calling dataFrame functions for all the dataframe which will be used for visualization'''
ele_con_c, ele_con_y = dataFrame("API_19_DS2_en_csv_v2_4700503.csv",
                                       "Indicator Name", "Electric power consumption (kWh per capita)",
                                       countries)

print(ele_con_c,)

#GDP_capita_y=GDP_capita_y.drop('Country Code',axis=0)
print(ele_con_y)

#returns a numpy array as x
x = ele_con_y.values

min_max_scaler = preprocessing.MinMaxScaler()
x_scaled = min_max_scaler.fit_transform(x)
normalized_df= pd.DataFrame(x_scaled)

print(normalized_df)

wcss = []
for i in range(1, 10):
    kmeans = KMeans(n_clusters = i,init = 'k-means++', max_iter = 300, n_init = 10, random_state = 0)
    kmeans.fit(normalized_df)
    wcss.append(kmeans.inertia_)

print(wcss)

plt.figure()
plt.plot(range(1, 10), wcss)
plt.title('The elbow method')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS') #within cluster sum of squares
plt.show()

kmeans = KMeans(n_clusters = 3, init = 'k-means++', max_iter = 100, n_init = 10, random_state = 0)
y_kmeans = kmeans.fit_predict(normalized_df)

print(y_kmeans)

lables = kmeans.fit_predict(normalized_df)
centroids= kmeans.cluster_centers_

print('centroids=',centroids)


plt.figure()
plt.scatter(normalized_df.values[y_kmeans == 0, 0], normalized_df.values[y_kmeans == 0, 1], s = 100, c = 'green', label = 'Cluster1')
plt.scatter(normalized_df.values[lables == 1, 0], normalized_df.values[lables == 1, 1], s = 100, c = 'orange', label = 'Cluster2')
plt.scatter(normalized_df.values[lables == 2, 0], normalized_df.values[lables == 2, 1], s = 100, c = 'purple', label = 'Cluster3')
plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], s=100, c='red', label = 'Centroids')
plt.legend()
plt.title('Clusters of GDP per Capita of 3 countries')
plt.xlabel('Years')
plt.ylabel('GDP per year')
plt.show()


'''calling dataFrame functions for all the dataframe which will be used for visualization'''
school_c, school_y = dataFrame("API_19_DS2_en_csv_v2_4700503.csv",
                                       "Indicator Name", "School enrollment, primary and secondary (gross), gender parity index (GPI)",countries)
school_y['years'] = school_y.index


school_y.plot(y='India',use_index=True)

def exponential(t, n0, g):
    """Calculates exponential function with scale factor n0 and growth rate g."""
    t = t - 1960.0
    f = n0 * np.exp(g*t)
    return f

print(type(school_y["years"].iloc[1]))
school_y["years"] = pd.to_numeric(school_y["years"])
print(type(school_y["years"].iloc[1]))
param, covar = opt.curve_fit(exponential, school_y["years"], school_y["India"],
p0=(73233967692.102798, 0.03))

school_y["fit"] = exponential(school_y["years"], *param)
school_y.plot("years", ["India", "fit"])
plt.show()
