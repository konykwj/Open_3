#Finding Nonlocality with monte carlo quantum trajectory method.
import numpy as np
from general_functions import *
import S_maximize_3q as S3
import M_maximize_3q as M3



def S_check_Single(ith_traj,guess,tsteps,opts):

    smlist=np.zeros(tsteps,dtype=np.ndarray) #List for all maximum positive violatons for each vector
    maxlistlist=np.zeros(tsteps,dtype=np.ndarray)
    t=0
    for j in range(tsteps): #For every timestep...        
        psi=ith_traj[0,j]
        
        xoptalist=S3.S_maximize(guess,psi)
        speciallist=S3.unique_search(xoptalist)
        maxlist=S3.max_cull(speciallist,psi)
        Sm=S3.Fa(maxlist[0],psi)
        if opts[0]==1:
            maxlistlist[j]=maxlist
        smlist[j]=Sm

    return smlist,maxlistlist

def S_calc(raw,guess,ntraj,tsteps,name,opts,job_server):
    #Raw is already a ntraj by tstep matrix.
    jobs = []
    maximized=np.zeros([ntraj,tsteps],dtype=complex)
    maxlistlist=np.zeros([ntraj,tsteps],dtype=np.ndarray)
    
    #Apportions the raw array by each trajectory
    for i in range(ntraj):
        ith_traj=np.zeros([1,tsteps],dtype=np.ndarray)
        for j in range(tsteps):
            ith_traj[0,j]=raw[i,j]
        jobs.append(job_server.submit(S_check_Single, (ith_traj,guess,tsteps,opts), (), ("numpy as np","S_maximize_3q as S3",)))
    print "All Jobs Submitted"
    #Records the results from the individual jobs in an array

    for i in range(ntraj):
        job=jobs[i]
        print i,"th trajectory complete"
        qth_smlist,qth_maxlist=job()
        for j in range(tsteps):
            maximized[i,j]=qth_smlist[j]
            maxlistlist[i,j]=qth_maxlist
         
            
    #Averages the array
    avgSlist=np.zeros(tsteps,dtype=complex)
    for j in range(tsteps):
        Smax=0
        for i in range(ntraj):
            Smax=Smax+maximized[i,j]
        Smax=abs(Smax/float(ntraj))
        avgSlist[j]=Smax
    avgSlist=np.real(avgSlist)
    return avgSlist,maxlistlist

#Mermin Calculating:

def M_check_Single(ith_traj,guess,tsteps):

    Mlist=np.zeros(tsteps,dtype=np.ndarray) #List for all maximum positive violatons for each vector
    t=0
    for j in range(tsteps): #For every timestep...        
        psi=ith_traj[0,j]
        
        xoptalist=M3.M_maximize(guess,psi)
        speciallist=M3.unique_search(xoptalist)
        maxlist=M3.max_cull(speciallist,psi)
        Mm=M3.Fa(maxlist[0],psi)
        Mlist[j]=Mm

    return Mlist

def M_calc(raw,guess,ntraj,tsteps,name,job_server):
    #Raw is already a ntraj by tstep matrix.
    jobs = []
    maximized=np.zeros([ntraj,tsteps],dtype=complex)
    
    #Apportions the raw array by each trajectory
    for i in range(ntraj):
        ith_traj=np.zeros([1,tsteps],dtype=np.ndarray)
        for j in range(tsteps):
            ith_traj[0,j]=raw[i,j]
        jobs.append(job_server.submit(M_check_Single, (ith_traj,guess,tsteps), (), ("numpy as np","M_maximize_3q as M3",)))
    print "All Jobs Submitted"
    #Records the results from the individual jobs in an array

    for i in range(ntraj):
        job=jobs[i]
        print i,"th trajectory complete"
        qth_smlist=job()
        for j in range(tsteps):
            maximized[i,j]=qth_smlist[j]
         
            
    #Averages the array
    avgMlist=np.zeros(tsteps,dtype=complex)
    for j in range(tsteps):
        Mmax=0
        for i in range(ntraj):
            Mmax=Mmax+maximized[i,j]
        Mmax=abs(Mmax/float(ntraj))
        avgMlist[j]=Mmax
    avgMlist=np.real(avgMlist)
    return avgMlist

