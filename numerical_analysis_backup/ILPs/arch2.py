# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 17:31:59 2016

@author: li

Modelling for architecture 2
"""

import pandas as pd
from gurobipy import *
from scipy.linalg import toeplitz
import numpy as np
import time
import itertools

class ModelSDM_arch2(object):
    """Create models for different SDM DCN architectures
    """
    def __init__(self, traffic_matrix, num_slots=320, num_cores=10,
                 slot_capacity =25, num_guard_slot=1, num_slot_groups=2):
        """Initialize 
        """
        # traffic matrix
        self.traffic_matrix = traffic_matrix
        # number of PODs
        self.num_pods = traffic_matrix.shape[0]
        # capacity per spectrum slot, Gbps
        self.slot_capacity = slot_capacity
        # number of slot as guardband
        self.num_guard_slot = num_guard_slot
        # number of slots
        self.num_slots = num_slots
        # number of cores
        self.num_cores = num_cores
        # number of total demands
        self.total_demands = sum(self.traffic_matrix.flatten()>0)
        # number of slots per group, only for architecture 3
        self.num_slot_groups = num_slot_groups
        
#    def create_model1(self, **kwargs):
#        """BLP
#        """
#        # Need to consider guardbands
#        # max capacity per core with all spectrum slots
#        c_max = self.num_slots * self.slot_capacity
#        self.tm = self.traffic_matrix.copy()
#        # number of blocked demands at the begining
#        self.num_blocked1 = sum(self.tm.flatten()>c_max)
#        # remove those demands with too large capacities
#        self.tm[self.tm>c_max] = 0
#        
#        # Model data
#        # set of pods, pod_0, ..., pod_(N_p-1)
#        pods = list(range(self.num_pods))
#        # pairs of traffic demands
#        traffic_pairs = tuplelist([(i, j) for i in pods for j in pods
#                            if self.tm[i, j]>0])
#        # create channels for each traffic demand, the number of spectrum slots
#        # in the channel meets the requirement of the demand
#        # A is the matrix to convert x_ijk to z_ijl
#        channels = {}
#        A = {}
#        for i, j in traffic_pairs:
#            if self.tm[i, j] > 0:
#                traffic_slot = int(np.ceil(self.tm[i, j] / 
#                            self.slot_capacity) + self.num_guard_slot)
#                channels[i, j] = list(range(self.num_slots - traffic_slot + 1))
#                c = np.zeros((self.num_slots,))
#                c[:traffic_slot] = 1
#                r = np.zeros((self.num_slots - traffic_slot + 1, ))
#                r[0] = 1
#                A[i, j] = toeplitz(c, r)
#        
#        # set of spectrum slots
#        slots = list(range(self.num_slots))
#        
#        # set of cores
#        cores = list(range(self.num_cores))
#        
#        # Model
#        tic = time.clock()
#        m1 = Model('model_arch2')
#        
#        # Create variables: x_ijk = 1 if POD i to POD j uses channel k
#        bin_pair_channel = {}
#        for i, j in traffic_pairs:
#            for k in channels[i, j]:
#                bin_pair_channel[i, j, k] = m1.addVar(vtype=GRB.BINARY,
#                            name='bin_pair_channel_%s_%s_%s' % (i, j, k))
#                            
#        # Create variables: y_ij = 1 if demand (i, j) is successfully allocated
#        bin_pair = {}
#        for i, j in traffic_pairs:
#            bin_pair[i, j] = m1.addVar(vtype=GRB.BINARY, obj=-1,
#                        name='bin_pair_%s_%s' % (i, j))
#                        
#        # Create variables: z_ijl = 1 if POD i to POD j uses spectrum slot l
#        bin_pair_slot =  {}
#        for i, j in traffic_pairs:
#            for l in slots:
#                bin_pair_slot[i, j, l] = m1.addVar(vtype=GRB.BINARY, 
#                            name='bin_pair_slot_%s_%s_%s' % (i, j, l))
#                            
#        # Create variables: w_ijn^+ = 1 if the out traffic from POD i to POD j 
#        # uses core n, same with w_ijn^- for in traffic
#        bin_pair_core_out = {}
#        bin_pair_core_in = {}
#        for i, j in traffic_pairs:
#            for n in cores:
#                bin_pair_core_out[i, j, n] = m1.addVar(vtype=GRB.BINARY,
#                            name='bin_pair_core_out_%s_%s_%s' % (i, j, n))
#                bin_pair_core_in[i, j, n] = m1.addVar(vtype=GRB.BINARY,
#                            name='bin_pair_core_in_%s_%s_%s' % (i, j, n))
#                            
#        # Create variables: v_ijln^+ = 1 if the out traffic from POD i to POD j
#        # uses spectrum slot l and core n, same for v_ijln^- for in  traffic
#        bin_pair_slot_core_out = {}
#        bin_pair_slot_core_in = {}
#        for i, j in traffic_pairs:
#            for l in slots:
#                for n in cores:
#                    bin_pair_slot_core_out[i, j, l, n] = \
#                        m1.addVar(vtype=GRB.BINARY, 
#                                  name='bin_pair_slot_core_out_%s_%s_%s_%s' % 
#                                  (i, j, l, n))
#                    bin_pair_slot_core_in[i, j, l, n] = \
#                        m1.addVar(vtype=GRB.BINARY, 
#                                  name='bin_pair_slot_core_out_%s_%s_%s_%s' % 
#                                  (i, j, l, n))
#                                  
#        m1.update()
#                                  
#        # Create constraints: y_ij = sum_k x_ijk
#        for i, j in traffic_pairs:
#            m1.addConstr(bin_pair[i, j] == 
#                quicksum(bin_pair_channel[i, j, k] for k in channels[i, j]),
#                         name='con_pair_channel_%s_%s' % (i, j))
#        
#        # Create constraints: y_ij = sum_n w_ijn^+/-
#        for i, j in  traffic_pairs:
#            m1.addConstr(bin_pair[i, j] ==
#                quicksum(bin_pair_core_out[i, j, n] for n in cores),
#                         name='con_pair_core_out_%s_%s' % (i, j))
#            m1.addConstr(bin_pair[i, j] ==
#                quicksum(bin_pair_core_in[i, j, n] for n in cores),
#                         name='con_pair_core_in_%s_%s' % (i, j))
#        
#        # Create constraints: convert channel to slot
#        for i, j in traffic_pairs:
#            for l in slots:
#                m1.addConstr(bin_pair_slot[i, j, l] ==
#                    quicksum(A[i, j][l, c] * bin_pair_channel[i, j, c]
#                    for c in channels[i, j]), 
#                    name='con_channel2slot_%s_%s_%s' % (i, j, l))
#                        
#        # Create constraints: v_ijln^+ = w_ijn^+ * z_ijl, same for v_ijln^-
#        for i, j in traffic_pairs:
#            for l in slots:
#                for n in cores:
#                    m1.addConstr(bin_pair_slot_core_out[i, j, l, n] <=
#                        bin_pair_core_out[i, j, n])
#                    m1.addConstr(bin_pair_slot_core_out[i, j, l, n] <=
#                        bin_pair_slot[i, j, l])
#                    m1.addConstr(bin_pair_slot_core_out[i, j, l, n] >=
#                        bin_pair_core_out[i, j, n] + 
#                        bin_pair_slot[i, j, l] - 1)
#                    m1.addConstr(bin_pair_slot_core_in[i, j, l, n] <=
#                        bin_pair_core_in[i, j, n])
#                    m1.addConstr(bin_pair_slot_core_in[i, j, l, n] <=
#                        bin_pair_slot[i, j, l])
#                    m1.addConstr(bin_pair_slot_core_in[i, j, l, n] >=
#                        bin_pair_core_in[i, j, n] +
#                        bin_pair_slot[i, j, l] - 1)
#                        
#        # Create constraints: one spectrum & core slot can be used by at most
#        # one traffic demand
#        for u in pods:
#            for l in slots:
#                for n in cores:
#                    m1.addConstr(quicksum(bin_pair_slot_core_out[u, j, l, n]
#                                for u, j in traffic_pairs.select(u, '*')) + 
#                                quicksum(bin_pair_slot_core_in[i, u, l, n]
#                                for i, u in traffic_pairs.select('*', u)) <= 1)
#                         
#        # params
#        if len(kwargs):
#            for key, value in kwargs.items():
#                setattr(m1.params, key, value)
#                         
#        m1.optimize()
#        toc = time.clock()
#    
#        self.model1 = m1
#        self.allocated_traffic1 = -m1.objVal
#        self.num_blocked1 += (len(traffic_pairs) - 
#                                self.allocated_traffic1)
#        self.block_rate1 = self.num_blocked1 / self.total_demands
#        self.runtime1 = toc - tic
        
        
    def create_model2(self, **kwargs):
        """ILP
        """
        # Need to consider guardbands
        # max capacity per core with all spectrum slots
        c_max = self.num_slots * self.slot_capacity
        self.tm_arch2 = self.traffic_matrix.copy()
        # number of blocked demands at the begining
        self.num_blocked2 = sum(self.tm_arch2.flatten()>c_max)
        # remove those demands with too large capacities
        self.tm_arch2[self.tm_arch2>c_max] = 0
        
        # Model data
        # set of pods, pod_0, ..., pod_(N_p-1)
        pods = list(range(self.num_pods))
        # pairs of traffic demands
        traffic_pairs = tuplelist([(i, j) for i in pods for j in pods
                            if self.tm_arch2[i, j]>0])
        # traffic capacities
        traffic_capacities = {}
        for i, j in traffic_pairs:
            if self.tm_arch2[i, j] > 0:
                traffic_slot = int(np.ceil(self.tm_arch2[i, j] / 
                            self.slot_capacity) + self.num_guard_slot)
                traffic_capacities[i, j] = traffic_slot
