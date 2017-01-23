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

i = 19 
time_limit_routing = 1200 # 1000
time_limit_sa = 108 # 10800

filename = 'traffic_matrix_old_'+str(i)+'.csv'
#    print filename
tm = []
with open(filename) as f:
    reader = csv.reader(f)
    for idx, row in enumerate(reader):
        row = [float(u) for u in row]
        tm.append(row)

tm = np.array(tm)
#%% arch2
betav = np.array([8e-2, 1e-1])
connection_ub = []
throughput_ub = []
obj_ub = []

connection_lb = []
throughput_lb = []
obj_lb = []

connection_he = []
throughput_he = []
obj_he = []

for beta in betav:        
    m = Arch5_decompose(tm, num_slots=num_slots, num_cores=num_cores, 
        alpha=1,beta=beta)

    m.create_model_routing(mipfocus=1,timelimit=1800,mipgap=0.01, method=2)
    connection_ub.append(m.connection_ub_)
    throughput_ub.append(m.throughput_ub_)
    obj_ub.append(m.obj_ub_)

    m.create_model_sa(mipfocus=1,timelimit=10800,mipgap=0.01, method=2, 
                      SubMIPNodes=2000, heuristics=0.8)
    connection_lb.append(m.connection_lb_)
    throughput_lb.append(m.throughput_lb_)
    obj_lb.append(m.obj_lb_)
    m.write_result_csv('cnklist_lb_%d_%.2e.csv'%(i,beta), m.cnklist_lb)
    
    connection_lb.append(0)
    throughput_lb.append(0)
    obj_lb.append(0)

    m.heuristic()
    connection_he.append(m.obj_heuristic_connection_)
    throughput_he.append(m.obj_heuristic_throughput_)
    obj_he.append(m.obj_heuristic_)
    m.write_result_csv('cnklist_heuristic_%d_%.2e.csv'%(i,beta), m.cnklist_heuristic_)

result = np.array([betav,
                   connection_ub,throughput_ub,obj_ub,
                   connection_lb,throughput_lb,obj_lb,
                   connection_he,throughput_he,obj_he]).T
file_name = "result_pareto_arch5_old_5_{}.csv".format(i)
with open(file_name, 'w') as f:
    writer = csv.writer(f, delimiter=',')
    writer.writerow(['beta', 'connection_ub', 'throughput_ub', 
    'obj_ub', 'connection_lb', 'throughput_lb', 'obj_lb',
    'connection_he', 'throughput_he', 'obj_he'])
    writer.writerows(result)
