#General Functions required for the program

#Setup Functions:

import qutip as qt
from file_io import *
from entanglement_MC import *
from nonlocal_MC import *
from entanglement_DM import *
from nonlocal_DM import *
from graphing import *
import numpy as np
import time,pp

from math import sin
from math import cos

#General and Collapse Operators

I=qt.qeye(2)

sm1=qt.tensor(qt.sigmam().dag(),I,I)      #destruction operator for qubit excitations for cavity+qubit system
sm2=qt.tensor(I,qt.sigmam().dag(),I)    #Also to note: sigmam() is actually the raising operator. sigmam().dag() is the lowering operator.
sm3=qt.tensor(I,I,qt.sigmam().dag())

#Creates pauli operators for the qubits

A=qt.tensor(qt.sigmax(),I,I)    #Creates the pauli operators for each different qubit
B=qt.tensor(qt.sigmay(),I,I)
C=qt.tensor(qt.sigmaz(),I,I)    #Example: Q=Sigma z operator for qubit 1 
D=qt.tensor(I,qt.sigmax(),I)
E=qt.tensor(I,qt.sigmay(),I)
F=qt.tensor(I,qt.sigmaz(),I)
G=qt.tensor(I,I,qt.sigmax())
H=qt.tensor(I,I,qt.sigmay())
K=qt.tensor(I,I,qt.sigmaz())

u=A.shape

O=np.zeros(u,dtype=complex)  #Takes the above Qobj qutip classes and turns them into faster numpy arrays for minimizing
M=np.zeros(u,dtype=complex)
Q=np.zeros(u,dtype=complex)
R=np.zeros(u,dtype=complex)
S=np.zeros(u,dtype=complex)
T=np.zeros(u,dtype=complex)
U=np.zeros(u,dtype=complex)
V=np.zeros(u,dtype=complex)
W=np.zeros(u,dtype=complex)

for i in range(u[0]):       #The loop that creates the numpy arrays for the pauli operators
    for j in range(u[1]):
        O[i,j]=A[i,j]
        M[i,j]=B[i,j]
        Q[i,j]=C[i,j]
        R[i,j]=D[i,j]
        S[i,j]=E[i,j]
        T[i,j]=F[i,j]
        U[i,j]=G[i,j]
        V[i,j]=H[i,j]
        W[i,j]=K[i,j]

sigma1=np.array([O,M,Q],dtype=complex)    #Pauli vector, used to compute the dot product for each vector later
sigma2=np.array([R,S,T],dtype=complex)
sigma3=np.array([U,V,W],dtype=complex)


def S_operators(gamma1,gamma2,gamma3,know):
    if know==0:#Calculates values with no knowledge of which qubit jumps

        #collapse operators
        s=np.sqrt(gamma1)*sm1+np.sqrt(gamma2)*sm2+np.sqrt(gamma3)*sm3 
        slist=[s]

    if know==1:#in the case we know which qubit jumps
        
        #collapse operators
        s1=np.sqrt(gamma1)*sm1 
        s2=np.sqrt(gamma2)*sm2
        s3=np.sqrt(gamma3)*sm3
        slist=[s1,s2,s3]
        
    return slist


#Density Matrix Evolution Solver

def mastersolve(Data):
    #run master equation solver

    print "running ME Solver..."
    rawdm=qt.mesolve(Data.H,Data.psi0,Data.tlist,Data.slist,[]) #This runs the solver with whichever collapse operators and hamiltonian are chosen
    Data.entire_raw=rawdm    
    rawdm=rawdm.states
    Data.rawq=rawdm
    #Since the analysis always bogs down, and the raw.states data structure can be very large,
    #This will turn it into a numpy array rather than a qobj for purposes of speed.
    print "numpying"
    u=len(rawdm)
    rawarray=np.zeros(u,dtype=np.ndarray)
    for i in range(u): #Each Timestep
        rawi=rawdm[i]    #Calls the i,jth element of the state vector structure
        xary=np.zeros([8,8],dtype=complex) #Defines the new array for the state vectors

        for q in range(8):
            for j in range(8):
                xary[q,j]=rawi[q,j] #Turns the qobj to a numpy array
        rawarray[i]=xary      #Writes the element to the array
    Data.raw=rawarray                #Removes the old data structure. 

    return    

#Monte Carlo Solver

def solve(Data,ntraj):
    #run monte-carlo solver

    print "running Monte Carlo Solver..."
    raw=qt.mcsolve(Data.H,Data.psi0,Data.tlist,Data.slist,[],ntraj) #This runs the solver with whichever collapse operators and hamiltonian are chosen
    Data.entire_raw=raw
    raw=raw.states
    Data.rawq=raw
    #Since the analysis always bogs down, and the raw.states data structure can be very large,
    #This will turn it into a numpy array rather than a qobj for purposes of speed.

    u=raw.shape
    rawarray=np.zeros([u[0],u[1]],dtype=np.ndarray)
    for i in range(u[0]): #Each Trajectory
        for j in range(u[1]): #Each Timestep
            rawij=raw[i,j]    #Calls the i,jth element of the state vector structure
            xary=np.zeros([8,1],dtype=complex) #Defines the new array for the state vectors
            for q in range(8):
                xary[q,0]=rawij[q,0] #Turns the qobj to a numpy array
            rawarray[i,j]=xary      #Writes the element to the array
    Data.raw=rawarray                #Removes the old data structure. 
    
    return 



