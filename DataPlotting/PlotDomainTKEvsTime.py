'''
Script to do comparison plots between openfoam case and Md results

'''
import matplotlib.pyplot as plt
import numpy as np



FileDir = '/mnt/d/Documents/CFD/CouetteFlowStudies/CouetteFlow0029/' # Openfoam, RE 400
#FileDir = '/mnt/d/Documents/Brunel/Data/summary_rhouP_data/'#MD Flow


NumTimeRecs =50
TimeStart =0



TimeArr = range(TimeStart,(TimeStart+NumTimeRecs))


#Load Data
UPrimeNorm = np.load(FileDir+'postProcessing/TKEBudget/UPrimeNormFile.npy',mmap_mode ='r')
DomainTKE = np.load(FileDir+'postProcessing/TKEBudget/TKEDomainFile.npy',mmap_mode ='r') 




#Shape info
Nx,Ny,Nz,NT = UPrimeNorm[:,:,:,:,0].shape



fig1, axes = plt.subplots(1, 1, figsize=(9, 4))



axes.plot(TimeArr,DomainTKE,'k-o',linestyle='solid',label='Domain TKE',zorder=1)
axes.set_xlabel("Time Sample")
axes.set_ylabel("TKE")
axes.set_title('1D Channel Domain TKE vs Time')
axes.legend(loc = 'upper right')#bbox_to_anchor=(1.,0.)
axes.grid(which='minor', color='#DDDDDD', linestyle=':', linewidth=0.8)
axes.minorticks_on()

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.show(block =False)

fig1.savefig(FileDir+'postProcessing/TKEBudget/DomainTKEvsTimePlot.png')

plt.pause(5)

plt.close("all")

	
	

