# -*- coding: utf-8 -*-
"""
Created on Sat Jun  4 22:42:19 2016

@author: li
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Jun  3 13:10:12 2016

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

result_arch4 = []
result_arch1 = []
result_arch2 = []
result_arch5 = []
total_cnk = []

for i in range(1):
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
    m.create_model_routing(mipfocus=1,timelimit=1000)
    tmp = -m.model_routing.objVal
    try:
        m.create_model_sa(mipfocus=1,timelimit=180000)
        tmpsa = m.model_sa.objVal
    except GurobiError:
        tmpsa = 0
    tmp -= tmpsa
    result_arch4.append(tmp)
    print "\n"
    print result_arch4
    print "\n"
    