def Run_record(Data,opts,name,know,H,psi0,ntraj,gamma1,gamma2,gamma3,g12,g23,g31,Y,t0,tf,tsteps,guess):
    Data.infolist=[g12,g23,g31,gamma1,gamma2,gamma3,Y,t0,tf,tsteps,ntraj,know,guess,opts[5]]               #A record of the variables used to produce the graph, recorded as human redable. 
    Data.keylist=["g12","g23","g31","gamma1","gamma2","gamma3","Y","t0","tf","tsteps","ntraj","know","guess","MC_0 or DM_1"]  #A record in the file to know which elements of the list correspond to what. 
    Data.tlist=np.linspace(t0,tf,tsteps)
    Data.H=H
    Data.psi0=psi0
    Data.name=name
    Data.opts=opts
    Data.slist=S_operators(gamma1,gamma2,gamma3,know)

    return
                

# opts is a list with the following=[save maxlists,save raw,calculate entanglement,calculate S,Calculate M,MC(0) DM(1)
def Calculate(opts,name,know,H,psi0,ntraj,gamma1,gamma2,gamma3,g12,g23,g31,Y,t0,tf,tsteps,guess,job_server):
    Data=data_def()
    Run_record(Data,opts,name,know,H,psi0,ntraj,gamma1,gamma2,gamma3,g12,g23,g31,Y,t0,tf,tsteps,guess)
    if opts[5]==0:
        print "Using Quantum Trajectory Method"
        solve(Data,ntraj)
        if opts[2]==1:
            Ent_calc(Data,job_server)
        if opts[3]==1:
            Data.avgSlist,Data.S_maxlistlist=S_calc(Data.raw,guess,ntraj,tsteps,name,opts,job_server)
        if opts[4]==1:
            Data.avgMlist=M_calc(Data.raw,guess,ntraj,tsteps,Data.name,job_server)
    if opts[5]==1:
        print "Using Master Equation Solver Method"
        mastersolve(Data)
        if opts[2]==1:
            Ent_calc_DM(Data,job_server)
        if opts[3]==1:
            Data.avgSlist,Data.S_maxlistlist=S_calc_DM(Data.raw,guess,Data.opts,job_server)
        if opts[4]==1:
            Data.avgMlist,Data.M_Maxlistlist=M_calc_DM(Data.raw,guess,Data.opts,job_server)
    save(Data)

    return Data

def Call_Calculations(opts,name,know,H,psi0,ntraj,gamma1,gamma2,gamma3,g12,g23,g31,Y,t0,tf,tsteps,guess):
    Data=data_def()
    Run_record(Data,opts,name,know,H,psi0,ntraj,gamma1,gamma2,gamma3,g12,g23,g31,Y,t0,tf,tsteps,guess)
    call(Data) 

    return Data 

def DC_Run(opts,name,know,H,psi0,ntraj,gamma1,gamma2,gamma3,g12,g23,g31,Y,t0,tf,tsteps,guess,job_server):
    #nodes is a list of all cluster ip addresses ['10.2.2.2.','10.3.34.3.3' etc.]
    #local_cpu is how many local cups should be used. Default is all.
    t1=time.time()
    time.sleep(1)
    print "Active nodes: ",job_server.get_active_nodes()
    Data=Calculate(opts,name,know,H,psi0,ntraj,gamma1,gamma2,gamma3,g12,g23,g31,Y,t0,tf,tsteps,guess,job_server)
    Graph(Data)
    job_server.print_stats()
    t2=time.time()
    t3=(t2-t1)/60.0
    print "Finished ",name," in ",t3," minutes."
    return
    
def Call_Run(opts,name,know,H,psi0,ntraj,gamma1,gamma2,gamma3,g12,g23,g31,Y,t0,tf,tsteps,guess):
    t1=time.time()
    Data=Call_Calculations(opts,name,know,H,psi0,ntraj,gamma1,gamma2,gamma3,g12,g23,g31,Y,t0,tf,tsteps,guess)
    Graph(Data)
    t2=time.time()
    t3=(t2-t1)/60.0
    print "Finished ",name," in ",t3," minutes."
    return
    


def Test(opts,job_server):
    ntraj=4
    guess=2
    t0=0
    tf=10
    tsteps=3
    #Initial System Parameters
    psi0=1.0/np.sqrt(2)*(qt.tensor(qt.basis(2,0),qt.basis(2,0),qt.basis(2,0))+qt.tensor(qt.basis(2,1),qt.basis(2,1),qt.basis(2,1)))
    gamma1=1.0              #spontaneous emission rate
    gamma2=1.0
    gamma3=1.0
    g12=1.0                    #atom-cavity coupling
    g23=1.0
    g31=1.0
    Y=1.0                 #amplitude of driving field
    know=0
    name='O3_test'
    hbar=1
    H=1j*hbar*Y*(sm1.dag()-sm1)+hbar*g12*(sm1.dag()*sm2+sm2.dag()*sm1)+hbar*g23*(sm2.dag()*sm3+sm3.dag()*sm2)+hbar*g31*(sm3.dag()*sm1+sm1.dag()*sm3)
    DC_Run(opts,name,know,H,psi0,ntraj,gamma1,gamma2,gamma3,g12,g23,g31,Y,t0,tf,tsteps,guess,job_server)
    Call_Run(opts,name,know,H,psi0,ntraj,gamma1,gamma2,gamma3,g12,g23,g31,Y,t0,tf,tsteps,guess)
    print "test, a test, successful"
    return
