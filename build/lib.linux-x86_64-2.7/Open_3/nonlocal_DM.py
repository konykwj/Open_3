import numpy as np
from general_functions import *
import DM_S_M_maximize_3q as DMSM



############################
#Svetlinchny Routine

def S_check_Single_DM(rho,guess,opts):

    xoptalist=DMSM.S_maximizedm(guess,rho)
    speciallist=DMSM.unique_search(xoptalist)
    maxlist=DMSM.max_culldm(speciallist,rho)
    x=maxlist[0]
    Sm=DMSM.Fadm(x,rho)
    
    if opts[0]==0:
        maxlist=0.0

    return Sm,maxlist


def S_calc_DM(rawdm,guess,opts,job_server): 
    print "beginning S DC..."
    lenlist=len(rawdm)

    avgSlist=np.zeros(lenlist,dtype=float)
    S_Maxlistlist=np.zeros(lenlist,dtype=np.ndarray)

    jobs = []

    #Apportion Jobs
    for j in range(lenlist):
        rho=rawdm[j]
        jobs.append(job_server.submit(S_check_Single_DM, (rho,guess,opts), (), ("numpy as np","import DM_S_M_maximize_3q as DMSM",)))

    #Read Jobs
        
    for j in range(lenlist): #For every timestep...
        job=jobs[j]
        Sm,maxlist=job()
        
        if opts[0]==1:
            S_Maxlistlist[j]=maxlist
        avgSlist[j]=abs(Sm)

        print 100*(1-float(j)/(float(lenlist)-1.0))

    return avgSlist,S_Maxlistlist


#####################################
#Mermin Routine

def M_check_Single_DM(rho,guess,opts):

    xoptalist=DMSM.M_maximizedm(guess,rho)
    speciallist=DMSM.unique_search(xoptalist)
    maxlist=DMSM.max_culldm(speciallist,rho)
    x=maxlist[0]
    M=DMSM.Mdm(x,rho)
    
    if opts[0]==0:
        maxlist=0.0

    return M,maxlist


def M_calc_DM(rawdm,guess,opts,job_server): 
    print "beginning M DC..."
    lenlist=len(rawdm)

    avgMlist=np.zeros(lenlist,dtype=float)
    M_Maxlistlist=np.zeros(lenlist,dtype=np.ndarray)

    jobs = []
    
    #Apportion Jobs
    for j in range(lenlist):
        rho=rawdm[j]
        jobs.append(job_server.submit(M_check_Single_DM, (rho,guess,opts), (), ("numpy as np","import DM_S_M_maximize_3q as DMSM",)))

    #Read Jobs
        
    for j in range(lenlist): 
        job=jobs[j]
        M,maxlist=job()
        
        if opts[0]==1:
            M_Maxlistlist[j]=maxlist
        avgMlist[j]=abs(M)

        print 100*(1-float(j)/(float(lenlist)-1.0))
        
    return avgMlist,M_Maxlistlist


