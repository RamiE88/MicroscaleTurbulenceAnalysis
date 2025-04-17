'''
Script to do comparison plots between digitised anderssen DNS data and my OpenFOAM cases

'''
import matplotlib.pyplot as plt
import numpy as np
import csv


DigitisedAndersson="/mnt/d/Documents/Brunel/Data/Anderssen_digitised_data/Budget_pic3.csv" #location of Andersson data
OFData1 = '/mnt/d/Documents/CFD/CouetteFlowStudies/CouetteFlow0008/'# RE,H is 1300 RE,T similar to Andersson
OFData2 = '/mnt/d/Documents/CFD/CouetteFlowStudies/CouetteFlow0007/'# RE,H is 2600 RE,T much higher to Andersson

#Open CSV Data and print to terminal

with open (DigitisedAndersson,'r') as file:
	csvreader = csv.reader(file)
	data = list(csvreader)
		
DataArr = np.array(data[1:len(data)],dtype =float)
NumRows = DataArr.shape

Andersson_X=DataArr[0:NumRows[0]-1,0]
Andersson_P=DataArr[0:NumRows[0]-1,1]
Andersson_T=DataArr[0:NumRows[0]-1,2]
Andersson_D=DataArr[0:NumRows[0]-1,3]
Andersson_PI=DataArr[0:NumRows[0]-1,4]
Andersson_Eps=DataArr[0:NumRows[0]-1,5]

OpenFoam1_X = np.load(OFData1+'XNormFile.npy', allow_pickle =True)
OpenFoam2_X = np.load(OFData2+'XNormFile.npy', allow_pickle =True)
Ycoord1 = OpenFoam1_X[1]
Ycoord2 = OpenFoam2_X[1]

OpenFoam1_P = np.load(OFData1+'TKE_PFile.npy')
OpenFoam1_T = np.load(OFData1+'TKE_TFile.npy')
OpenFoam1_D = np.load(OFData1+'TKE_DFile.npy')
OpenFoam1_Eps = np.load(OFData1+'TKE_EpsFile.npy')
OpenFoam1_PI = np.load(OFData1+'TKE_PIFile.npy')

OpenFoam2_P = np.load(OFData2+'TKE_PFile.npy')
OpenFoam2_T = np.load(OFData2+'TKE_TFile.npy')
OpenFoam2_D = np.load(OFData2+'TKE_DFile.npy')
OpenFoam2_Eps = np.load(OFData2+'TKE_EpsFile.npy')
OpenFoam2_PI = np.load(OFData2+'TKE_PIFile.npy')

DkDt_Andersson = Andersson_P+Andersson_T+Andersson_D+Andersson_PI+Andersson_Eps
DkDt_OpenFoam1 = OpenFoam1_P+OpenFoam1_T+OpenFoam1_D+OpenFoam1_PI+OpenFoam1_Eps
DkDt_OpenFoam2 = OpenFoam2_P+OpenFoam2_T+OpenFoam2_D+OpenFoam2_PI+OpenFoam2_Eps





fig1, ax = plt.subplots()# was 14,2
ax.plot(Andersson_X,Andersson_P,'b-',label='P_A')
ax.plot(Ycoord1,OpenFoam1_P,'bx',label='P_OF_RE1300')
ax.plot(Ycoord2,OpenFoam2_P,'bo',label='P_OF_RE2600')

ax.plot(Andersson_X,Andersson_T,'y-',label='T_A')
ax.plot(Ycoord1,OpenFoam1_T,'yx',label='T_OF_Re1300')
ax.plot(Ycoord2,OpenFoam2_T,'yo',label='T_OF_Re2600')

ax.plot(Andersson_X,Andersson_PI,'g-',label='PI_A')
ax.plot(Ycoord1,OpenFoam1_PI,'gx',label='PI_OF_Re1300')
#ax.plot(Ycoord2,OpenFoam2_PI,'go',label='PI_OF_Re2600')

ax.plot(Andersson_X,Andersson_D,'r-',label='D_A')
ax.plot(Ycoord1,OpenFoam1_D,'rx',label='D_OF_Re1300')
ax.plot(Ycoord2,OpenFoam2_D,'ro',label='D_OF_Re2600')

ax.plot(Andersson_X,Andersson_Eps,'m-',label='-Eps_A')
ax.plot(Ycoord1,OpenFoam1_Eps,'mx',label='-Eps_OF_Re1300')
ax.plot(Ycoord2,OpenFoam2_Eps,'mo',label='-Eps_OF_Re2600')

#Graph Settings

ax.set_xlabel("Y-Coord")
ax.set_ylabel("Energy")
ax.set_title('1D Channel TKE Budget vs YCoord Andersson vs OF')
ax.legend(loc = 'center',bbox_to_anchor=(1.06,0.5))
ax.grid(which='minor', color='#DDDDDD', linestyle=':', linewidth=0.8)
ax.minorticks_on()
plt.xlim(-0.5,2.5)
plt.ylim(-30,30)

plt.grid(True)


#Budget Comparisons

fig2, ax = plt.subplots()# was 14,2
ax.plot(Andersson_X,DkDt_Andersson,'b-',label='DkDt_Spectral')
ax.plot(Ycoord1,DkDt_OpenFoam1,'bx',label='DkDt_FVM_Re1300')
ax.plot(Ycoord2,DkDt_OpenFoam1,'b^',label='DkDt_FVM_Re2600')

ax.set_xlabel("Y-Coord")
ax.set_ylabel("Dk/Dt")
ax.set_title('1D Channel Dk/Dt vs YCoord Continuum Spectral vs FVM')
ax.legend(loc = 'center',bbox_to_anchor=(1.06,0.5))
ax.grid(which='minor', color='#DDDDDD', linestyle=':', linewidth=0.8)
ax.minorticks_on()
plt.xlim(0,2)

plt.grid(True)

plt.show()