#                print(traffic_slot)
                
        # set of cores
        cores = list(range(self.num_cores))
        
        # Model
        tic = time.clock()
        m2 = Model('model_arch2')
        
        # Create integer variables: 1 <= x_ij <= M, the begin slot of (i, j)
        bin_pair_begin = {}
        for i, j in traffic_pairs:
            bin_pair_begin[i, j] = m2.addVar(vtype=GRB.INTEGER, lb=1,
                ub=self.num_slots+1-traffic_capacities[i, j])
                            
        # Create binary variables: c_ij,n = 1 if (i, j) uses core n
        bin_pair_core_out = {}
        bin_pair_core_in = {}
        for i, j in traffic_pairs:
            for k in cores:
                bin_pair_core_out[i, j, k] = \
                    m2.addVar(vtype=GRB.BINARY, obj=-1)
                bin_pair_core_in[i, j, k] = \
                    m2.addVar(vtype=GRB.BINARY)
                        
        # Create binary variables: d_iu,iv = 1 if x_iu < x_iv, also d_iv,iu
        bin_pair_order =  {}
        for i in pods:
            tmp = list((i, u) for (i, u) in traffic_pairs.select(i, '*'))
            tmp0 = list((u, i) for (u, i) in traffic_pairs.select('*', i))
            tmp.extend(tmp0)
            for u, v in itertools.combinations(tmp, 2):
                bin_pair_order[u, v] = m2.addVar(vtype=GRB.BINARY)
                bin_pair_order[v, u] = m2.addVar(vtype=GRB.BINARY)
                        
        # update model
        m2.update()
        
        bigM = self.num_slots
                                  
        # Create constraints: sum_n c_ij,n <= 1
        for i, j in traffic_pairs:
            m2.addConstr(quicksum(bin_pair_core_out[i, j, k] 
                for k in cores) <= 1)
            m2.addConstr(quicksum(bin_pair_core_out[i, j, k] 
                for k in cores) == 
                quicksum(bin_pair_core_in[i, j, k] 
                for k in cores))
        
        # Create constraints: d_iv,iu + d_iu,iv = 1
        for i in  pods:
            tmp = list((i, u) for (i, u) in traffic_pairs.select(i, '*'))
            tmp0 = list((u, i) for (u, i) in traffic_pairs.select('*', i))
            tmp.extend(tmp0)
            for u, v in itertools.combinations(tmp, 2):
                m2.addConstr(bin_pair_order[u, v] + 
                    bin_pair_order[v, u] == 1)
                for n in cores:
                    if u[0] == i and v[0] == i:
                        m2.addConstr(bin_pair_begin[u[0], u[1]] - 
                            bin_pair_begin[v[0], v[1]] +
                            traffic_capacities[u[0], u[1]] + bigM * 
                            (bin_pair_order[u, v] + 
                            bin_pair_core_out[u[0], u[1], n] + 
                            bin_pair_core_out[v[0], v[1], n]) <= 3 * bigM)
                        m2.addConstr(bin_pair_begin[v[0], v[1]] - 
                            bin_pair_begin[u[0], u[1]] +
                            traffic_capacities[v[0], v[1]] + bigM * 
                            (bin_pair_order[v, u] + 
                            bin_pair_core_out[u[0], u[1], n] + 
                            bin_pair_core_out[v[0], v[1], n]) <= 3 * bigM)
                    elif u[0] == i and v[1] == i:
                        m2.addConstr(bin_pair_begin[u[0], u[1]] - 
                            bin_pair_begin[v[0], v[1]] +
                            traffic_capacities[u[0], u[1]] + bigM * 
                            (bin_pair_order[u, v] + 
                            bin_pair_core_out[u[0], u[1], n] + 
                            bin_pair_core_in[v[0], v[1], n]) <= 3 * bigM)
                        m2.addConstr(bin_pair_begin[v[0], v[1]] - 
                            bin_pair_begin[u[0], u[1]] +
                            traffic_capacities[v[0], v[1]] + bigM * 
                            (bin_pair_order[v, u] + 
                            bin_pair_core_out[u[0], u[1], n] + 
                            bin_pair_core_in[v[0], v[1], n]) <= 3 * bigM)
                    elif u[1] == i and v[0] == i:
                        m2.addConstr(bin_pair_begin[u[0], u[1]] - 
                            bin_pair_begin[v[0], v[1]] +
                            traffic_capacities[u[0], u[1]] + bigM * 
                            (bin_pair_order[u, v] + 
                            bin_pair_core_in[u[0], u[1], n] + 
                            bin_pair_core_out[v[0], v[1], n]) <= 3 * bigM)
                        m2.addConstr(bin_pair_begin[v[0], v[1]] - 
                            bin_pair_begin[u[0], u[1]] +
                            traffic_capacities[v[0], v[1]] + bigM * 
                            (bin_pair_order[v, u] + 
                            bin_pair_core_in[u[0], u[1], n] + 
                            bin_pair_core_out[v[0], v[1], n]) <= 3 * bigM)
                    elif u[1] == i and v[1] == i:
                        m2.addConstr(bin_pair_begin[u[0], u[1]] - 
                            bin_pair_begin[v[0], v[1]] +
                            traffic_capacities[u[0], u[1]] + bigM * 
                            (bin_pair_order[u, v] + 
                            bin_pair_core_in[u[0], u[1], n] + 
                            bin_pair_core_in[v[0], v[1], n]) <= 3 * bigM)
                        m2.addConstr(bin_pair_begin[v[0], v[1]] - 
                            bin_pair_begin[u[0], u[1]] +
                            traffic_capacities[v[0], v[1]] + bigM * 
                            (bin_pair_order[v, u] + 
                            bin_pair_core_in[u[0], u[1], n] + 
                            bin_pair_core_in[v[0], v[1], n]) <= 3 * bigM)
            
                                    
        # params
        if len(kwargs):
            for key, value in kwargs.items():
                setattr(m2.params, key, value)
        
        m2.optimize()
        toc = time.clock()
    
        self.model2 = m2
        self.allocated_traffic2 = -m2.objVal
        self.num_blocked2 += (len(traffic_pairs) - 
                                self.allocated_traffic2)
        self.block_rate2 = self.num_blocked2 / self.total_demands
        self.runtime2 = toc - tic
        
        # Validate the solution by checking if any slot is used by more than 
        # once
        u = np.zeros((len(pods), self.num_slots, self.num_cores))
        for i in pods:
            for j in pods:
                if (j != i) and ((i, j) in traffic_pairs):
                    if np.sum(bin_pair_core_out[i, j, n].x for n in cores) == 1:
#                        print('successfully allocate (%s, %s)' % (i, j))
                        a = int(bin_pair_begin[i, j].x)
                        b = a + int(traffic_capacities[i, j])
                        c = int(sum(bin_pair_core_out[i, j, n].x * n
                            for n in cores))
                        u[i, a:b, c] += 1
        self.validate_arch2 = u
        self.feasible_arch2 = np.max(u.flatten()) <= 1
        
        self.sol2 = {}
        self.sol2['spectrum_begin'] = bin_pair_begin
        self.sol2['core_begin_out'] = bin_pair_core_out
        self.sol2['core_begin_in'] = bin_pair_core_in
        self.sol2['spectrum_order'] = bin_pair_order
        
        

if __name__=='__main__':
    traffic_matrix = \
    pd.read_excel('traffic_panel_pods_50_max_50_min_25_tmean_400_tvar_400.xls',
                  sheetname=2)
    traffic_matrix = traffic_matrix.as_matrix()
    m = ModelSDM_arch2(traffic_matrix, num_slots=20, num_cores=10)
    m.create_model2(mipfocus=1, timelimit=1000)