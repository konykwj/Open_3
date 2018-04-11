#Various graphing programs
import pylab as py
from file_io import *
import sys

pathname=sys.path[0]


py.rc('lines',lw=3) 
py.rc('axes',lw=2)
params={'axes.labelsize':20,'xtick.labelsize':15,'ytick.labelsize':15,'text.fontsize':10,'legend.fontsize':16,'lines.markeredgewidth':3,'lines.markerlength':20}
py.rcParams.update(params)

def Graph(Data):
    name=Data.name
    avgcr123list=Data.avgcr123list
    avgcr231list=Data.avgcr231list
    avgcr312list=Data.avgcr312list
    tlist=Data.tlist
    avgSlist=Data.avgSlist
    avgvnlist=Data.avgvnlist
    avgtglist=Data.avgtglist
    avgMlist=Data.avgMlist
    infolist=Data.infolist
    opts=Data.opts

    
    Timegraph_all(opts,name,avgcr123list,avgcr231list,avgcr312list,tlist,avgSlist,avgvnlist,infolist,avgtglist,avgMlist)
    Concurgraph(opts,name,avgSlist,avgcr123list,avgcr231list,avgcr312list,infolist,avgMlist,tlist)
    vnentropygraph(opts,name,avgSlist,avgvnlist,infolist,avgMlist,tlist)
    Tanglegraph(opts,name,avgSlist,avgtglist,infolist,avgMlist,tlist)
    Nonlocal_single(opts,name,avgcr123list,avgcr231list,avgcr312list,tlist,avgSlist,avgvnlist,infolist,avgtglist,avgMlist)
    nonlocal_graph(opts,name,avgSlist,avgMlist,infolist,tlist)
    py.clf()

    return

def Timegraph_all(opts,name,avgcr123list,avgcr231list,avgcr312list,tlist,avgSlist,avgvnlist,infolist,avgtglist,avgMlist):

    py.clf()

    xlist=tlist


    if opts[2]==1:
        ylist=avgtglist
        lable="3-Tangle"
        py.plot(xlist,ylist,'c',label=lable)

        ylist=avgcr123list
        lable="C1(23)"
        py.plot(xlist,ylist,'m',label=lable)

        ylist=avgcr231list
        lable="C2(31)"
        py.plot(xlist,ylist,'g',label=lable)

        ylist=avgcr312list
        lable="C3(12)"
        py.plot(xlist,ylist,'b',label=lable)

    if opts[3]==1:
        ylist=avgSlist
        lable="<S>"
        four_list=np.tile(4,len(tlist))
        py.plot(tlist,four_list,'y--')
        py.plot(xlist,ylist,'k',label=lable)
    if opts[4]==1:
        ylist=avgMlist
        lable="<M>"
        four_list=np.tile(2,len(tlist))
        two_root_two_list=np.tile(2.0*np.sqrt(2),len(tlist))
        py.plot(tlist,four_list,'y--')
        py.plot(tlist,two_root_two_list,"y--")
        py.plot(xlist,ylist,"r",label=lable)

    py.xlabel('Time')
    py.legend(bbox_to_anchor=(.88, 1), loc=2, borderaxespad=0.)
    filename=pathname+"/Figures/ALLvsT/"+name+str(infolist)+" all vs time.png"
    py.savefig(filename)
    return





