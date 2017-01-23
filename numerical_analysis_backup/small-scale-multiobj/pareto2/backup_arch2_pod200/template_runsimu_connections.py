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
from arch2_decomposition_new import Arch2_decompose

np.random.seed(2010)

num_cores=3
num_slots=80

i = 1 # index of start 
time_limit_routing = 2400 # 1000
time_limit_sa = 108 # 10800

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

#%% arch2
betav1 = np.arange(0,0.105,0.005)
betav2 = np.arange(0.15,1.05,0.05)
betav3 = np.arange(10, 110, 10)
betav = np.concatenate((betav1, betav2, betav3))
connection_ub = []
throughput_ub = []
connection_lb = []
throughput_lb = []
obj_ub = []
obj_lb = []
for beta in betav:        
    m = Arch2_decompose(tm, num_slots=num_slots, num_cores=num_cores,alpha=1,beta=beta)
    m.create_model_routing(mipfocus=1,timelimit=time_limit_routing,mipgap=0.01, method=2)
    m.sa_heuristic(ascending1=False,ascending2=False)
    connection_ub.append(m.connections_ub)
    throughput_ub.append(m.throughput_ub)
    obj_ub.append(m.alpha*m.connections_ub+m.beta*m.throughput_ub)
    connection_lb.append(m.obj_sah_connection_)
    throughput_lb.append(m.obj_sah_throughput_)
    obj_lb.append(m.alpha*m.obj_sah_connection_+m.beta*m.obj_sah_throughput_)
#        print m.obj_sah_/float(m.alpha*m.connections_ub+m.beta*m.throughput_ub)
    
result = np.array([betav,connection_ub,throughput_ub,obj_ub,
                   connection_lb,throughput_lb,obj_lb]).T
file_name = "result_pareto_arch2_pod200_{}.csv".format(i)
with open(file_name, 'w') as f:
    writer = csv.writer(f, delimiter=',')
    writer.writerow(['beta', 'connection_ub', 'throughput_ub', 
    'obj_ub', 'connection_lb', 'throughput_lb', 'obj_lb'])
    writer.writerows(result)