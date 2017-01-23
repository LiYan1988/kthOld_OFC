# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 09:38:02 2016

@author: li
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

result_arch4_ub = []
result_arch1_ub = []
result_arch2_ub = []
result_arch5_ub = []
result_arch4_lb = []
result_arch1_lb = []
result_arch2_lb = []
result_arch5_lb = []
total_cnk = []

for i in range(10,15):
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
    print "\n"
    print total_cnk
    print "\n"

    #%% arch4    
    m = Arch4_decompose(tm, num_slots=num_slots, num_cores=num_cores)
    m.create_model_routing(mipfocus=1,timelimit=1000,mipgap=0.01)
    tmp = -m.model_routing.objVal
    result_arch4_ub.append(tmp)
    try:
        m.create_model_sa(mipfocus=1,timelimit=15000)
        tmpsa = m.model_sa.objVal
    except GurobiError:
        tmpsa = tmp
    tmp -= tmpsa
    result_arch4_lb.append(tmp)
    print "\n"
    print result_arch4_ub
    print result_arch4_lb
    print "\n"
    
    #%% arch1
    m = ModelSDM_arch1(tm, num_slots=num_slots, num_cores=num_cores)
    m.create_model(mipfocus=1, timelimit=1000,mipgap=0.01)
    result_arch1_ub.append(-m.model.objVal)
    result_arch1_lb.append(-m.model.objVal)
    print "\n"
    print result_arch1_ub
    print result_arch1_lb
    print "\n"
    
    #%% arch2
    m = Arch2_decompose(tm, num_slots=num_slots, num_cores=num_cores)
    m.create_model_routing(mipfocus=1,timelimit=1000,mipgap=0.01)
    tmp = -m.model_routing.objVal
    result_arch2_ub.append(tmp)
    try:
        m.create_model_sa(mipfocus=1,timelimit=9000)
        if m.model_sa.objVal<tmp:
            tmpsa = m.model_sa.objVal
    except GurobiError:
        tmpsa = tmp
    tmp -= tmpsa
    result_arch2_lb.append(tmp)
    print "\n"
    print result_arch2_ub
    print result_arch2_lb
    print "\n"
    
    #%% arch5
    m = Arch5_decompose(tm, num_slots=num_slots, num_cores=num_cores)
    m.create_model_routing(mipfocus=1, timelimit=1000, mipgap=0.01)
    tmp = m.n_suc_routing
    result_arch5_ub.append(tmp)
    try:
        m.create_model_sa(mipfocus=1, timelimit=9000)
        tmpsa = m.model_sa.objVal
    except GurobiError:
        tmpsa = 0
    tmp -= tmpsa
    result_arch5_lb.append(tmp)
    print "\n"
    print result_arch5_ub
    print result_arch5_lb
    print "\n"
    
result = np.array([result_arch1_ub,result_arch1_lb,result_arch2_ub,result_arch2_lb,
                   result_arch4_ub,result_arch4_lb,result_arch5_ub,result_arch5_lb,total_cnk]).transpose()
with open('result3.csv', 'w') as f:
    writer = csv.writer(f, delimiter=',')
    writer.writerow(['arch1_ub', 'arch1_lb', 'arch2_ub', 'arch2_lb', 
    'arch4_ub', 'arch4_lb', 'arch5_ub', 'arch5_lb', 'total_cnk'])
    writer.writerows(result)