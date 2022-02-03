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


def plotData(df):
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
    for i,value in enumerate(range(size)):
   
        if((i+1)<size):
            lat0 = df['X'][i]
            lat1 = df['X'][i+1]
            lon0 = df['Y'][i]
            lon1 = df['Y'][i+1]
            d = calculteDistance(lat0, lon0, lat1, lon1) 
            print('m=',d*1000)
            newList.append((d*1000,df['Z'][i]))
    return newList
            
            
        
def calculteDistance(lat1,lon1,lat2,lon2):

    dist = mpu.haversine_distance((lat1, lon1), (lat2, lon2))
    print(dist)

    return dist


#some comment
#comment for Stevie 
    

# # Point one
# lat1 = 52.2296756
# lon1 = 21.0122287

# # Point two
# lat2 = 52.406374
# lon2 = 16.9251681



df = saveCsvtoDf(path)
a = dataTo2d(df)
#a =calculteDistance(lat1,lon1,lat2,lon2)

fig = plotData(df)

