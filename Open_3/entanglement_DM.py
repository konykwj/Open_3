import qutip as qt
import numpy as np
import pp


def entropy_lin_DM(rho):
    linen=np.real(1-(rho*rho).tr())
    return linen


def Concur_DM(rho):
    Cijk=np.sqrt(abs(2*(1.0-(rho*rho).tr())))
    return Cijk


def Three_Tgl_DM(rho):
    tgl=0.0
    return tgl



def Entangle_calc_DM(rho):

    rho0=qt.ptrace(rho,0)
    C123=Concur_DM(rho0)
    X0=entropy_lin_DM(rho0)

    rho1=qt.ptrace(rho,1)
    C231=Concur_DM(rho1)
    X1=entropy_lin_DM(rho1)
    
    rho2=qt.ptrace(rho,2)
    C312=Concur_DM(rho2)
    X2=entropy_lin_DM(rho2)

    xcomp=[X0,X1,X2]
    vn=min(xcomp)

    Tgl=Three_Tgl_DM(rho)

    return C123,C231,C312,vn,Tgl



def Ent_calc_DM(Data,job_server): 
    jobs = []
    tsteps=int((Data.infolist)[9])

    avgcr123list=np.zeros(tsteps,dtype=float)
    avgcr231list=np.zeros(tsteps,dtype=float)
    avgcr312list=np.zeros(tsteps,dtype=float)
    avgtglist=np.zeros(tsteps,dtype=float)
    avgvnlist=np.zeros(tsteps,dtype=float)
    
    #Apportions the raw array by each timestep
    for j in range(tsteps):
        rho=Data.rawq[j]
        jobs.append(job_server.submit(Entangle_calc_DM, (rho,), (Concur_DM,entropy_lin_DM,Three_Tgl_DM,), ("numpy as np","qutip as qt",)))
    print "Ent_calc, All Jobs Submitted"

    for j in range(tsteps):
        job=jobs[j]
        C123,C231,C312,vn,Tgl=job()
        avgtglist[j]=Tgl
        avgcr123list[j]=C123
        avgcr231list[j]=C231
        avgcr312list[j]=C312
        avgvnlist[j]=vn

    Data.avgtglist=avgtglist
    Data.avgcr123list=avgcr123list
    Data.avgcr231list=avgcr231list
    Data.avgcr312list=avgcr312list
    Data.avgvnlist=avgvnlist
    
    return

