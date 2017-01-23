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

num_cores=10
num_slots=320

i = 2 
time_limit_routing = 3600 
time_limit_sa = 10800 

filename = 'traffic_matrix_pod250_load50_'+str(i)+'.csv'

tm = []
with open(filename) as f:
    reader = csv.reader(f)
    for idx, row in enumerate(reader):
        row = [float(u) for u in row]
        tm.append(row)

tm = np.array(tm)
#%% arch2
corev = np.array([1, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20])
#corev = np.array([1, 2])
connection_ub = []
throughput_ub = []
obj_ub = []

connection_lb = []
throughput_lb = []
obj_lb = []

connection_he = []
throughput_he = []
obj_he = []

for c in corev:        
    m = Arch2_decompose(tm, num_slots=num_slots, num_cores=c, 
        alpha=1,beta=0, num_guard_slot=0) 

    m.create_model_routing(mipfocus=1,timelimit=7200,mipgap=0.01, method=2)
    connection_ub.append(m.connection_ub_)
    throughput_ub.append(m.throughput_ub_)
    obj_ub.append(m.obj_ub_)

#    m.create_model_sa(mipfocus=1,timelimit=10800,mipgap=0.01, method=2, 
#        SubMIPNodes=2000, heuristics=0.8)
#    connection_lb.append(m.connection_lb_)
#    throughput_lb.append(m.throughput_lb_)
#    obj_lb.append(m.obj_lb_)
#    m.write_result_csv('cnklist_lb_%d_%d.csv'%(i,c), m.cnklist_lb)
    
    connection_lb.append(0)
    throughput_lb.append(0)
    obj_lb.append(0)

    m.heuristic()
    connection_he.append(m.obj_heuristic_connection_)
    throughput_he.append(m.obj_heuristic_throughput_)
    obj_he.append(m.obj_heuristic_)
    m.write_result_csv('cnklist_heuristic_i%d_c%d.csv'%(i,c), m.cnklist_heuristic_)

result = np.array([corev,
                   connection_ub,throughput_ub,obj_ub,
                   connection_lb,throughput_lb,obj_lb,
                   connection_he,throughput_he,obj_he]).T
file_name = "result_pareto_arch2_old_pod100_i{}.csv".format(i)
with open(file_name, 'w') as f:
    writer = csv.writer(f, delimiter=',')
    writer.writerow(['#cores', 'connection_ub', 'throughput_ub', 
    'obj_ub', 'connection_lb', 'throughput_lb', 'obj_lb',
    'connection_he', 'throughput_he', 'obj_he'])
    writer.writerows(result)
