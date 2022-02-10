#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 20 09:55:00 2022

@author: josepabloceballos
"""

import csv
import pandas as pd
import matplotlib.pyplot as plt
import mpu
from rdp import rdp
import numpy as np


#path = '../InputData/ww_ten_points.csv'
print('Input .csv file path ../InputData/ww_ten_points.csv')
#path = input()
path = '../InputData/ww_ten_points.csv'


def showFileContents(path):
    
    with open(path, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            print(', '.join(row))
    
    return

def saveCsvtoDf(path):
    df = pd.read_csv(path, usecols= ['Z','X','Y'])
    return df


def customePlotData(df):
    x = df.X
    y = df.Y
    z = df.Z
    fig = plt.figure(figsize=(6, 6))
    ax = plt.axes(projection='3d')
    ax = fig.add_subplot(111, projection='3d')
    ax.plot3D(x, y, z, 'gray')
    ax.scatter3D(x, y,z,
           linewidths=1, alpha=.7,
           edgecolor='k',
           cmap='Greens',
           s = 100,
           c=z)
    ax.view_init(30, 0)
    for angle in range(0, 1):
        ax.view_init(30, angle)
        plt.draw()
        plt.pause(300)
    return fig


def dataTo2d(df):
    size = df.shape[0]
    newList = []
    
    startX = df['X'][0]
    startY = df['Y'][0]
    for i,value in enumerate(range(size)):
   
        if((i+1)<size):
            lat0 = df['X'][i]
            lat1 = df['X'][i+1]
            lon0 = df['Y'][i]
            lon1 = df['Y'][i+1]
            d = calculteDistance(startX, startY, lat1, lon1) 
            #print('m=',d*1000,lat0, lon0, lat1, lon1)
            newList.append((d*1000,df['Z'][i]))
    return newList
            
            
        
def calculteDistance(lat1:float,lon1:float,lat2:float,lon2:float):

    dist = mpu.haversine_distance((lat1, lon1), (lat2, lon2))
    print(dist)

    return dist


def customPlot(lst:list):
    x = []
    y = []
    general = []
    for i,element in enumerate(lst):
        x.append(lst[i][0])
        y.append(lst[i][1])
        general.append(lst[i][0])
        general.append(lst[i][1])
    x.reverse()
    y.reverse()
    #print(general)
    return  plt.scatter(x,y)

def dfToListXYZ(df):
    size = df.shape[0]
    general = []
    
    for i,elemnt in enumerate(range(size)):
        general.append(df['X'][i])
        general.append(df['Y'][i])
        general.append(df['Z'][i])
    return general

def dfToListXY(df):
    size = df.shape[0]
    general = []
    
    for i,elemnt in enumerate(range(size)):
        general.append(df['X'][i])
        general.append(df['Y'][i])
    return general

def fromArrayToDF(arr):
    df = pd.DataFrame(data=arr, columns=["X", "Y","Z"])
    return df

def simplifyDf3D(df,epsilon:float):
    lst = dfToListXYZ(df)
    M = np.array(lst).reshape(10, 3)
    simplyfiedM = rdp(M,epsilon)
    newDf = fromArrayToDF(simplyfiedM)
    return newDf

    
#add this simplify segment --> df X,Y,Z ---> df same shape X,Y,Z

# passes a the data 

df = saveCsvtoDf(path)

#Makes the data into 2d
a = dataTo2d(df)


#implements simplidication

b = simplifyDf3D(df,0.001)

#fig = customePlotData(b)
#fig2 = customePlotData(df)


#customPlot(a)

