'''
Script to calculated TKE Budget for 1D Channel using formulation given in Anderrson paper. 
U values normalised by Ustar
Xcoord values normalised by HalfChannel
P vales normalised by Tau Wall

'''
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
from tempfile import mkdtemp
from numpy.lib.format import open_memmap


#USER INPUTS

#LOAD DATA THAT HAS BEEN PREVIOUSLY EXTRACTED
#FileDir = '/mnt/d/Documents/CFD/CouetteFlowStudies/CouetteFlow0022/'# CFD - MD equivalent
FileDir = '/mnt/d/Documents/Brunel/Data/summary_rhouP_data/'#MD Flow

HalfChannel =280.4
SaveVars =True


#END OF USER INPUTS


#Upload Pre Calculated Data
Xcoord = np.load(FileDir+'postProcessing/TKEBudget/XNormFile.npy', allow_pickle =True)
Ycoord = np.load(FileDir+'postProcessing/TKEBudget/YNormFile.npy', allow_pickle =True)
Zcoord = np.load(FileDir+'postProcessing/TKEBudget/ZNormFile.npy', allow_pickle =True)

XNorm =[Xcoord,Ycoord,Zcoord]

UStar = np.load(FileDir+'postProcessing/TKEBudget/UstarFile.npy')
Re = np.load(FileDir+'postProcessing/TKEBudget/ReynoldsNumberFile.npy')


UBarNorm = np.load(FileDir+'postProcessing/TKEBudget/UBarNormFile.npy',mmap_mode ='r')
UPrimeNorm = np.load(FileDir+'postProcessing/TKEBudget/UPrimeNormFile.npy',mmap_mode ='r')
PPrimeNorm = np.load(FileDir+'postProcessing/TKEBudget/PPrimeNormFile.npy',mmap_mode ='r')

(NumXRec,NumYRec,NumZRec,NumTimeRec,NumFieldRec)=UPrimeNorm.shape


print(PPrimeNorm)




#Make mem-mapped arrays for data we want to keep

P = open_memmap(FileDir+'postProcessing/TKEBudget/TKE_PFile.npy',dtype= float, mode='w+', shape =(NumYRec,1))
T = open_memmap(FileDir+'postProcessing/TKEBudget/TKE_TFile.npy',dtype= float, mode='w+', shape =(NumYRec,1))
pi = open_memmap(FileDir+'postProcessing/TKEBudget/TKE_PIFile.npy',dtype= float, mode='w+', shape =(NumYRec,1))
D = open_memmap(FileDir+'postProcessing/TKEBudget/TKE_DFile.npy',dtype= float, mode='w+', shape =(NumYRec,1))
eps = open_memmap(FileDir+'postProcessing/TKEBudget/TKE_EpsFile.npy',dtype= float, mode='w+', shape =(NumYRec,1))

TKE_Balance = open_memmap(FileDir+'postProcessing/TKEBudget/TKE_TermsBalanceFile.npy',dtype= float, mode='w+', shape =(NumYRec,1))

q2v_Bar = open_memmap(FileDir+'postProcessing/TKEBudget/TKE_q2V_BarFile.npy',dtype= float, mode='w+', shape =(NumYRec,1))
u2v_Bar = open_memmap(FileDir+'postProcessing/TKEBudget/TKE_u2v_BarFile.npy',dtype= float, mode='w+', shape =(NumYRec,1))


#Temporary mem-mapped files for usage during calculation but not saved

UBarNorm1DTempfile = os.path.join(mkdtemp(), 'UBarNorm1Dfile.npy')
UBarNorm1D = np.memmap(UBarNorm1DTempfile,dtype= float,mode='w+', shape =(NumYRec,3) ) 

k1DTempfile = os.path.join(mkdtemp(), 'k1Dfile.npy')
k_1D = np.memmap(k1DTempfile,dtype= float,mode='w+', shape =(NumYRec,1) ) 