def Concurgraph(opts,name,avgSlist,avgcr123list,avgcr231list,avgcr312list,infolist,avgMlist,tlist):
    if opts[2]==1:
        for i in range(2):
            py.clf()
            four_xlist=np.linspace(0,1,len(avgcr123list))
            if i==0 and opts[3]==1:
                four_list=np.tile(4,len(avgcr123list))
                ylist=avgSlist
                filename=pathname+"/Figures/SvsCON/"+name+str(infolist)+" smax vs concur.png"
                py.ylabel('Max <S>')


                xlist=avgcr123list
            
                lable="C1(23)"
                color='blue'
                py.scatter(xlist,ylist,s=10,c=color,linewidth=0.5,label=lable)
                        
                xlist=avgcr231list
                lable="C2(31)"
                color='red'
                py.scatter(xlist,ylist,s=10,c=color,linewidth=0.5,label=lable)

                xlist=avgcr312list
                lable="C3(12)"
                color='green'
                py.scatter(xlist,ylist,s=10,c=color,linewidth=0.5,label=lable)

                py.plot(four_xlist,four_list,'k--')
                        
                py.xlabel('Concurrences')
                py.legend(bbox_to_anchor=(.88, 1), loc=2, borderaxespad=0.)
                py.savefig(filename)

            if i==1 and opts[4]==1:
                four_list=np.tile(2,len(avgcr123list))
                two_root_two_list=np.tile(2.0*np.sqrt(2),len(avgcr123list))
                py.plot(four_xlist,four_list,'k--')
                py.plot(four_xlist,two_root_two_list,"k--")
                
                ylist=avgMlist
                filename=pathname+"/Figures/MvsCON/"+name+str(infolist)+" Mmax vs concur.png"
                py.ylabel('Max <M>')

                xlist=avgcr123list
                
                lable="C1(23)"
                color='blue'
                py.scatter(xlist,ylist,s=10,c=color,linewidth=0.5,label=lable)
                        
                xlist=avgcr231list
                lable="C2(31)"
                color='red'
                py.scatter(xlist,ylist,s=10,c=color,linewidth=0.5,label=lable)

                xlist=avgcr312list
                lable="C3(12)"
                color='green'
                py.scatter(xlist,ylist,s=10,c=color,linewidth=0.5,label=lable)

                        
                py.xlabel('Concurrences')
                py.legend(bbox_to_anchor=(.88, 1), loc=2, borderaxespad=0.)
                py.savefig(filename)
    return



def vnentropygraph(opts,name,avgSlist,avgvnlist,infolist,avgMlist,tlist):
    if opts[2]==1:
        four_xlist=np.linspace(0,.5,len(avgvnlist))
        for i in range(2):
            py.clf()
            if i==0 and opts[3]==1:
                four_list=np.tile(4,len(avgvnlist))
                ylist=avgSlist
                filename=pathname+"/Figures/SvsVN/"+name+str(infolist)+" smax vs vn.png"
                py.ylabel('Max <S>')
                py.plot(four_xlist,four_list,'k--')
                xlist=avgvnlist
                py.scatter(xlist,ylist,s=10,linewidth=0.5)
                py.xlabel('Von Neumann Entropy')
                py.legend(bbox_to_anchor=(.88, 1), loc=2, borderaxespad=0.)   
                py.savefig(filename)
                
            if i==1 and opts[4]==1:
                four_list=np.tile(2,len(avgvnlist))
                two_root_two_list=np.tile(2.0*np.sqrt(2),len(avgvnlist))
                py.plot(four_xlist,four_list,'k--')
                py.plot(four_xlist,two_root_two_list,"k--")
                ylist=avgMlist
                filename=pathname+"/Figures/MvsVN/"+name+str(infolist)+" Mmax vs vn.png"
                py.ylabel('Max <M>')
                xlist=avgvnlist
                py.scatter(xlist,ylist,s=10,linewidth=0.5)
                py.xlabel('Von Neumann Entropy')
                py.legend(bbox_to_anchor=(.88, 1), loc=2, borderaxespad=0.)   
                py.savefig(filename)
    return


def Tanglegraph(opts,name,avgSlist,avgtglist,infolist,avgMlist,tlist):
    if opts[2]==1:
        four_xlist=np.linspace(0,1,len(avgtglist))
        for i in range(2):
            py.clf()
            if i==0 and opts[3]==1:
                four_list=np.tile(4,len(avgtglist))
                ylist=avgSlist
                filename=pathname+"/Figures/SvsTGL/"+name+str(infolist)+" smax vs vn.png"
                py.ylabel('Max <S>')
                py.plot(four_xlist,four_list,'k--')
                xlist=avgtglist
                py.scatter(xlist,ylist,s=10,linewidth=0.5)
                py.xlabel('Three Tangle')
                py.legend(bbox_to_anchor=(.88, 1), loc=2, borderaxespad=0.)   
                py.savefig(filename)

            if i==1 and opts[4]==1:
                four_list=np.tile(2,len(avgtglist))
                two_root_two_list=np.tile(2.0*np.sqrt(2),len(avgtglist))
                py.plot(four_xlist,four_list,'k--')
                py.plot(four_xlist,two_root_two_list,"k--")
                ylist=avgMlist
                filename=pathname+"/Figures/MvsTGL/"+name+str(infolist)+" Mmax vs vn.png"
                py.ylabel('Max <M>')
                xlist=avgtglist
                py.scatter(xlist,ylist,s=10,linewidth=0.5)
                py.xlabel('Three Tangle')
                py.legend(bbox_to_anchor=(.88, 1), loc=2, borderaxespad=0.)   
                py.savefig(filename)

    return

