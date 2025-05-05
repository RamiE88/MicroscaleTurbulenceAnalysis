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
Euu_streamwise_Arr = np.load(FileDir+'postProcessing/EnergySpectrum/20pcPlane/EuuStreamwiseArr.npy',mmap_mode ='r') 
KxArr = np.load(FileDir+'postProcessing/EnergySpectrum/20pcPlane/KxArr.npy',mmap_mode ='r')

print(Euu_streamwise_Arr)
# Kolmogorov -5/3 scaling for reference
kx=KxArr[:,0]
C_k = 1.5  # Kolmogorov constant (typical range: 1.5-2.0)
Ekx_kolmogorov = C_k * kx**(-5/3) 


#Shape info
Nx,Ny,Nz,NT = UPrimeNorm[:,:,:,:,0].shape
Yheight = '20pc'

#Mean Euu
Euu_streamwise_mean = np.mean(Euu_streamwise_Arr,axis=1)

for timeVal in TimeArr:

	

	fig1, axes = plt.subplots(1, 2, figsize=(9, 4), sharey=False)

	#Streamwise plot
	axes[0].loglog(kx,Euu_streamwise_mean, 'k-o', linewidth=2, label=r'$Euu(kx) Mean$',zorder=1)
	axes[0].loglog(kx,Euu_streamwise_Arr[:,timeVal], 'r-o', linewidth=2, label=r'$Euu(kx) Snapshot$',zorder=2)
	axes[0].loglog(kx, Ekx_kolmogorov, 'k', label=r"$C_k k^{-5/3}$",zorder=3)
	axes[0].set_title('Snapshot '+str(timeVal)+' ' +str(Nx)+'x'+str(Ny)+'x'+str(Nz)+' Channel')
	axes[0].set_xlabel(r'$kx$')
	axes[0].set_ylabel(r'$Euu(kx)$')
	axes[0].grid(True, which="both", linestyle="--", linewidth=0.5)
	axes[0].legend(loc = 'lower left')
	axes[0].set_xlim(1e-3,1e0)
	axes[0].set_ylim(1e-20,1e5)



	axes[1].plot(TimeArr,DomainTKE,linestyle='solid', color='k',label='Domain TKE',zorder=1)
	axes[1].scatter(TimeArr,DomainTKE,marker='o',facecolors='w',edgecolors='k',zorder=2)
	axes[1].scatter(TimeArr[timeVal],DomainTKE[timeVal],marker='o',facecolors='r',edgecolors='red',zorder=3)
	axes[1].set_xlabel("Time Sample")
	axes[1].set_ylabel("TKE")
	axes[1].set_title('1D Channel Domain TKE vs Time')
	axes[1].legend(loc = 'upper right')#bbox_to_anchor=(1.,0.)
	axes[1].grid(which='minor', color='#DDDDDD', linestyle=':', linewidth=0.8)
	axes[1].minorticks_on()

	plt.tight_layout(rect=[0, 0, 1, 0.95])
	plt.show(block =False)

	fig1.savefig(FileDir+'postProcessing/Videos/EnergySpectrum_20pc/DomainTKEvsTimePlot_'+ str(1000+timeVal)+'.png')

	plt.pause(5)

	plt.close("all")

	
	

