# This code calculates the TKE energy spectrum on a plane of choice


import numpy as np
import matplotlib.pyplot as plt
import os
import sys
from tempfile import mkdtemp
from numpy.lib.format import open_memmap

#Function definition

def compute1DEnergySpectrum(U,Lx,Lz,axis=0):

	Nx,Nz = U.shape

	if axis !=0:

		#Streamwise, with averaging on Span

		dx = Lx/Nx
		Kx=np.fft.fftfreq(Nx, d=dx) * 2 * np.pi
		Kx =np.fft.fftshift(Kx)
		Ukx = np.fft.fftn(U)/Nx
		Ekx = np.fft.fftshift(0.5*(Ukx*np.conj(Ukx)).real)
		Ekx = np.mean(Ekx,axis)
		Ek = Ekx[Nx//2+2:]
		K =  Kx[Nx//2+2:]
		print(Ekx.shape)
		print(Kx.shape)

		
	else:

		#Spanwise, with averaging on Stream
		dz = Lz/Nz
		Kz=np.fft.fftfreq(Nz, d=dz) * 2 * np.pi
		Kz =np.fft.fftshift(Kz)
		Ukz = np.fft.fftn(U)/Nz
		Ekz = np.fft.fftshift(0.5*(Ukz*np.conj(Ukz)).real)
		Ekz = np.mean(Ekz,axis)
		Ek = Ekz[Nz//2+1:]
		K =  Kz[Nz//2+1:]

	return Ek,K,

def makeSpectrumPlots(Kx,Kz,E_streamwise,E_spanwise,EComponentName,PlotTitle,SavePlots,FileName='DidNotSave'):

	fig1, axes = plt.subplots(1, 2, figsize=(9, 4), sharey=True)

	#Streamwise plot
	axes[0].loglog(Kx, E_streamwise, 'r-o', linewidth=2, label=r'$'+EComponentName+'(kx)$')
	axes[0].loglog(Kx, Ekx_kolmogorov, 'k', label=r"$C_k k^{-5/3}$")
	axes[0].set_xlabel(r'$kx$')
	axes[0].set_ylabel(r'$'+EComponentName+'(kx)$')
	axes[0].grid(True, which="both", linestyle="--", linewidth=0.5)
	axes[0].legend(loc = 'lower left')
	axes[0].set_xlim(1e-3,1e0)
	axes[0].set_ylim(1e-20,1e5)


	#Spanwise plot
	axes[1].loglog(Kz, Euu_spanwise, 'r-o', linewidth=2, label=r'$'+EComponentName+'(kz)$')
	axes[1].loglog(Kz, Ekz_kolmogorov, 'k', label=r"$C_k k^{-5/3}$")
	axes[1].set_xlabel(r'$kz$')
	axes[1].set_ylabel(r'$'+EComponentName+'(kz)$')
	axes[1].grid(True, which="both", linestyle="--", linewidth=0.5)
	axes[1].legend(loc = 'lower left')
	axes[1].set_xlim(1e-3,1e0)

	fig1.suptitle(PlotTitle)
	plt.tight_layout(rect=[0, 0, 1, 0.95])
	plt.show(block =False)

	if SavePlots:

        	fig1.savefig(FolderforResults+FileName)

	plt.pause(2)

	plt.close("all")




#User Options

Lx = 1541.0 
Ly = 560.0
Lz = 1057.0

ViewPlots = True
SavePlots = True
SaveVars = True

YPlaneDivisor = 5
Yresultsfolder ='20pcPlane'





#LOAD DATA THAT HAS BEEN PREVIOUSLY EXTRACTED

#Cases = ['0005','0010','0011','0012','0013','0014','0015','0016','0018',
#'0019','0020','0021','0022','0023','0024','0025','0026','0028']

#Cases = ['0005','0005','0010','0011','0012']
Cases =['0005']

for iteration in range(len(Cases)):

	

	FileDir = '/mnt/d/Documents/CFD/CouetteFlowStudies/CouetteFlow' + Cases[iteration] + '/'# CFD - MD equivalent
	#FileDir = '/mnt/d/Documents/Brunel/Data/summary_rhouP_data/'#MD Flow
	
	FolderforResults = FileDir+'postProcessing/EnergySpectrum/'+Yresultsfolder+'/'

	#Ycoord = np.load(FileDir+'postProcessing/TKEBudget/YCoordFile.npy', allow_pickle =True)
	UPrimeNorm = np.load(FileDir+'postProcessing/TKEBudget/UPrimeNormFile.npy',mmap_mode ='r')
	UPrimeNorm = UPrimeNorm[:,:,:,:]


	#MAIN CODE


	# Check if folder exists, if not,create it



	print('Now working on CouetteFlow' + Cases[iteration])
	if not os.path.exists(FolderforResults):
		os.makedirs(FolderforResults)



	Nx,Ny,Nz,NT = UPrimeNorm[:,:,:,:,0].shape

	
	dx = Lx/Nx
	dy = Ly/Ny
	dz = Lz/Nz

	Yheight=(Ly/YPlaneDivisor)/Ly
	print(UPrimeNorm[:,:,:,:,0].shape)

	print(Nx//2-1)
	print(Nx//2)

	

	Euu_streamwise_Arr =open_memmap(FolderforResults+'EuuStreamwiseArr.npy',dtype= float, mode='w+', shape =(Nx//2-2,NT))
	Euu_spanwise_Arr =open_memmap(FolderforResults+'EuuSpanwiseArr.npy',dtype= float, mode='w+', shape =(Nz//2-1,NT))
	Eww_streamwise_Arr =open_memmap(FolderforResults+'EwwStreamwiseArr.npy',dtype= float, mode='w+', shape =(Nx//2-2,NT))
	Eww_spanwise_Arr =open_memmap(FolderforResults+'EwwSpanwiseArr.npy',dtype= float, mode='w+', shape =(Nz//2-1,NT))


	KxArr =open_memmap(FolderforResults+'KxArr.npy',dtype= float, mode='w+', shape =(Nx//2-2,NT))
	KzArr =open_memmap(FolderforResults+'KzArr.npy',dtype= float, mode='w+', shape =(Nz//2-1,NT))


	for timeiter in range(NT):

		velocity_field = np.mean([UPrimeNorm[:,Ny//YPlaneDivisor,:,timeiter,:],UPrimeNorm[:,Ny//YPlaneDivisor+1,:,timeiter,:]], axis=0 ) 

		#velocity_field = UPrimeNorm[:,Ny//YPlaneDivisor-1,:,timeiter,:]

		Ux = velocity_field[:,:,0] #streamwise
		Uy = velocity_field[:,:,1]
		Uz = velocity_field[:,:,2]#spanwise
	
		Euu_streamwise_Arr[:,timeiter],KxArr[:,timeiter] = compute1DEnergySpectrum(Ux,Lx,Lz,axis=1)
		Euu_spanwise_Arr[:,timeiter],KzArr[:,timeiter] = compute1DEnergySpectrum(Ux,Lx,Lz,axis=0)

		Eww_streamwise_Arr[:,timeiter],KxArr[:,timeiter] = compute1DEnergySpectrum(Uz,Lx,Lz,axis=1)
		Eww_spanwise_Arr[:,timeiter],KzArr[:,timeiter] = compute1DEnergySpectrum(Uz,Lx,Lz,axis=0)


	Euu_streamwise = np.mean(Euu_streamwise_Arr,axis=1)
	Euu_spanwise = np.mean(Euu_spanwise_Arr,axis=1)

	Eww_streamwise = np.mean(Eww_streamwise_Arr,axis=1)
	Eww_spanwise = np.mean(Eww_spanwise_Arr,axis=1)

	Kx = KxArr[:,0]
	Kz = KzArr[:,0]


	# Kolmogorov -5/3 scaling for reference
	C_k = 1.5  # Kolmogorov constant (typical range: 1.5-2.0)
	Ekx_kolmogorov = C_k * Kx**(-5/3)
	Ekz_kolmogorov = C_k * Kz**(-5/3)

	#Snapshot Plots

	for iteration in range(NT):

		TEuuTitle='Snapshot '+str(iteration)+' 1D Energy Spectrum in ' +str(Nx)+'x'+str(Ny)+'x'+str(Nz)+' Channel at '+ str(Yheight)+ ' Channel Height'
		TEuuFilename = 'T_'+str(iteration)+'_EuuPlots.png'
		makeSpectrumPlots(Kx,Kz,Euu_streamwise_Arr[:,iteration],Euu_spanwise_Arr[:,iteration],'Euu',TEuuTitle,SavePlots,TEuuFilename)

		TEwwTitle='Snapshot '+str(iteration)+' 1D Energy Spectrum in ' +str(Nx)+'x'+str(Ny)+'x'+str(Nz)+' Channel at '+ str(Yheight)+ ' Channel Height'
		TEwwFilename = 'T_'+str(iteration)+'_EwwPlots.png'
		makeSpectrumPlots(Kx,Kz,Eww_streamwise_Arr[:,iteration],Eww_spanwise_Arr[:,iteration],'Eww',TEwwTitle,SavePlots,TEwwFilename)

	

	#Time Averaged Plots
	# Euu Plots
	TAEuuTitle="Time Ave 1D Energy Spectrum in " +str(Nx)+'x'+str(Ny)+'x'+str(Nz)+' Channel at '+ str(Yheight)+ ' Channel Height'
	makeSpectrumPlots(Kx,Kz,Euu_streamwise,Euu_spanwise,'Euu',TAEuuTitle,SavePlots,'TA_EuuPlots.png')

	# Eww Plots
	TAEwwTitle="Time Ave 1D Energy Spectrum in " +str(Nx)+'x'+str(Ny)+'x'+str(Nz)+' Channel at '+ str(Yheight)+ ' Channel Height'
	makeSpectrumPlots(Kx,Kz,Eww_streamwise,Eww_spanwise,'Eww',TAEwwTitle,SavePlots,'TA_EwwPlots.png')


	if SaveVars:

		#Save all data that can be used for TKE analysis

		Euu_streamwise_Arr.flush()
	
		Euu_spanwise_Arr.flush()

		Eww_streamwise_Arr.flush()
		
		Eww_spanwise_Arr.flush()

		KxArr.flush()

		KzArr.flush()


		print("Data Saved.")
















