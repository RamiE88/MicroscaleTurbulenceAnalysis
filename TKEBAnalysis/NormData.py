#The purpose of this code is to compare instantaneous shear stress, mean stear stress, and the normalized values

import matplotlib.pyplot as plt
import numpy as np
import os
import sys
import copy
#from FlowFieldExtract import get_MD_data
import pickle
from numpy.lib.format import open_memmap

#USER CONTROLS

SaveVars = True
isMD = True

fileMD = '/mnt/d/Documents/Brunel/Data/summary_rhouP_data/'
fileCFD = '/mnt/d/Documents/CFD/CouetteFlowStudies/CouetteFlow0022/'

#NumTimeRec = 30# temporary, need to fix header of extracted files so they contain shape information


#Physical Constants
Nu =.625 #MD case from ed .625, cfd = .701
HalfChannel = 280.4


#END USER CONTROLS

#LOAD DATA THAT HAS BEEN PREVIOUSLY EXTRACTED

if isMD:

	FileDir = fileMD #0 to 206
else:

	FileDir = fileCFD 

#Upload Pre Calculated Data 

X = np.load(FileDir+'postProcessing/TKEBudget/XCoordFile.npy',allow_pickle=True)





#NumXRec = len(X[0])# temporary, need to fix header of extracted files so they contain shape information
#NumYRec = len(X[1])# temporary, need to fix header of extracted files so they contain shape information
#NumZRec = len(X[2])# temporary, need to fix header of extracted files so they contain shape information
Xcoord = X[0]
Ycoord= X[1]
Zcoord = X[2]

UBar = np.load(FileDir+'postProcessing/TKEBudget/UBarFile.npy',mmap_mode ='r')
UPrime = np.load(FileDir+'postProcessing/TKEBudget/UPrimeFile.npy',mmap_mode ='r')
PBar = np.load(FileDir+'postProcessing/TKEBudget/PBarFile.npy',mmap_mode ='r')
PPrime = np.load(FileDir+'postProcessing/TKEBudget/PPrimeFile.npy',mmap_mode ='r')

(NumXRec,NumYRec,NumZRec,NumTimeRec,NumFieldRec)=UPrime.shape

#UBar = np.memmap(FileDir+'postProcessing/TKEBudget/UBarFile.npy',dtype= float,mode='r', shape =(NumXRec,NumYRec,NumZRec,3) ) 
#UPrime = np.memmap(FileDir+'postProcessing/TKEBudget/UPrimeFile.npy',dtype= float,mode='r', shape =(NumXRec,NumYRec,NumZRec,NumTimeRec,3) )
#PBar = np.memmap(FileDir+'postProcessing/TKEBudget/PBarFile.npy',dtype= float,mode='r', shape =(NumXRec,NumYRec,NumZRec,1) ) 
#PPrime = np.memmap(FileDir+'postProcessing/TKEBudget/PPrimeFile.npy',dtype= float,mode='r', shape =(NumXRec,NumYRec,NumZRec,NumTimeRec,1) )



UPrimeNorm = open_memmap(FileDir+'postProcessing/TKEBudget/UPrimeNormFile.npy',dtype= float, mode='w+', shape =(NumXRec,NumYRec,NumZRec,NumTimeRec,3))
UBarNorm = open_memmap(FileDir+'postProcessing/TKEBudget/UBarNormFile.npy',dtype= float, mode='w+', shape =(NumXRec,NumYRec,NumZRec,3))

PPrimeNorm = open_memmap(FileDir+'postProcessing/TKEBudget/PPrimeNormFile.npy',dtype= float, mode='w+', shape =(NumXRec,NumYRec,NumZRec,NumTimeRec,1))
PBarNorm = open_memmap(FileDir+'postProcessing/TKEBudget/PBarNormFile.npy',dtype= float, mode='w+', shape =(NumXRec,NumYRec,NumZRec,1))

TKE = open_memmap(FileDir+'postProcessing/TKEBudget/TKEFile.npy',dtype= float, mode='w+', shape =(NumXRec,NumYRec,NumZRec,NumTimeRec,1))
TKEDomain = open_memmap(FileDir+'postProcessing/TKEBudget/TKEDomainFile.npy',dtype= float, mode='w+', shape =(NumTimeRec,1))

#UBarNorm = np.memmap(FileDir+'postProcessing/TKEBudget/UBarNormFile.npy',dtype= float,mode='w+', shape =(NumXRec,NumYRec,NumZRec,3) ) 
#UPrimeNorm = np.memmap(FileDir+'postProcessing/TKEBudget/UPrimeNormFile.npy',dtype= float,mode='w+', shape =(NumXRec,NumYRec,NumZRec,NumTimeRec,3) )
#PBarNorm = np.memmap(FileDir+'postProcessing/TKEBudget/PBarNormFile.npy',dtype= float,mode='w+', shape =(NumXRec,NumYRec,NumZRec,1) ) 
#PPrimeNorm = np.memmap(FileDir+'postProcessing/TKEBudget/PPrimeNormFile.npy',dtype= float,mode='w+', shape =(NumXRec,NumYRec,NumZRec,NumTimeRec,1) )
#TKE = np.memmap(FileDir+'postProcessing/TKEBudget/TKEFile.npy',dtype= float,mode='w+', shape =(NumXRec,NumYRec,NumZRec,NumTimeRec,1) )
#TKEDomain = np.memmap(FileDir+'postProcessing/TKEBudget/TKEDomainFile.npy',dtype= float,mode='w+', shape =(NumTimeRec,1) )

