#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 20 09:55:00 2022

@author: josepabloceballos
"""

import csv
import pandas as pd
import matplotlib.pyplot as plt


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
    df = pd.read_csv(path)
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

df = saveCsvtoDf(path)
plt = plotData(df)
print(plt)
plt.draw()
