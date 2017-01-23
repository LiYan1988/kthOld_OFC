# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 17:31:59 2016

@author: li

Modelling for architecture 2
"""

from gurobipy import *
import numpy as np
import time
import itertools
import csv

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
    np.random.seed(2010)
    num_cores=3
    num_slots=160
    tm = []
    with open('simu1_matrix_2.csv') as f:
        reader = csv.reader(f)
        i = 0
        for idx, row in enumerate(reader):
            if idx>11:
                row.pop()
                row = [int(u) for u in row]
                tm.append(row)
    tm = np.array(tm)*25
    m = ModelSDM_arch2(tm, num_slots=num_slots, num_cores=num_cores)
    m.create_model2(mipfocus=1, timelimit=72000)