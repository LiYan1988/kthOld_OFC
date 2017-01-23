# -*- coding: utf-8 -*-
"""
Created on Thu Aug  4 15:15:10 2016

@author: li

optimize hybrid
"""

#import sys
#sys.path.insert(0, '/home/li/Dropbox/KTH/numerical_analysis/ILPs')

import csv
from gurobipy import *
import numpy as np
from arch4_decomposition import Arch4_decompose
from arch1 import ModelSDM_arch1
from arch2_decomposition import Arch2_decompose
from arch5_decomposition import Arch5_decompose

np.random.seed(2010)

num_cores=3
num_slots=80

n_sim = 1 # number of simulations
n_start = 17 # index of start 
n_end = n_start+n_sim # index of end
time_limit_routing = 1000 # 1000
time_limit_sa = 25200


result = np.zeros((n_sim, 15))
total_cnk = []

for i in range(n_start, n_end):
    filename = 'traffic_matrix__matrix_'+str(i)+'.csv'
#    print filename
    tm = []
    with open(filename) as f:
        reader = csv.reader(f)
        for idx, row in enumerate(reader):
            if idx>11:
                row.pop()
                row = [int(u) for u in row]
                tm.append(row)
    tm = np.array(tm)*25
    total_cnk.append(tm.flatten().astype(bool).sum())
    result[i-n_start, 14] = tm.flatten().astype(bool).sum()
    print "\n"
    print total_cnk
    print "\n"

    #%% arch4    
    print "Architecture 4"
    m = Arch4_decompose(tm, num_slots=num_slots, num_cores=num_cores,alpha=1,beta=0.01)
    m.create_model_routing(mipfocus=1,timelimit=time_limit_routing,mipgap=0.01)
    m.create_model_sa(mipfocus=1,timelimit=time_limit_sa)
    result[i-n_start, 0] = m.connections_lb
    result[i-n_start, 1] = m.connections_ub
    result[i-n_start, 2] = m.throughput_lb
    result[i-n_start, 3] = m.throughput_ub
    
    #%% arch1
    print "Architecutre 1"
    m = ModelSDM_arch1(tm, num_slots=num_slots, num_cores=num_cores,alpha=1,beta=0.01)
    m.create_model(mipfocus=1, timelimit=time_limit_routing,mipgap=0.01)
    result[i-n_start, 4] = m.connections
    result[i-n_start, 5] = m.throughput
    
    #%% arch2
    print "Architecture 2"
    m = Arch2_decompose(tm, num_slots=num_slots, num_cores=num_cores,alpha=1,beta=0.01)
    m.create_model_routing(mipfocus=1,timelimit=time_limit_routing,mipgap=0.01)
    m.create_model_sa(mipfocus=1,timelimit=time_limit_sa)
    result[i-n_start, 6] = m.connections_lb
    result[i-n_start, 7] = m.connections_ub
    result[i-n_start, 8] = m.throughput_lb
    result[i-n_start, 9] = m.throughput_ub
    
    #%% arch5
    print "Architecture 5"
    m = Arch5_decompose(tm, num_slots=num_slots, num_cores=num_cores,alpha=1,beta=0.01)
    m.create_model_routing(mipfocus=1, timelimit=time_limit_routing, mipgap=0.01)
    m.create_model_sa(mipfocus=1, timelimit=time_limit_sa)
    result[i-n_start, 10] = m.connections_lb
    result[i-n_start, 11] = m.connections_ub
    result[i-n_start, 12] = m.throughput_lb
    result[i-n_start, 13] = m.throughput_ub
    
file_name = "result_hybrid_{}to{}.csv".format(n_start, n_end)
with open(file_name, 'w') as f:
    writer = csv.writer(f, delimiter=',')
    writer.writerow(['arch4_connections_lb', 'arch4_connections_ub', 
    'arch4_throughput_lb', 'arch4_throughput_ub', 
    'arch1_connections', 'arch1_throughput', 
    'arch2_connections_lb', 'arch2_connections_ub', 
    'arch2_throughput_lb', 'arch2_throughput_ub', 
    'arch5_connections_lb', 'arch5_connections_ub', 
    'arch5_throughput_lb', 'arch5_throughput_ub', 
    'total_cnk'])
    writer.writerows(result)