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
    EGradientArr[:,timeVal] = np.gradient(EArr[:,timeVal],KArr[:,timeVal],axis=0,edge_order=1)

print(EArr[:,0]/1e-12)


fig1, axes = plt.subplots(1, 2, figsize=(12, 5))

#Gradient vs Wavenumber plot
axes[0].plot(KArr[:,0], EGradientArr[:,0], 'r-o', linewidth=2)
axes[0].set_xscale('log')
#axes[0].set_ylim(-1e-13,-1e-14)
axes[0].set_xlim(1e-3,1e0)
axes[0].set_xlabel('Wavenumber')
axes[0].set_ylabel('Gradient of Energy')

#Energy vs Wavenumber plot

axes[1].loglog(KArr[:,0], EArr[:,0], 'r-o', linewidth=2)
axes[1].set_xlim(1e-3,1e0)
axes[1].set_ylim(1e-20,1e5)
axes[1].set_xlabel('Wavenumber')
axes[1].set_ylabel('Energy')

plt.show()