dUdyTempfile = os.path.join(mkdtemp(), 'dUdyfile.npy')
dUdy = np.memmap(dUdyTempfile,dtype= float,mode='w+', shape =(NumYRec,1) ) 

q2Tempfile = os.path.join(mkdtemp(), 'q2file.npy')
q2 = np.memmap(q2Tempfile,dtype= float,mode='w+', shape =(NumXRec,NumYRec,NumZRec,NumTimeRec,1) ) 

u1Tempfile = os.path.join(mkdtemp(), 'u1file.npy')
u1 = np.memmap(u1Tempfile,dtype= float,mode='w+', shape =(NumXRec,NumYRec,NumZRec,NumTimeRec,1) ) 

u2Tempfile = os.path.join(mkdtemp(), 'u2file.npy')
u2 = np.memmap(u2Tempfile,dtype= float,mode='w+', shape =(NumXRec,NumYRec,NumZRec,NumTimeRec,1) ) 

u3Tempfile = os.path.join(mkdtemp(), 'u3file.npy')
u3 = np.memmap(u3Tempfile,dtype= float,mode='w+', shape =(NumXRec,NumYRec,NumZRec,NumTimeRec,1) ) 

u1u2Tempfile = os.path.join(mkdtemp(), 'u1u2file.npy')
u1u2 = np.memmap(u1u2Tempfile,dtype= float,mode='w+', shape =(NumXRec,NumYRec,NumZRec,NumTimeRec,1) ) 

u1u2BarTempfile = os.path.join(mkdtemp(), 'u1u2Barfile.npy')
u1u2Bar = np.memmap(u1u2BarTempfile,dtype= float,mode='w+', shape =(NumYRec,1) ) 

pv_barTempfile = os.path.join(mkdtemp(), 'pv_barfile.npy')
pv_bar = np.memmap(pv_barTempfile,dtype= float,mode='w+', shape =(NumYRec,1) )

dkdy_Tempfile = os.path.join(mkdtemp(), 'dkdyfile.npy')
dkdy = np.memmap(dkdy_Tempfile,dtype= float,mode='w+', shape =(NumYRec,1) )

d2kdy2_Tempfile = os.path.join(mkdtemp(), 'd2kdy2file.npy')
d2kdy2 = np.memmap(d2kdy2_Tempfile,dtype= float,mode='w+', shape =(NumYRec,1) )

duidxj1_Tempfile = os.path.join(mkdtemp(), 'duidxj1file.npy')
duidxj_1 = np.memmap(duidxj1_Tempfile,dtype= float,mode='w+', shape =(NumXRec,NumYRec,NumZRec,NumTimeRec,1) )

duidxj2_Tempfile = os.path.join(mkdtemp(), 'duidxj2file.npy')
duidxj_2 = np.memmap(duidxj2_Tempfile,dtype= float,mode='w+', shape =(NumXRec,NumYRec,NumZRec,NumTimeRec,1) )

duidxj_Tempfile = os.path.join(mkdtemp(), 'duidxjfile.npy')
duidxj = np.memmap(duidxj_Tempfile,dtype= float,mode='w+', shape =(NumYRec,1) )


print("Calculating....")

print("Reynolds number is:")
print(Re)

print("Ustar is:")
print(UStar)

print("HalfChannel is:")
print(HalfChannel)



#Calculate 1D dU/Dy

UBarNorm1D[:,:] = np.mean(UBarNorm, axis =(0,2))
dUdy[:,0] = np.gradient(UBarNorm1D[:,0],Ycoord,axis=0,edge_order=2)


#Calculate u1u2, q, and k

u1[:,:,:,:,0] = UPrimeNorm[:,:,:,:,0]
u2[:,:,:,:,0] = UPrimeNorm[:,:,:,:,1]
u3[:,:,:,:,0] = UPrimeNorm[:,:,:,:,2]

u1u2[:,:,:,:,:] = u1*u2
q2[:,:,:,:,:] = (u1**2 + u2**2 + u3**2)


k_1D[:,:]= 0.5*np.mean(q2,axis = (3,0,2)) #mean TKE

