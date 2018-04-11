import Open_3 as O3
import sys,pickle
from os import listdir

pathname=sys.path[0]


filenames=listdir(pathname+"/Data/Calculated/")

for i in range(len(filenames)):
    filename=pathname+"/Data/Calculated/"+filenames[i]
    print filename
    Data=O3.data_def()
    O3.call_from_file(Data,filename)
    if len(Data.tlist)>0:
        Data.opts=[0,0,0,0,0,0]
        if len(Data.avgMlist)>0:
            Data.opts[4]=1
            print len(Data.avgMlist)," M"
        if len(Data.avgSlist)>0:
            Data.opts[3]=1
            print len(Data.avgSlist)," S"
        if len(Data.avgtglist)>0:
            Data.opts[2]=1
            print len(Data.avgtglist)," Tgl"
        print len(Data.tlist)," T"
        print Data.opts

        O3.Graph(Data)