#print(UPrime)



#MD data for fluid is at 2nd cell
if isMD:

	RhoBar = np.memmap(FileDir+'postProcessing/TKEBudget/RhoBarFile.npy',dtype= float,mode='r', shape =(NumXRec,NumYRec,NumZRec,1) ) 
	RhoPrime = np.memmap(FileDir+'postProcessing/TKEBudget/RhoPrimeFile.npy',dtype= float,mode='r', shape =(NumXRec,NumYRec,NumZRec,NumTimeRec,1) )
	TopShift =2
	BotShift =1

else:
	RhoData = np.memmap(FileDir+'postProcessing/TKEBudget/RhoDataFile.npy',dtype= float,mode='r', shape =(NumXRec,NumYRec,NumZRec,NumTimeRec,1) )
	RhoBar = np.memmap(FileDir+'postProcessing/TKEBudget/RhoBarFile.npy',dtype= float,mode='w+', shape =(NumXRec,NumYRec,NumZRec,1) ) 
	TopShift =1
	BotShift =0
	RhoBar[:,:,:,:] = np.mean(RhoData[:,:,:,:,:], axis =(3))

     
#Make a 3D UBar and PBar
#UProfile = np.mean(UBar,axis = (0,2))


#Get Tau Wall, UStar, and Friction Reynolds Number
dUdy1D=np.gradient(UBar[0,:,0,0],Ycoord,axis=0,edge_order=2)



#Load dataset to get Tau value
try:
	data = np.array(pickle.load(open("profiles.p","rb"), encoding='latin1'))
	ave = np.mean(data,0)
	rho = ave[0,:]
	rhouv = rho*0.5*(ave[3,:]+ave[3,::-1]) #rho*np.mean(up*vp,0)
	Tauk = 0.5*(ave[4,:]+ave[4,::-1])-rhouv
	Tauc = 0.5*(ave[5,:]+ave[5,::-1])
	Tau1D = -(Tauk + Tauc)

except  FileNotFoundError:
	#Get Tau from mu*dUdy

	RhoBar1D = np.mean(RhoBar, axis =(0,2))


	mu_raw= Nu*RhoBar1D[:,0]
	[rowsMu_raw] = mu_raw.shape
	Top_mu_raw = mu_raw[rowsMu_raw-TopShift]# for MD dataset density is at second data point
	Bottom_mu_raw = mu_raw[BotShift]
	mu = np.mean([Top_mu_raw,Bottom_mu_raw])
	Tau1D=mu*dUdy1D

#Get top and bottom surface values
[rowsTau]=Tau1D.shape
Top_Tau0=Tau1D[rowsTau-TopShift]
TopRho = RhoBar1D[rowsTau-TopShift]
Bottom_Tau0=Tau1D[BotShift]
BottomRho=RhoBar1D[BotShift]
Tau_Wall= np.mean([Bottom_Tau0,Top_Tau0]) #compute average of top and bottom wall shear
#Tau_Wall = 0.00212

Rho_Wall=np.mean([BottomRho,TopRho])
Ustar = np.sqrt(Tau_Wall/Rho_Wall)
Re=Ustar*HalfChannel/Nu
Yplus = Ycoord*Ustar/Nu

#Normalise Data


for TimeVal in range(NumTimeRec):

	PPrimeNorm[:,:,:,TimeVal,:]= np.divide(PPrime[:,:,:,TimeVal,:],Tau_Wall)
	UPrimeNorm[:,:,:,TimeVal,:]= np.divide(UPrime[:,:,:,TimeVal,:],Ustar)
	TKE[:,:,:,TimeVal,0]= 0.5*(UPrime[:,:,:,TimeVal,0]**2+UPrime[:,:,:,TimeVal,1]**2+UPrime[:,:,:,TimeVal,2]**2)


PBarNorm[:,:,:,:] = PBar[:,:,:,:]/Tau_Wall
UBarNorm[:,:,:,:] = UBar[:,:,:,:]/Ustar
XNorm = X[0]/HalfChannel 
YNorm = X[1]/HalfChannel 
ZNorm = X[2]/HalfChannel 

TKEDomain[:,:] = np.sum(TKE,axis=(0,2,1))


print("Calculation over.")

print(UPrimeNorm)

if SaveVars:

    #Save all data that can be used for TKE analysis
	UPrimeNorm.flush()
	UBarNorm.flush()
	PPrimeNorm.flush()
	PBarNorm.flush()
	TKE.flush()
	TKEDomain.flush()

	np.save(os.path.join(FileDir,'postProcessing/TKEBudget/UstarFile'),Ustar)     
	np.save(os.path.join(FileDir,'postProcessing/TKEBudget/XNormFile'),XNorm)
	np.save(os.path.join(FileDir,'postProcessing/TKEBudget/YNormFile'),YNorm)
	np.save(os.path.join(FileDir,'postProcessing/TKEBudget/ZNormFile'),ZNorm)
	np.save(os.path.join(FileDir,'postProcessing/TKEBudget/TauFile'),Tau1D)
	np.save(os.path.join(FileDir,'postProcessing/TKEBudget/ReynoldsNumberFile'),Re)
	print("Normalised Data Saved.")
 
