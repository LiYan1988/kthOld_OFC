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
from arch5_decomposition_new import Arch5_decompose

np.random.seed(2010)

num_cores=3
num_slots=80
filename = 'traffic_matrix.csv'
tm = []
with open(filename) as f:
    reader = csv.reader(f)
    for idx, row in enumerate(reader):
        row = [float(u) for u in row]
        tm.append(row)
tm = np.array(tm)

#%% arch5
beta = 1e-05 
m = Arch5_decompose(tm, num_slots=num_slots, num_cores=num_cores,alpha=1,beta=beta)
m.create_model_routing(mipfocus=1,timelimit=3000,mipgap=0.015, method=2, SubMIPNodes=2000, heuristics=0.8)
m.create_model_sa(mipfocus=1,timelimit=25000, method=2, SubMIPNodes=2000, heuristics=0.8)
m.save_tensor(m.tensor_milp, 'tensor_milp_%.2e.csv'%beta)
filename = 'milp_cnk_%.2e.csv'%beta
suclist = m.suclist_sa
m.write_result_csv(filename, suclist)
efficiency_milp = m.efficiency_milp
    
with open('efficiency_%.2e.csv'%beta, 'w') as f:
    writer = csv.writer(f, delimiter=',')
    writer.writerow(['beta', 'milp'])
    writer.writerow([beta, efficiency_milp])