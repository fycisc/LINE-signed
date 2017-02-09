#!/usr/local/bin/python
from __future__ import print_function

import sys
import numpy as np
import argparse


# convert data file to arff file
# input:
#   data file: (id,vertex_embedding,[context_embedding],...)
#   edge file: (id_source, id_target, weight)

def convert2arff(datafilename,edgefilename, outfilename):
    # use vertex embedding difference as the feature of an edge
    num_edge = 0
    with open(edgefilename,"r") as fo:
        line = fo.readline()
        if len(line.split())>0:
            num_edge += 1   
        while(line):
            line = fo.readline()
            if len(line.split())>0:
                num_edge += 1



    print("Start reading edge data")

    edgedata = np.zeros((num_edge,3),dtype=np.int)
    count = 0
    num_edge_pos = 0
    num_edge_neg = 0
    with open(edgefilename,"r") as fo:
        line = fo.readline()

        while(line):
            items = line.strip().split()
            assert len(items) ==3, " length of edge line should be 3"
            source_id, target_id, weight = items
            weight = float(weight)
            source_id = int(source_id)
            target_id = int(target_id)
            label = np.sign(weight)
            if label>0:
                num_edge_pos += 1
            else:
                num_edge_neg += 1

            edgedata[count,:] = (source_id, target_id, label)
            count += 1
            line = fo.readline()
    print("Finish reading edge data\n")

    print("number of edges: "+str(num_edge))
    print("number of positive edges: "+str(num_edge_pos))
    print("number of negative edges: "+str(num_edge_neg))
    print("positive/negative ratio: "+str(float(num_edge_pos)/float(num_edge_neg)))
    print("")


    dim_embed = 0
    num_embed = 0
    num_vertex = 0

    with open(datafilename, "r") as fo:
        line = fo.readline() # first line: num_vertex, dim_embed, num_embed
        num_vertex, dim_embed, num_embed = map(int,line.strip().split())
    print("embedding dimension: "+ str(dim_embed))
    print("number of embedding per vertex: " + str(num_embed))
    print("number of vertex: " + str(num_vertex))


    embeddata = np.zeros((num_vertex,num_embed,dim_embed),dtype=np.double)
    map_id2index = {}


    print("\nStart reading embedding data")

    count = 0
    with open(datafilename, "r") as fo:
        line = fo.readline()
        for i in range(num_vertex):
            vertexid = int(fo.readline())
            map_id2index[vertexid] = count
            for j in range(num_embed):
                line = fo.readline()
                items = line.strip().split()
                assert len(items)==dim_embed, "embedding dimension error"
                embeddata[i,j,:] = items
            count +=1
    print("Finish reading embedding data")


    print("Start writing arff file")
    with open(outfilename, "w") as fo:
        # data name
        fo.write("@relation train\n\n")
        # attributes: dim_embed features + 1 label
        for i in range(dim_embed*2):
            fo.write("@attribute component" +str(i+1)+" numeric\n")
        fo.write("@attribute label {p,n}\n\n")

        # date section
        fo.write("@data\n")
        for i in range(num_edge):
            s_id, t_id, label = edgedata[i,:]
            s_index = map_id2index[s_id]
            t_index = map_id2index[t_id]
            line = ",".join(map(str,embeddata[s_index,0,:])) \
                    + "," + ",".join(map(str,embeddata[t_index,0,:]))+","
            fo.write(line)
            if label>0:
                fo.write("p\n")
            else:
                fo.write("n\n")

            # output progess
            l = 0
            if i%(num_edge/100)==0:
                s = str(i/(num_edge/100))+"%"
                sys.stdout.write("\b"*l)
                sys.stdout.write(s)
                sys.stdout.flush()
                l = len(s)



if __name__ == "__main__":
    print("=========="+sys.argv[0]+"=============")

    # parsing command line arguments
    parser = argparse.ArgumentParser(description='simple arff converter')
    parser.add_argument('-e','--edge',dest='edgefilename',required=True)
    parser.add_argument('-d','--data','--embedding',dest='datafilename',required=True)
    parser.add_argument('-o','--out','--output',dest='outfilename',default='~/Desktop/train.arff')
    class C(object):
        pass
    parserobj = C()
    print(sys.argv[1:])
    parser.parse_args(args=sys.argv[1:],namespace=parserobj)
    edgefilename = parserobj.edgefilename
    datafilename = parserobj.datafilename
    outfilename = parserobj.outfilename
    # print(edgefilename)
    # print(datafilename)
    # print(outfilename)


    # call converter function
    convert2arff(datafilename, edgefilename, outfilename)



















