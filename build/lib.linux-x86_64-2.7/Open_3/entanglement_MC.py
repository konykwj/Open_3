#Defines custom partial traces
#Various Routines for calculating the entanglement of a system
import qutip as qt
import numpy as np
import pp

oq=qt.basis(2,0)
lq=qt.basis(2,1)

o=np.zeros([2,1],dtype=complex)
l=np.zeros([2,1],dtype=complex)
u=oq.shape

for i in range(u[0]):       #The loop that creates the numpy arrays for the pauli operators
    for j in range(u[1]):
        o[i,j]=oq[i,j]
        l[i,j]=lq[i,j]
        
        
def rhoC_trace(psi):
    
    a=(psi[0,0]*o+psi[1,0]*l)*((psi[0,0]*o+psi[1,0]*l).conjugate()).transpose() ###Check that dot prod isn't what's required (though this routine has been checked previously)
    b=(psi[4,0]*o+psi[5,0]*l)*((psi[4,0]*o+psi[5,0]*l).conjugate()).transpose()
    c=(psi[2,0]*o+psi[3,0]*l)*((psi[2,0]*o+psi[3,0]*l).conjugate()).transpose()
    d=(psi[6,0]*o+psi[7,0]*l)*((psi[6,0]*o+psi[7,0]*l).conjugate()).transpose()
    
    rhop=a+b+c+d
    return rhop

def rhoB_trace(psi):

    a=(psi[0,0]*o+psi[2,0]*l)*((psi[0,0]*o+psi[2,0]*l).conjugate()).transpose()
    b=(psi[1,0]*o+psi[3,0]*l)*((psi[1,0]*o+psi[3,0]*l).conjugate()).transpose()
    c=(psi[4,0]*o+psi[6,0]*l)*((psi[4,0]*o+psi[6,0]*l).conjugate()).transpose()
    d=(psi[5,0]*o+psi[7,0]*l)*((psi[5,0]*o+psi[7,0]*l).conjugate()).transpose()
    
    rhop=a+b+c+d
    return rhop

def rhoA_trace(psi):

    a=(psi[0,0]*o+psi[4,0]*l)*((psi[0,0]*o+psi[4,0]*l).conjugate()).transpose()
    b=(psi[2,0]*o+psi[6,0]*l)*((psi[2,0]*o+psi[6,0]*l).conjugate()).transpose()
    c=(psi[1,0]*o+psi[5,0]*l)*((psi[1,0]*o+psi[5,0]*l).conjugate()).transpose()
    d=(psi[3,0]*o+psi[7,0]*l)*((psi[3,0]*o+psi[7,0]*l).conjugate()).transpose()
    
    rhop=a+b+c+d
    return rhop


#General entanglement computations:

def Three_Tgl(psi):
    d1=(psi[0]**2)*(psi[7]**2)+(psi[1]**2)*(psi[6]**2)+(psi[2]**2)*(psi[5]**2)+(psi[4]**2)*(psi[3]**2)
    d2=psi[0]*psi[7]*psi[3]*psi[4]+psi[0]*psi[7]*psi[5]*psi[2]+psi[0]*psi[7]*psi[6]*psi[1]+psi[3]*psi[4]*psi[5]*psi[2]+psi[3]*psi[4]*psi[6]*psi[1]+psi[5]*psi[2]*psi[6]*psi[1]
    d3=psi[0]*psi[6]*psi[5]*psi[3]+psi[7]*psi[1]*psi[2]*psi[4]
    tgl=4*abs(d1-2*d2+4*d3)
    return tgl


def entropy_lin(rho):
    linen=np.real(1-(np.dot(rho,rho)).trace())
    return linen


def Concur(rho):
    Cijk=np.sqrt(2*(1.0-(rho*rho).trace()))
    return Cijk


def Entangle_calc(qth_tstep,ntraj):  #Averages each timestep

    Tgl=0
    C123=0
    C231=0
    C312=0
    vn=0
    
    for i in range(ntraj):
        psi=qth_tstep[0,i]
        
        rho0=rhoA_trace(psi)
        C123=Concur(rho0)+C123
        X0=entropy_lin(rho0)

        rho1=rhoB_trace(psi)
        C231=Concur(rho1)+C231
        X1=entropy_lin(rho1)
        
        rho2=rhoC_trace(psi)
        C312=Concur(rho2)+C312
        X2=entropy_lin(rho2)

        xcomp=[X0,X1,X2]
        vn=min(xcomp)+vn

        Tgl=Three_Tgl(psi)+Tgl

    Tgl=np.real(Tgl/float(ntraj))
    C123=np.real(C123/float(ntraj))
    C231=np.real(C231/float(ntraj))
    C312=np.real(C312/float(ntraj))
    vn=np.real(vn/float(ntraj))

    return C123,C231,C312,vn,Tgl



def Ent_calc(Data,job_server): 
    jobs = []
    tsteps=int((Data.infolist)[9])
    ntraj=int((Data.infolist)[10])


    avgcr123list=np.zeros(tsteps,dtype=float)
    avgcr231list=np.zeros(tsteps,dtype=float)
    avgcr312list=np.zeros(tsteps,dtype=float)
    avgtglist=np.zeros(tsteps,dtype=float)
    avgvnlist=np.zeros(tsteps,dtype=float)
    
    #Apportions the raw array by each timestep
    for j in range(tsteps):
        qth_tstep=np.zeros([1,ntraj],dtype=np.ndarray)
        for i in range(ntraj):
            qth_tstep[0,i]=(Data.raw)[i,j]
        jobs.append(job_server.submit(Entangle_calc, (qth_tstep,ntraj,), (Concur,entropy_lin,Three_Tgl,rhoC_trace,rhoB_trace,rhoA_trace,), ("numpy as np","from Open_3 import o,l")))  ###May not work properly yet
    print "Ent_calc, All Jobs Submitted"


    for j in range(tsteps):
        job=jobs[j]
        print "Ent Timestep ",j," complete"
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

