# -*- coding: utf-8 -*-
"""
Created on Thu Aug  4 15:15:10 2016

@author: li

optimize both throughput and connections
"""

#import sys
#sys.path.insert(0, '/home/li/Dropbox/KTH/numerical_analysis/ILPs')

import csv
import numpy as np
from arch2_decomposition_new import Arch2_decompose

np.random.seed(2010)

num_cores=3
num_slots=80

i = 1 # index of start 
time_limit_routing = 1200 # 1000
time_limit_sa = 108 # 10800

filename = 'traffic_matrix.csv'
#    print filename
tm = []
with open(filename) as f:
    reader = csv.reader(f)
    for idx, row in enumerate(reader):
        row = [int(round(float(u))) for u in row]
        tm.append(row)
tm = np.array(tm)

#%% arch2
betav = np.array([0, 0.005, 0.01, 0.15, 0.02, 0.03, 0.1, 1])
efficiency_milp = []
efficiency_heuristic = []
for i, beta in enumerate(betav):
    m = Arch2_decompose(tm, num_slots=num_slots, num_cores=num_cores,alpha=1,beta=beta)
    m.create_model_routing(mipfocus=1,timelimit=1000,mipgap=0.01, method=2)
    m.create_model_sa(mipfocus=1,timelimit=10000,heuristics=0.05,submipnodes=2000)
    m.sa_heuristic(ascending1=True,ascending2=False)
    m.save_tensor(m.tensor_milp, 'tensor_milp_%e.csv' % beta)
    m.save_tensor(m.tensor_heuristic, 'tensor_heuristic_%e.csv' % beta)
    m.write_result_csv('milp_cnk_%e.csv'%beta, m.suclist_sa)
    m.write_result_csv('heuristic_cnk%e.csv'%beta, m.suclist_heuristic)
    efficiency_milp.append(m.efficiency_milp)
    efficiency_heuristic.append(m.efficiency_heuristic)
    
with open('efficiency.csv', 'w') as f:
    writer = csv.writer(f, delimiter=',')
    writer.writerow(['beta', 'milp', 'heuristic'])
    for i,b in enumerate(betav):
        writer.writerow([b, efficiency_milp[i], efficiency_heuristic[i]])