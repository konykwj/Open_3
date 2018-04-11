#Saving and Calling functions
import pickle,sys
import numpy as np


pathname=sys.path[0]

def data_def():
    class Data():
        avgSlist=[]
        avgMlist=[]
        avgtglist=[]
        avgcr123list=[]
        avgcr231list=[]
        avgcr312list=[]
        avgvnlist=[]
        psi0=[]
        infolist=[]
        keylist=[]
        name=[]
        H=[]
        S_Maxlistlist=[]
        M_Maxlistlist=[]
        raw=[]
        opts=[]
        tlist=[]
        slist=[]
        pathname=[]
        rawq=[]
        entire_raw=[]
    return Data

#A saving function. Data is a class which contains the information for the trial,
#Opts is a list which contains the following: [Save S_maxlistlist and M_maxlist Y=1 N=0, Save Raw data Y=1 N=0]
def save(Data):
    filename=pathname+"/Data/Calculated/"+str(Data.name)+str(Data.infolist)+".txt"
    f=open(filename,"wb")
    Data.avgSlsit=np.real(Data.avgSlist)
    Data.avgMlist=np.real(Data.avgMlist)
    pickle.dump(Data.avgSlist,f)
    pickle.dump(Data.avgMlist,f)
    pickle.dump(Data.avgvnlist,f)
    pickle.dump(Data.avgtglist,f)
    pickle.dump(Data.avgcr123list,f)
    pickle.dump(Data.avgcr231list,f)
    pickle.dump(Data.avgcr312list,f)
    pickle.dump(Data.psi0,f)
    pickle.dump(Data.infolist,f)
    pickle.dump(Data.keylist,f)
    pickle.dump(Data.name,f)
    pickle.dump(Data.H,f)
    pickle.dump(Data.opts,f)
    f.close()

    if Data.opts[0]==1:
        filename=pathname+"/Data/Maxlists/"+str(Data.name)+str(Data.infolist)+".txt"
        f=open(filename,"wb")
        pickle.dump(Data.S_Maxlistlist,f)
        pickle.dump(Data.M_Maxlistlist,f)
        pickle.dump(Data.psi0,f)
        pickle.dump(Data.infolist,f)
        pickle.dump(Data.keylist,f)
        pickle.dump(Data.name,f)
        pickle.dump(Data.H,f)
        pickle.dump(Data.opts,f)
        f.close()
    if Data.opts[1]==1:
        filename=pathname+"/Data/Raw/"+str(Data.name)+str(Data.infolist)+".txt"
        f=open(filename,"wb")
        pickle.dump(Data.entire_raw,f)
        pickle.dump(Data.psi0,f)
        pickle.dump(Data.infolist,f)
        pickle.dump(Data.keylist,f)
        pickle.dump(Data.name,f)
        pickle.dump(Data.H,f)
        pickle.dump(Data.opts,f)
        f.close()
    return




def call(Data):

    filename=pathname+"/Data/Calculated/"+str(Data.name)+str(Data.infolist)+".txt"
    f=open(filename,"rb")
    Data.avgSlist=pickle.load(f)
    Data.avgMlist=pickle.load(f)
    Data.avgvnlist=pickle.load(f)
    Data.avgtglist=pickle.load(f)
    Data.avgcr123list=pickle.load(f)
    Data.avgcr231list=pickle.load(f)
    Data.avgcr312list=pickle.load(f)
    Data.psi0=pickle.load(f)
    Data.infolist=pickle.load(f)
    Data.keylist=pickle.load(f)
    Data.name=pickle.load(f)
    Data.H=pickle.load(f)
    Data.opts=pickle.load(f)
    f.close()

    Data.avgSlsit=np.real(Data.avgSlist)
    Data.avgMlist=np.real(Data.avgMlist)
    if Data.opts[0]==1:
        filename=pathname+"/Data/Maxlists/"+str(Data.name)+str(Data.infolist)+".txt"
        f=open(filename,"rb")
        Data.S_Maxlistlist=pickle.load(f)
        Data.M_Maxlistlist=pickle.load(f)
        Data.psi0=pickle.load(f)
        Data.infolist=pickle.load(f)
        Data.keylist=pickle.load(f)
        Data.name=pickle.load(f)
        Data.H=pickle.load(f)
        Data.opts=pickle.load(f)
        f.close()
    if Data.opts[1]==1:
        filename=pathname+"/Data/raw/"+str(Data.name)+str(Data.infolist)+".txt"
        f=open(filename,"rb")
        Data.entire_raw=pickle.load(f)
        Data.psi0=pickle.load(f)
        Data.infolist=pickle.load(f)
        Data.keylist=pickle.load(f)
        Data.name=pickle.load(f)
        Data.H=pickle.load(f)
        Data.opts=pickle.load(f)
        f.close()


    return 



def combinedc(name,know,t0,tf,ntrajlist,Y,g12,g23,g31,gamma1,gamma2,gamma3,tsteps):
    
    lgavgtglist=np.zeros(tsteps)
    lgavgcr123list=np.zeros(tsteps)
    lgavgcr231list=np.zeros(tsteps)
    lgavgcr312list=np.zeros(tsteps)
    ntrajsum=ntrajlist[0]*len(ntrajlist)
    
    for i in range(len(ntrajlist)):
        ntraj=int(ntrajlist[i])
        avgtglist,avgcr123list,avgcr231list,avgcr312list,psi0,infolist,keylist,name=call_calculations(name,know,t0,tf,ntraj,Y,g12,g23,g31,gamma1,gamma2,gamma3,tsteps)
        for j in range(int(float(ntraj)-ntrajlist[0])):
            avgtglist=np.delete(avgtglist,-1,1)
            avgcr123list=np.delete(avgcr123list,-1,1)
            avgcr231list=np.delete(avgcr231list,-1,1)
            avgcr312list=np.delete(avgcr312list,-1,1)
        ntraj=float(ntraj)
        lgavgtglist=avgtglist*ntraj+lgavgtglist
        lgavgcr123list=avgcr123list*ntraj+lgavgcr123list
        lgavgcr231list=avgcr231list*ntraj+lgavgcr231list
        lgavgcr312list=avgcr312list*ntraj+lgavgcr312list
        
    lgavgtglist=lgavgtglist/ntrajsum
    lgavgcr123list=lgavgcr123list/ntrajsum
    lgavgcr231list=lgavgcr231list/ntrajsum
    lgavgcr312list=lgavgcr312list/ntrajsum

    ntraj=int(ntrajsum)
    infolist=[g12,g23,g31,gamma1,gamma2,gamma3,Y,t0,tf,tsteps,ntraj,know]
    filename=pathname+"/Data/analysis"+name+"know="+str(know)+",t0=" +str(t0)+", tf="+str(tf)+", tsteps="+str(tsteps)+", ntraj="+str(ntraj)+" , Y="+str(Y)+" ,g12="+str(g12)+" ,g23="+str(g23)+" ,g31="+str(g31)+" ,gamma1="+str(gamma1)+" ,gamma2="+str(gamma2)+" ,gamma3="+str(gamma3)+".txt"
    f=open(filename,"wb")
    pickle.dump(lgavgtglist,f)
    pickle.dump(lgavgcr123list,f)
    pickle.dump(lgavgcr231list,f)
    pickle.dump(lgavgcr312list,f)
    pickle.dump(psi0,f)
    pickle.dump(infolist,f)
    pickle.dump(keylist,f)
    pickle.dump(name,f)
    f.close()

    return