def nonlocal_graph(opts,name,avgSlist,avgMlist,infolist,tlist):
    if opts[3]==1 and opts[4]==1:
        py.clf()
        if min(avgSlist)<4.0:
            four_xlist=np.linspace(min(avgMlist),max(avgMlist),len(avgSlist))
            four_list=np.tile(4,len(avgMlist))
            py.plot(four_xlist,four_list,'k--')
        if min(avgMlist)<2.0:
            two_xlist=np.linspace(min(avgSlist),max(avgSlist),len(avgMlist))
            two_list=np.tile(2,len(avgSlist))
            two_root_two_list=np.tile(2.0*np.sqrt(2),len(avgSlist))
            py.plot(two_xlist,two_list,'k--')
            py.plot(two_xlist,two_root_two_list,"k--")

        ylist=avgSlist
        filename=pathname+"/Figures/SvsM/"+name+str(infolist)+" smax vs mmax.png"
        py.ylabel('Max <S>')
        xlist=avgMlist
        py.scatter(xlist,ylist,s=10,linewidth=0.5)
        py.xlabel('Max <M>')
        py.legend(bbox_to_anchor=(.88, 1), loc=2, borderaxespad=0.)   
        py.savefig(filename)

    return


def Nonlocal_single(opts,name,avgcr123list,avgcr231list,avgcr312list,tlist,avgSlist,avgvnlist,infolist,avgtglist,avgMlist):
    py.clf()
    xlist=tlist
    if opts[2]==1:
        for i in range(2):
            py.clf()
            if i==0 and opts[3]==1:
                four_list=np.tile(4,len(tlist))
                
                ylist=avgSlist
                py.plot(tlist,four_list,'--')
                lable="<S> max"
                py.plot(xlist,ylist,label=lable)
                py.xlabel('Time')
                py.ylabel('<S> max')
                py.legend(bbox_to_anchor=(.88, 1), loc=2, borderaxespad=0.)
                filename=pathname+"/Figures/SvsT/"+name+str(infolist)+" smax vs time.png"
                py.savefig(filename)

                py.clf()
                ylist=avgcr123list
                py.plot(tlist,four_list,'--')
                lable="C1(23)"
                py.plot(xlist,ylist,label=lable)
                ylist=avgSlist
                lable="<S> max"
                py.plot(xlist,ylist,label=lable)
                py.xlabel('Time')
                py.legend(bbox_to_anchor=(.88, 1), loc=2, borderaxespad=0.)
                filename=pathname+"/Figures/SvsT/Concur/"+name+str(infolist)+" smax, c123 vs time.png"
                py.savefig(filename)

                py.clf()
                ylist=avgcr231list
                py.plot(tlist,four_list,'--')
                lable="C2(31)"
                py.plot(xlist,ylist,label=lable)
                py.xlabel('Time')
                ylist=avgSlist
                lable="<S> max"
                py.plot(xlist,ylist,label=lable)
                py.legend(bbox_to_anchor=(.88, 1), loc=2, borderaxespad=0.)
                filename=pathname+"/Figures/SvsT/Concur/"+name+str(infolist)+" smax, c231 vs time.png"
                py.savefig(filename)

                py.clf()
                ylist=avgcr312list
                py.plot(tlist,four_list,'--')
                lable="C3(12)"
                py.plot(xlist,ylist,label=lable)
                py.xlabel('Time')
                ylist=avgSlist
                lable="<S> max"
                py.plot(xlist,ylist,label=lable)
                py.legend(bbox_to_anchor=(.88, 1), loc=2, borderaxespad=0.)
                filename=pathname+"/Figures/SvsT/Concur/"+name+str(infolist)+" smax, c312 vs time.png"
                py.savefig(filename)

                py.clf()
                ylist=avgvnlist
                py.plot(tlist,four_list,'--')
                lable="VN Entropy"
                py.plot(xlist,ylist,label=lable)
                py.xlabel('Time')
                ylist=avgSlist
                lable="<S> max"+name
                py.plot(xlist,ylist,label=lable)
                py.legend(bbox_to_anchor=(.88, 1), loc=2, borderaxespad=0.)
                filename=pathname+"/Figures/SvsT/VonNeumann/"+name+str(infolist)+" smax, vn vs time.png"
                py.savefig(filename)


                py.clf()
                ylist=avgtglist
                py.plot(tlist,four_list,'--')
                lable="Tangle"
                py.plot(xlist,ylist,label=lable)
                py.xlabel('Time')
                ylist=avgSlist
                lable="<S> max"
                py.plot(xlist,ylist,label=lable)
                py.legend(bbox_to_anchor=(.88, 1), loc=2, borderaxespad=0.)
                filename=pathname+"/Figures/SvsT/Tangle/"+name+str(infolist)+" smax, tangle vs time.png"
                py.savefig(filename)

            if i==1 and opts[4]==1:
                four_list=np.tile(2,len(tlist))
                two_root_two_list=np.tile(2.0*np.sqrt(2),len(tlist))
                
                py.clf()
                ylist=avgMlist
                py.plot(tlist,four_list,'--')
                py.plot(tlist,two_root_two_list,"--")
                lable="<M> max"
                py.plot(xlist,ylist,label=lable)
                py.xlabel('Time')
                py.ylabel('<M> max')
                py.legend(bbox_to_anchor=(.88, 1), loc=2, borderaxespad=0.)
                filename=pathname+"/Figures/MvsT/"+name+str(infolist)+" Mmax vs time.png"
                py.savefig(filename)

                py.clf()
                ylist=avgcr123list
                py.plot(tlist,four_list,'--')
                py.plot(tlist,two_root_two_list,"--")
                lable="C1(23)"
                py.plot(xlist,ylist,label=lable)
                ylist=avgMlist
                lable="<M> max"
                py.plot(xlist,ylist,label=lable)
                py.xlabel('Time')
                py.legend(bbox_to_anchor=(.88, 1), loc=2, borderaxespad=0.)
                filename=pathname+"/Figures/MvsT/Concur/"+name+str(infolist)+" Mmax, c123 vs time.png"
                py.savefig(filename)

                py.clf()
                ylist=avgcr231list
                py.plot(tlist,four_list,'--')
                py.plot(tlist,two_root_two_list,"--")
                lable="C2(31)"
                py.plot(xlist,ylist,label=lable)
                py.xlabel('Time')
                ylist=avgMlist
                lable="<M> max"
                py.plot(xlist,ylist,label=lable)
                py.legend(bbox_to_anchor=(.88, 1), loc=2, borderaxespad=0.)
                filename=pathname+"/Figures/MvsT/Concur/"+name+str(infolist)+" Mmax, c231 vs time.png"
                py.savefig(filename)

                py.clf()
                ylist=avgcr312list
                py.plot(tlist,four_list,'--')
                py.plot(tlist,two_root_two_list,"--")
                lable="C3(12)"
                py.plot(xlist,ylist,label=lable)
                py.xlabel('Time')
                ylist=avgMlist
                lable="<M> max"
                py.plot(xlist,ylist,label=lable)
                py.legend(bbox_to_anchor=(.88, 1), loc=2, borderaxespad=0.)
                filename=pathname+"/Figures/MvsT/Concur/"+name+str(infolist)+" Mmax, c312 vs time.png"
                py.savefig(filename)

                py.clf()
                ylist=avgvnlist
                py.plot(tlist,four_list,'--')
                py.plot(tlist,two_root_two_list,"--")
                lable="VN Entropy"
                py.plot(xlist,ylist,label=lable)
                py.xlabel('Time')
                ylist=avgMlist
                lable="<M> max"+name
                py.plot(xlist,ylist,label=lable)
                py.legend(bbox_to_anchor=(.88, 1), loc=2, borderaxespad=0.)
                filename=pathname+"/Figures/MvsT/VonNeumann/"+name+str(infolist)+" Mmax, vn vs time.png"
                py.savefig(filename)


                py.clf()
                ylist=avgtglist
                py.plot(tlist,four_list,'--')
                py.plot(tlist,two_root_two_list,"--")
                lable="Tangle"
                py.plot(xlist,ylist,label=lable)
                py.xlabel('Time')
                ylist=avgMlist
                lable="<M> max"
                py.plot(xlist,ylist,label=lable)
                py.legend(bbox_to_anchor=(.88, 1), loc=2, borderaxespad=0.)
                filename=pathname+"/Figures/MvsT/Tangle/"+name+str(infolist)+" Mmax, tangle vs time.png"
                py.savefig(filename)
    
    return



    
