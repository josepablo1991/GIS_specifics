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
#from rdp import rdp
from ramer_douglas_peuker import rdp
import numpy as np
from scipy import interpolate


#path = '../InputData/ww_ten_points.csv'
print('Input .csv file path ../InputData/ww_ten_points.csv')
#path = input()
path = '../InputData/ww_ten_points.csv'

path2 = './input_test_points.csv'



def showFileContents(path):
    
    with open(path, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            print(', '.join(row))
    
    return

def saveCsvtoDf(path):
    df = pd.read_csv(path, usecols= ['r_id','Z','X','Y'])
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
      
        general.append(df['X'].iloc[i])
        general.append(df['Y'].iloc[i])
        general.append(df['Z'].iloc[i])
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
    
    reshapeSize = int(len(lst)/3)
    M = np.array(lst).reshape(reshapeSize, 3)
    simplyfiedM = rdp(M,epsilon)
    newDf = fromArrayToDF(simplyfiedM)
    return newDf


#This function is responsible for restoring the simplyfied segment to its original form but with 
#interpolated Z values with simple line interpolation
def refilldf(newdf,olddf):
    newSize = newdf.shape[0]
    resetedDf =olddf.assign(Z=0)
    oldSize = resetedDf.shape[0]
    x = newdf.loc[:,('X')].tolist()
    y = newdf.loc[:,('Y')].tolist()
    z = newdf.loc[:,('Z')].tolist()
    funtion = getInterpolateFunction(x,y,z,oldSize)
    step = getStep(z,oldSize)
    trend = step > 0 

    #b = pd.concat([newdf,a]).drop_duplicates().reset_index(drop=True)
    for i,element in enumerate(range(oldSize)):
        for j,newElement in enumerate(range(newSize)):
            if(resetedDf['X'].iloc[i] == newdf['X'].iloc[j] and resetedDf['Y'].iloc[i] == newdf['Y'].iloc[j]):
                resetedDf.loc[resetedDf.index[i],('Z')] = newdf.loc[newdf.index[j],('Z')]    
        
    #Refilling empty segment table
    resetDfSize = resetedDf.shape[0]
    for i,element in enumerate(range(resetDfSize)):
        if(resetedDf.loc[resetedDf.index[i],('Z')] == 0 ):
            a = funtion(resetedDf.loc[resetedDf.index[i],('X')])
            prev = resetedDf.loc[resetedDf.index[i-1],('Z')]
            #resetedDf.loc[resetedDf.index[i],('Z')] = resetedDf.loc[resetedDf.index[0],('Z')] + step*(i-1)
            if(trend and a<prev):
                resetedDf.loc[resetedDf.index[i],('Z')] = a
            elif(trend and a > prev): 
                resetedDf.loc[resetedDf.index[i],('Z')] =  resetedDf.loc[resetedDf.index[i-1],('Z')]
            elif(not trend and a < prev):
                resetedDf.loc[resetedDf.index[i],('Z')] = a
            else:
                resetedDf.loc[resetedDf.index[i],('Z')] =  resetedDf.loc[resetedDf.index[i-1],('Z')]


    return resetedDf

def getInterpolateFunction(x,y,z,size):
    
    f = interpolate.interp1d(x, z,fill_value="extrapolate")
    return f

def getStep(z,size):
    d =  z[0]- z[-1]
    step = d/size
    return step
    

#implements simplidication of segment

def simplifySegmentXYZ(df):
    a = simplifyDf3D(df,0.0005)
    b = refilldf(a,df)
    return b


# Creates a flag for each node, marking those that have to be preserved.
# 0 = No reason to be kept and therefore can be replaced with interpolated values.
# 1 = Has an overlapping node and therefore its elevation has to be preserved.
# 2 = Is a start/end point and therefore its elevation has to be preserved.
def keepFlag(df): 
    groupedRiver = df.groupby('r_id')
    startsEnds = pd.concat([groupedRiver.head(1), groupedRiver.tail(1)])
    oids = [i for i in startsEnds.index]
    df['keepFlag'] = np.where(df.duplicated(['X', 'Y'], keep=False), 1, 0)
    df['keepFlag'] = np.where(df.index.isin(oids), 2, df['keepFlag'])
    return df


# Marks the r_id to which the node is connected to. 
# 0 means that the node has no other connections other than its own river. 
def connectedR(df):
    for i in df.index:
        x = df.at[i, 'X']
        y = df.at[i, 'Y']
        if df.at[i, 'keepFlag'] != 0:
            targetRow = df.loc[(df['X'] == x) & (df['Y'] == y) & (df.index != i)]
            targetCell = targetRow.r_id.tolist()
            if targetCell == []:
                df.at[i, 'connectedR'] = 0
            else:
                df.at[i, 'connectedR'] = targetCell[0]
        else:
            df.at[i, 'connectedR'] = 0
    return df


# If keepFlag = 1, select a row where:
# "the original row's connectedR = the target row's r_id" 
# & "the original row's r_id = the target row's connectedR"
# Update the Z with the target row's.
def updateIntersection(df):
    for i in df.index:
        if df.at[i, 'keepFlag'] == 1:
            orid = df.at[i, 'r_id']
            ocr = df.at[i, 'connectedR']
            targetRow = df.loc[(df['r_id'] == ocr) & (df['connectedR'] == orid)]
            originalZ = targetRow.Z.tolist()
            df.at[i, 'Z'] = originalZ[0]
        else:
            pass
    return df
        
def makeSegmentBlocks(df):
    #list of segments
    segments = df['r_id'].unique()
    segmentsList = []
    for segmentValue in segments:
        segmentDf = df.loc[df['r_id'] == segmentValue]
        simplyfiedSegment = simplifySegmentXYZ(segmentDf[['X','Y','Z']])
        simplyfiedSegment['r_id'] = segmentValue
        segmentsList.append(simplyfiedSegment)
    simplyfiedSegments = pd.concat(segmentsList)
    return simplyfiedSegments
        
#add the code from the algorythm from the rdp PENDING
#make the df fill again with interpolated values.  DONE
#add this simplify segment --> df X,Y,Z ---> df same shape X,Y,Z 

# passes a the data 

df = saveCsvtoDf(path2)

#sa = keepFlag(df);


#Makes the data into 2d
#a = dataTo2d(df)

#implements simplidication THIS IS the function you need to use Stevie


b = makeSegmentBlocks(df)
c = keepFlag(b)
d = connectedR(c)
e = updateIntersection(d)

#b = simplifySegmentXYZ(df)

#fig = customePlotData(df)
#fig2 = customePlotData(e)




#customPlot(a)
