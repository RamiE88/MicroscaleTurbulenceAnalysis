'''
Script to do comparison plots between openfoam case and Md results

'''
import matplotlib.pyplot as plt
import numpy as np




OFData = '/mnt/d/Documents/CFD/CoutteFlowStudies/CouetteFlow0005/'# Openfoam, RE 400
MDData = '/mnt/d/Documents/Brunel/Data/summary_rhouP_data/'#MD Flow



OpenFoam_X = np.load(OFData+'XNormFile.npy', allow_pickle =True)
OpenFoam_Ycoord = OpenFoam_X[1]
OpenFoam_P = np.load(OFData+'TKE_PFile.npy')
OpenFoam_T = np.load(OFData+'TKE_TFile.npy')
OpenFoam_D = np.load(OFData+'TKE_DFile.npy')
OpenFoam_Eps = np.load(OFData+'TKE_EpsFile.npy')
OpenFoam_PI = np.load(OFData+'TKE_PIFile.npy')

MD_X = np.load(MDData+'XNormFile.npy', allow_pickle =True)
MD_Ycoord = MD_X[1]
MD_P = np.load(MDData+'TKE_PFile.npy')
MD_T = np.load(MDData+'TKE_TFile.npy')
MD_D = np.load(MDData+'TKE_DFile.npy')
MD_Eps = np.load(MDData+'TKE_EpsFile.npy')
MD_PI = np.load(MDData+'TKE_PIFile.npy')

DKDt_FVM = OpenFoam_P+OpenFoam_T+OpenFoam_D+OpenFoam_PI+OpenFoam_Eps
DKDt_MD = MD_P+MD_T+MD_D+MD_PI+MD_Eps

print(DKDt_FVM)
print(DKDt_MD)



#Budget Comparisons

fig1, ax = plt.subplots()# was 14,2
ax.plot(OpenFoam_Ycoord,OpenFoam_P,'b-',label='P_FVM')
ax.plot(MD_Ycoord,MD_P,'bx',label='P_MD')

ax.plot(OpenFoam_Ycoord,OpenFoam_T,'y-',label='T_FVM')
ax.plot(MD_Ycoord,MD_T,'yx',label='T_MD')

ax.plot(OpenFoam_Ycoord,OpenFoam_PI,'g-',label='PI_FVM')
ax.plot(MD_Ycoord,MD_PI,'gx',label='PI_MD')

ax.plot(OpenFoam_Ycoord,OpenFoam_D,'r-',label='D_FVM')
ax.plot(MD_Ycoord,MD_D,'rx',label='D_MD')

ax.plot(OpenFoam_Ycoord,OpenFoam_Eps,'m-',label='-Eps_FVM')
ax.plot(MD_Ycoord,MD_Eps,'mx',label='-Eps_MD')


#Graph Settings

ax.set_xlabel("Y-Coord")
ax.set_ylabel("Energy")
ax.set_title('1D Channel TKE Budget vs YCoord Continuum FVM vs MD')
ax.legend(loc = 'center',bbox_to_anchor=(1.06,0.5))
ax.grid(which='minor', color='#DDDDDD', linestyle=':', linewidth=0.8)
ax.minorticks_on()
plt.xlim(0,2)
plt.ylim(-15,10)

plt.grid(True)

#Budget Comparisons

fig2, ax = plt.subplots()# was 14,2
ax.plot(OpenFoam_Ycoord,DKDt_FVM,'b-',label='DkDt_FVM')
ax.plot(MD_Ycoord,DKDt_MD,'bx',label='DkDt_MD')

ax.set_xlabel("Y-Coord")
ax.set_ylabel("Dk/Dt")
ax.set_title('1D Channel Dk/Dt vs YCoord Continuum FVM vs MD')
ax.legend(loc = 'center',bbox_to_anchor=(1.06,0.5))
ax.grid(which='minor', color='#DDDDDD', linestyle=':', linewidth=0.8)
ax.minorticks_on()
plt.xlim(0,2)

plt.grid(True)

plt.show()