#Calculate P, shear production
u1u2Bar[:,:] = np.mean(u1u2, axis = (3,0,2))
P[:,:] = -u1u2Bar*dUdy 

#Calculate T, turbulent diffusion associated with velocity
u2v_Bar[:,:] = np.mean(u1**2*u2, axis = (3,0,2))
q2v_Bar[:,:] = np.mean(q2*u2, axis = (3,0,2))
T[:,:] = -0.5*np.gradient(q2v_Bar,Ycoord,axis=0,edge_order=2)

#Calculated pi, pressure fluctuations



pv_bar[:,:] = np.mean(PPrimeNorm*u2, axis = (3,0,2))
pi[:,:] = -np.gradient(pv_bar,Ycoord,axis=0,edge_order=2)

#Calculate D, Viscous Diffusion

dkdy[:,:] = np.gradient(k_1D,Ycoord,axis=0,edge_order=2)
d2kdy2[:,:] =np.gradient(dkdy,Ycoord,axis=0,edge_order=2)
D[:,:] = (1/Re)*d2kdy2

#Calculate eps, viscous energy dissipation

duidxj[:,0]=np.zeros(np.shape(Ycoord))

for i in range(3):
	for j in range(3):
		duidxj_1[:,:,:,:,0]=np.gradient(UPrimeNorm[:,:,:,:,i],XNorm[j],axis=j,edge_order=2)
		duidxj_2[:,:,:,:,:]=duidxj_1**2
		duidxj[:,:]=duidxj+np.mean(duidxj_2,axis=(3,0,2))


eps[:,:]=(-1/Re)*duidxj


TKE_Balance[:,:] = P+T+pi+D+eps



#plot 1D TKE Budget
fig1, ax = plt.subplots()# was 14,2
ax.plot(Ycoord,P,'-',label='P')
ax.plot(Ycoord,T,'--',label='T')
ax.plot(Ycoord,pi,'^-',label='PI')
ax.plot(Ycoord,D,'*-',label='D')
ax.plot(Ycoord,eps,'--',label='-Eps')
ax.set_xlabel("Y-Coord")
ax.set_ylabel("Energy")
ax.set_title(r'1D Channel TKE Budget vs YCoord at $Re_\tau$ of '+str(int(Re)))
ax.legend()
ax.set_ylim(bottom=-10)
ax.set_ylim(top=10)




#plot 1D Third order moments (Andersson fig 4)
fig2, ax = plt.subplots()
ax.plot(Ycoord,q2v_Bar,'-',label='q2v')
ax.plot(Ycoord,u2v_Bar,'--',label='u2v')
ax.set_xlabel("Y-Coord")
ax.set_ylabel("Third Order Moments")
ax.set_title(r'Third Order Moment Distribution across Channel at $Re_\tau$ of '+str(int(Re)))
ax.set_ylim(bottom=-1.5)
ax.set_ylim(top=1.5)
ax.legend()



#plot 1D Turbulence generation vs dissipation
fig3, ax = plt.subplots()


ax.plot(Ycoord,TKE_Balance,'-',label='Sum of all TKE Terms')
ax.set_xlabel("Y-Coord")
ax.set_ylabel("Energy")
ax.set_title(r'Sum of TKE Budget Terms across Channel at $Re_\tau$ of '+str(int(Re)))

ax.legend()

plt.show(block =False)

fig1.savefig(FileDir+'postProcessing/TKEBudget/TKEBudgetPlot.png')


fig2.savefig(FileDir+'postProcessing/TKEBudget/ThirdOrderMomentsPlot.png')

fig3.savefig(FileDir+'postProcessing/TKEBudget/TKESumTermsPlot.png')

plt.pause(10)

plt.close("all")




if SaveVars:

	#Save all data that can be used for TKE analysis

	P.flush()
	
	T.flush()

	pi.flush()
        
	D.flush()

	eps.flush()

	TKE_Balance.flush()

	q2v_Bar.flush()

	u2v_Bar.flush()


	print("Data Saved.")




