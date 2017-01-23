# -*- coding: utf-8 -*-
"""
Created on Thu Aug  4 15:15:10 2016

@author: li

optimize both throughput and connections
"""

#import sys
#sys.path.insert(0, '/home/li/Dropbox/KTH/numerical_analysis/ILPs')

import csv
from gurobipy import *
import numpy as np
from arch4_decomposition_new import Arch4_decompose

np.random.seed(2010)

num_cores=3
num_slots=80

i = 1 # index of start 
time_limit_routing = 2400 # 1000
time_limit_sa = 108 # 10800

filename = 'traffic_matrix.csv'
#    print filename
tm = []
with open(filename) as f:
    reader = csv.reader(f)
    for idx, row in enumerate(reader):
        row = [float(u) for u in row]
        tm.append(row)
tm = np.array(tm)

#%% arch2
betav = np.array([0,1e-5,1e-4, 5e-4, 1e-3, 3e-3, 5e-3, 0.01, 0.1, 1])
efficiency_milp = []
efficiency_heuristic = []
for beta in betav:        
    m = Arch4_decompose(tm, num_slots=num_slots, num_cores=num_cores,alpha=1,beta=beta)
    m.create_model_routing(mipfocus=1,timelimit=1000,mipgap=0.01, method=2)
    m.create_model_sa(mipfocus=1,timelimit=10000,submipnodes=2000,heuristics=1)
    m.sa_heuristic(ascending1=False,ascending2=False)
    m.save_tensor(m.tensor_milp, 'tensor_milp_%e.csv'%beta)
    m.save_tensor(m.tensor_heuristic, 'tensor_heuristic_%e.csv'%beta)
    filename = 'milp_cnk_%e.csv'%beta
    suclist = m.suclist_sa
    m.write_result_csv(filename, suclist)
    filename = 'heuristic_cnk_%e.csv'%beta
    suclist = m.suclist_heuristic
    m.write_result_csv(filename, suclist)
    efficiency_milp.append(m.efficiency_milp)
    efficiency_heuristic.append(m.efficiency_heuristic)
    
with open('efficiency.csv', 'w') as f:
    writer = csv.writer(f, delimiter=',')
    writer.writerow(['beta', 'milp', 'heuristic'])
    for i,b in enumerate(betav):
        writer.writerow([b, efficiency_milp[i], efficiency_heuristic[i]])
