'''
Calculate and plot the 1D Energy spectrum vs wave number data by

1. extracting the relevant data from the source folder
2. calculate the gradient of energy with respect to wave number
3. plot the energy gradient vs wavenumber
4. save the time array of the gradient vs wavenumber in the source folder


'''

import matplotlib.pyplot as plt
import numpy as np

# User Options

FileDir = '/mnt/d/Documents/CFD/CouetteFlowStudies/CouetteFlow0005/'

Plane = '100pcPlane'

EArrayFile = 'EuuStreamwiseArr.npy'

KArrayFile = 'KxArr.npy'


# Load Data and create mem-mapped arrays

EArr = np.load(f"{FileDir}postProcessing/EnergySpectrum/{Plane}/{EArrayFile}",mmap_mode ='r') 
KArr = np.load(f"{FileDir}postProcessing/EnergySpectrum/{Plane}/{KArrayFile}",mmap_mode ='r')

print(EArr.shape)