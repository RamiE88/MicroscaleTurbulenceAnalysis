'''


This code was based off of the old ReynoldsDecomp series of scripts I made. The purpose of this script is just to extract flowfield variables U,P,Rho,and X from MD or OpenFOAM simulations using pyDataView and same them into numpy arrays. This is done as I have found this process to take a long time, especially with fine mesh OpenFOAM cases/ 

'''
import matplotlib.pyplot as plt
import numpy as np
import sys
import os
from tempfile import TemporaryFile
from numpy.lib.format import open_memmap

ppdir = '/mnt/d/Documents/Brunel/PythonCodes/pyDataView'
sys.path.append(ppdir)
import postproclib as ppl

normal =0
component=0
fileStart=0
fileEnd=206 #time 500 to 55000 in CFD

IsMD = True

#SET WORKING DIRECTORY TO EXTRACT DATA FROM
#FileDir = '/mnt/d/Documents/CFD/CouetteFlowStudies/CouetteFlow2000/' #CFD files directory
FileDir = '/mnt/d/Documents/Brunel/Data/summary_rhouP_data/'


PPObj = ppl.All_PostProc(FileDir) #this class the allpostproc.py script which 


#GET DESIRED FIELD VARIABLES

plotObj = PPObj.plotlist['u']
plotObj2 = PPObj.plotlist['P']# Pressure Data (Note that this is kinemetic pessure)

if IsMD :
	
	plotObj3 = PPObj.plotlist['rho']# Rho Data (use rho for now)

else :

	RhoVal=1. #default value for rho given in OF



#SAVE FIELD VARIABLES INTO ARRAYS. 

RhoVal=1. #default value for rho given in OF

X = plotObj.grid[:] #Array of coordinate values X[X1,X2,X3] aka (X,Y,Z), 
NumXRec = len(X[0])
NumYRec = len(X[1])
NumZRec = len(X[2])
NumTimeRec = fileEnd+1-fileStart




#Iteratively call pydataview to extract data, and then add it to the existing data file using mem mapping

#Create memory-mapped files for Prime and Bar data

UData = open_memmap(FileDir+'postProcessing/TKEBudget/UDataFile.npy',dtype= float,mode='w+', shape =(NumXRec,NumYRec,NumZRec,NumTimeRec,3))
PData = open_memmap(FileDir+'postProcessing/TKEBudget/PDataFile.npy',dtype= float,mode='w+', shape =(NumXRec,NumYRec,NumZRec,NumTimeRec,1))
RhoData = open_memmap(FileDir+'postProcessing/TKEBudget/RhoDataFile.npy',dtype= float,mode='w+', shape =(NumXRec,NumYRec,NumZRec,NumTimeRec,1))

#UData = np.memmap(FileDir+'postProcessing/TKEBudget/UDataFile.npy',dtype= float,mode='w+', shape =(NumXRec,NumYRec,NumZRec,NumTimeRec,3) ) 
#PData = np.memmap(FileDir+'postProcessing/TKEBudget/PDataFile.npy',dtype= float,mode='w+', shape =(NumXRec,NumYRec,NumZRec,NumTimeRec,1) ) 
#RhoData = np.memmap(FileDir+'postProcessing/TKEBudget/RhoDataFile.npy',dtype= float,mode='w+', shape =(NumXRec,NumYRec,NumZRec,NumTimeRec,1) )


for iteration in range(NumTimeRec):

	dataSample = fileStart + iteration

	print("Now extracting data sample {}".format(dataSample))
	
	UData[:,:,:,iteration,:] = plotObj.read(dataSample,dataSample)[:,:,:,0,:] # UData[#X,#Y,#Z,#T,#Velocity components]
	
	PData[:,:,:,iteration,:] = RhoVal*plotObj2.read(dataSample,dataSample)[:,:,:,0,:] # PData[#X,#Y,#Z,#T,Pressure values]

	if IsMD :
	
		RhoData[:,:,:,iteration,:] = plotObj3.read(dataSample,dataSample)[:,:,:,0,:] # RhoData[#X,#Y,#Z,#T,Rho values]

	else :

		RhoData[:,:,:,iteration,:] = RhoVal*np.ones((NumXRec,NumYRec,NumZRec,1))

	

#Flush or Save Data

print("Now saving data..")

UData.flush()
PData.flush()
RhoData.flush()
np.save(FileDir+'postProcessing/TKEBudget/XCoordFile',X)
		




