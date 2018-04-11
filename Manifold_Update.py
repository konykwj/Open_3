#Create Manifold.
import Open_3 as O3
import sys,os.path
from os import listdir

pathname=sys.path[0]

dir_list=listdir(pathname+"/Data/Calculated/")

Datalist=[]

for i in range (len(dir_list)):
    filename=pathname+"/Data/Calculated/"+dir_list[i]
    extension = os.path.splitext(filename)[1]
    if extension==".txt":
        Data=O3.call_from_file(filename)
        Datalist.append(Data)



filename=pathname+"/Data/Calculated_Manifold.txt"
f=open(filename,"wb")
f.write(str("\t".join(["g12","g23","g31","gamma1","gamma2","gamma3","Y","t0","tf","tsteps",
                 "ntraj","know","guess","MC DM",'SLen','MLen','EntLen','Name'])))
for i in range(len(Datalist)):
    Data=Datalist[i]
    f.write('\n')
    f.write(str("\t".join([str(Data.infolist[0]),str(Data.infolist[1]),str(Data.infolist[2]),
                     str(Data.infolist[3]),str(Data.infolist[4]),str(Data.infolist[5]),
                     str(Data.infolist[6]),str(Data.infolist[7]),str(Data.infolist[8]),
                     str(Data.infolist[9]),str(Data.infolist[10]),str(Data.infolist[11]),
                     str(Data.infolist[12]),str(Data.infolist[13]),str(len(Data.avgSlist)),
                     str(len(Data.avgMlist)),str(len(Data.avgtglist)),str(Data.name)])))
    f.write('\n')
f.close()
