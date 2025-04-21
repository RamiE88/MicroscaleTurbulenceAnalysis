'''
Calculate and plot the 1D Energy spectrum vs wave number data by

1. extracting the relevant data from the source folder
2. calculate the gradient of energy with respect to wave number
3. plot the energy gradient vs wavenumber
4. save the time array of the gradient vs wavenumber in the source folder


'''

import matplotlib.pyplot as plt
import numpy as np
from numpy.lib.format import open_memmap

# User Options

FileDir = '/mnt/d/Documents/CFD/CouetteFlowStudies/CouetteFlow0005/'

Plane = '50pcPlane'

EArrayFile = 'EuuStreamwiseArr.npy'

KArrayFile = 'KxArr.npy'


# Load Data and create memory-mapped arrays

FolderforResults = f"{FileDir}postProcessing/EnergySpectrum/{Plane}"

EArr = np.load(f"{FolderforResults}/{EArrayFile}",mmap_mode ='r') 
KArr = np.load(f"{FolderforResults}/{KArrayFile}",mmap_mode ='r') 

# Make new array for gradient data
NumEdata,NumTdata = EArr.shape
NumKData = KArr.shape[0]

EGradientArr =open_memmap(f"{FolderforResults}/{EArrayFile[0:13]}GradArr.npy",dtype= float, mode='w+', shape =(NumEdata,NumTdata))

for timeVal in range(NumTdata):
    # Calculate the gradient of energy with respect to wave number
    EGradientArr[:,timeVal] = np.gradient(EArr[:,timeVal],KArr[:,0],axis=0,edge_order=2)


