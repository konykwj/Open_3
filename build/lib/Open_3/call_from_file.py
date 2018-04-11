#Since this won't work in file_io...
import general_functions as gf
import file_io as io
import sys,pickle,os.path
import numpy as np

pathname=sys.path[0]


def call_from_file(filename):
    Data=io.data_def()
    extension = os.path.splitext(filename)[1]
    if extension==".txt":
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
        Data.avgMlist=np.real(Data.avgMlist)
        Data.avgSlist=np.real(Data.avgSlist)
        hbar=1.0
        infolist=Data.infolist
        know=infolist[11]
        gamma1=infolist[3]
        gamma2=infolist[4]
        gamma3=infolist[5]
        t0=infolist[7]
        tf=infolist[8]
        tsteps=infolist[9]
        Data.tlist=np.linspace(t0,tf,tsteps)
        Data.slist=gf.S_operators(gamma1,gamma2,gamma3,know)

    return Data
