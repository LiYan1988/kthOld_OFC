# -*- coding: utf-8 -*-
"""
Created on Fri Jun  3 12:24:24 2016

@author: li
"""

from gurobipy import *
import time

class ModelSDM_arch1(object):
    """Create models for different SDM DCN architectures
    """
    def __init__(self, traffic_matrix, num_slots=320, num_cores=10,
                 slot_capacity =25, num_guard_slot=1):
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
        
        # Don't need to consider the guardband since it's fixed grid
        # max capacity per core with all spectrum slots
        c_max = self.num_slots * self.slot_capacity
        self.tm_arch = self.traffic_matrix.copy()
        # number of blocked demands at the begining
        self.num_blocked_init = sum(self.tm_arch.flatten()>c_max)
        # remove those demands with too large capacities
        self.tm_arch[self.tm_arch>c_max] = 0
        
        # Model data
        # set of pods, pod_0, ..., pod_(N_p-1)
        pods = list(range(self.num_pods))
        # pairs of traffic demands
        traffic_pairs = [(i, j) for i in pods for j in pods 
                            if self.tm_arch[i, j]>0]
        # capacities of traffic demands
        traffic_capacities = [self.tm_arch[i, j] for (i, j) in traffic_pairs]
        traffic_pairs, traffic_capacities = \
                        multidict(dict(zip(traffic_pairs, traffic_capacities)))
        traffic_pairs = tuplelist(traffic_pairs)
        # set of cores, core_0, ..., core_(N-1)
        cores = list(range(self.num_cores))
        
        self.cores = cores
        self.traffic_pairs = traffic_pairs
        self.pods = pods

        
    def create_model(self, **kwargs):
        """Create model for architecture 1,
        Uncoupled SDM & no WDM
        BLP, # variables: |T|N, |T| is the number of demands
        N is the number of cores
        """

        cores = self.cores
        traffic_pairs = self.traffic_pairs
        pods = self.pods
        
        # Model
        tic = time.clock()
        m1 = Model('model1')
        
        # create binary variables x_ijk^+ = 1 if out traffic from POD i to 
        # POD j uses core k, similar for x_ijk^-
        bin_pair_core_out = {}
        bin_pair_core_in = {}
        for i, j in traffic_pairs:
            for k in cores:
                bin_pair_core_out[i, j, k] = m1.addVar(vtype=GRB.BINARY, 
                            name='bin_pair_core_out_%s_%s_%s' % (i, j, k))
                bin_pair_core_in[i, j, k] = m1.addVar(vtype=GRB.BINARY,
                            name='bin_pair_core_in_%s_%s_%s' % (i, j, k))
        
        # create binary variables y_ij = sum(x_ijk^+/-) representing if traffic
        # demand (i, j) is successfully allocated
        bin_pair = {}
        for i, j in traffic_pairs:
            bin_pair[i, j] = m1.addVar(vtype=GRB.BINARY, obj=-1,
                            name='bin_pair_%s_%s' % (i, j))
                            
        m1.update()
        
        # create constraints: y_ij = sum(x_ijk^+) and y_ij = sum(x_ijk^-)
        # these constraints also imply that one traffic demand uses 
        # at most one core
        for i, j in traffic_pairs:
            m1.addConstr(bin_pair[i, j] == 
                        quicksum(bin_pair_core_in[i, j, k] for k in cores), 
                         name='pair_in_%s_%s' % (i, j))
            m1.addConstr(bin_pair[i, j] ==
                        quicksum(bin_pair_core_out[i, j, k] for k in cores),
                        name='pair_out_%s_%s' % (i, j))
        
        # create constraints: one core can be used by at most 
        # one traffic demand
        for k in cores:
            for u in pods:
                m1.addConstr(quicksum(bin_pair_core_out[u, j, k] 
                    for u, j in traffic_pairs.select(u, '*')) + 
                    quicksum(bin_pair_core_in[i, u, k]
                    for i, u in traffic_pairs.select('*', u)) <= 1, 
                             name='pod_%s_core_%s' % (u, k))                    
        
        # parameters
        if len(kwargs):
            for key, value in kwargs.items():
                setattr(m1.params, key, value)
        
        m1.optimize()
        toc = time.clock()
        
        self.model = m1
        self.allocated_traffic1 = -m1.objVal
        self.num_blocked1 = self.num_blocked_init + (len(traffic_pairs) - 
                                self.allocated_traffic1)
        self.block_rate1 = self.num_blocked1 / self.total_demands
        self.runtime1 = toc - tic
    
        
if __name__=='__main__':
    #%% generate traffic
    num_pods=100
    max_pod_connected=20
    min_pod_connected=20
    mean_capacity=200
    variance_capacity=100
    num_cores=3
    num_slots=160
    t = Traffic(num_pods=num_pods, max_pod_connected=max_pod_connected, 
                min_pod_connected=min_pod_connected, 
                mean_capacity=mean_capacity, 
                variance_capacity=variance_capacity)
    t.generate_traffic()
    traffic_matrix = t.traffic_matrix
    
    #%% solve
    m = ModelSDM_arch1(traffic_matrix, num_slots=num_slots, num_cores=num_cores)
#    m.create_model1(mipfocus=1, timelimit=10)
    m.create_model1(mipfocus=1, timelimit=100)
#    print('blocking prop.:', m.block_rate2)
#    m.create_model2(mipfocus=1, timelimit=15)
#    print('blocking prop.:', m.block_rate1)