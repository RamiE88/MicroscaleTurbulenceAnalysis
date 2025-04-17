#The purpose of this code is to compare instantaneous shear stress, mean stear stress, and the normalized values

import matplotlib.pyplot as plt
import numpy as np
import os
import sys
import copy
#from FlowFieldExtract import get_MD_data
import pickle
from tempfile import mkdtemp
from numpy.lib.format import open_memmap

isMD = True
#NumTimeRec = 10# temporary, need to fix header of extracted files so they contain shape information

#LOAD DATA THAT HAS BEEN PREVIOUSLY EXTRACTED
#Load Udata UBar and UPrime



FileDir = '/mnt/d/Documents/Brunel/Data/summary_rhouP_data/'
#FileDir = '/mnt/d/Documents/CFD/CouetteFlowStudies/CouetteFlow0003/' #Andersson use averaging from 25 to 55
#FileDir = '/mnt/d/Documents/CFD/CouetteFlowStudies/CouetteFlow0004/' #OF - Anderssen, REl 1300
#FileDir = '/mnt/d/Documents/CFD/CouetteFlowStudies/CouetteFlow0006/' #OF - Anderssen, more data
#FileDir = '/mnt/d/Documents/CFD/CouetteFlowStudies/CouetteFlow0007/' #OF - Anderssen, lower courant and higher order interpolation
#FileDir = '/mnt/d/Documents/CFD/CouetteFlowStudies/CouetteFlow0008/' #OF - Anderssen, lower courant and higher order interpolation
#FileDir = '/mnt/d/Documents/CFD/CouetteFlowStudies/CouetteFlow0005/' #OF - MD equivalent
#FileDir = '/mnt/d/Documents/CFD/CouetteFlowStudies/CouetteFlow0009/' #OF - MD equivalent
#FileDir = '/mnt/d/Documents/CFD/CouetteFlowStudies/CouetteFlow0010/' #OF - MD equivalent
#FileDir = '/mnt/d/Documents/CFD/CouetteFlowStudies/CouetteFlow0011/' #OF - MD equivalent
#FileDir = '/mnt/d/Documents/CFD/CouetteFlowStudies/CouetteFlow0022/' #OF - MD equivalent



X = np.load(FileDir+'postProcessing/TKEBudget/XCoordFile.npy',allow_pickle=True)

UData = np.load(FileDir+'postProcessing/TKEBudget/UDataFile.npy',mmap_mode ='r')
PData = np.load(FileDir+'postProcessing/TKEBudget/PDataFile.npy',mmap_mode ='r')

if isMD:
	RhoData = np.load(FileDir+'postProcessing/TKEBudget/RhoDataFile.npy',mmap_mode ='r')

(NumXRec,NumYRec,NumZRec,NumTimeRec,NumFieldRec)=UData.shape
	

#Modify X-coordinates if there are negative coordinates
rowsXCoord=np.zeros(3)
for index in range(3):
    rowsXCoord[index]=X[index].shape[0]
    if X[index][0]<0:
        CoordMax = int(rowsXCoord[index]-1)
        X[index][:]= (X[index][:]+X[index][CoordMax])

Xcoord = X[0]
Ycoord= X[1]
Zcoord = X[2]


#REYNOLDS DECOMPOSITION PORTION OF CODE

#Create memory-mapped files for Prime and Bar data

UPrime = open_memmap(FileDir+'postProcessing/TKEBudget/UPrimeFile.npy',dtype= float, mode='w+', shape =(NumXRec,NumYRec,NumZRec,NumTimeRec,3))
UBar = open_memmap(FileDir+'postProcessing/TKEBudget/UBarFile.npy',dtype= float, mode='w+', shape =(NumXRec,NumYRec,NumZRec,3))

PPrime = open_memmap(FileDir+'postProcessing/TKEBudget/PPrimeFile.npy',dtype= float, mode='w+', shape =(NumXRec,NumYRec,NumZRec,NumTimeRec,1))
PBar = open_memmap(FileDir+'postProcessing/TKEBudget/PBarFile.npy',dtype= float, mode='w+', shape =(NumXRec,NumYRec,NumZRec,1))


if isMD:

	RhoPrime = open_memmap(FileDir+'postProcessing/TKEBudget/RhoPrimeFile.npy',dtype= float,mode='w+', shape =(NumXRec,NumYRec,NumZRec,NumTimeRec,1))
	RhoBar = open_memmap(FileDir+'postProcessing/TKEBudget/RhoBarFile.npy',dtype= float,mode='w+', shape =(NumXRec,NumYRec,NumZRec,1))

#Calculate Profile values


UProfile = np.mean(UData, axis = (0,2,3))
PProfile = np.mean(PData, axis = (0,2,3))


if isMD:
	RhoProfile = np.mean(RhoData, axis =(0,2,3))

print("Calculating Bar Values...")

for YVal in range(NumYRec):
	UBar[:,YVal,:,:] = UProfile[YVal]*np.ones((NumXRec,NumZRec,3))
	PBar[:,YVal,:,:] = PProfile[YVal]*np.ones((NumXRec,NumZRec,1))
	if isMD:
		RhoBar[:,YVal,:,:] = RhoProfile[YVal]*np.ones((NumXRec,NumZRec,1))


print("Calculating Prime Values...")

for TimeVal in range(NumTimeRec):

	print("Calculating for TimeVal {}".format(TimeVal))

	UPrime[:,:,:,TimeVal,:]= np.subtract(UData[:,:,:,TimeVal,:],UBar)
	PPrime[:,:,:,TimeVal,:]= np.subtract(PData[:,:,:,TimeVal,:],PBar)
	if isMD:
		RhoPrime[:,:,:,TimeVal,:]= np.subtract(RhoData[:,:,:,TimeVal,:],RhoBar)

#Save modified data

if isMD:
	avesize = 10
	for TimeVal in range(NumTimeRec):
		if (TimeVal+avesize > NumTimeRec):
			UPrime[:,:,:,TimeVal,:] = np.mean(UPrime[:,:,:,TimeVal-avesize:TimeVal,:],3)
		elif (TimeVal-avesize < 0):
			UPrime[:,:,:,TimeVal,:] = np.mean(UPrime[:,:,:,TimeVal:TimeVal+avesize,:],3)
		else:

			UPrime[:,:,:,TimeVal,:] = np.mean(UPrime[:,:,:,TimeVal-int(avesize/2):TimeVal+int(avesize/2),:],3)
	RhoPrime.flush()
	RhoBar.flush()

print("Saving Files...") 

UPrime.flush()
UBar.flush()

PPrime.flush()
PBar.flush()



