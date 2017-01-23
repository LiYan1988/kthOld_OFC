# -*- coding: utf-8 -*-
"""
Created on Tue May 31 15:53:44 2016

@author: li
"""

from gurobipy import *
import numpy as np
import time
import itertools
from sdm1 import Traffic

class Arch2_decompose(object):
    """Create models for different SDM DCN architectures
    """
    def __init__(self, traffic_matrix, num_slots=320, num_cores=10,
                 slot_capacity =25, num_guard_slot=1, alpha=1, beta=0):
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
        # weight factor
        self.alpha = alpha
        self.beta = beta
        
    def create_model_routing(self, **kwargs):
        """ILP
        """
        c_max = self.num_slots * self.slot_capacity
        self.tm = self.traffic_matrix.copy()
        # number of blocked demands at the begining
        self.num_blocked2 = sum(self.tm.flatten()>c_max)
        # remove those demands with too large capacities
        self.tm[self.tm>c_max] = 0
        
        # Model data
        # set of pods, pod_0, ..., pod_(N_p-1)
        pods = list(range(self.num_pods))
        # pairs of traffic demands
        traffic_pairs = tuplelist([(i, j) for i in pods for j in pods
                            if self.tm[i, j]>0])
        # traffic capacities
        traffic_capacities = {}
        for u in traffic_pairs:
            if self.tm[u[0],u[1]] > 0:
                traffic_slot = int(np.ceil(self.tm[u[0],u[1]] / 
                            self.slot_capacity) + self.num_guard_slot)
                traffic_capacities[u] = traffic_slot
#                print(traffic_slot)
                
        # set of cores
        cores = list(range(self.num_cores))
        
        # Model
        tic = time.clock()
        model = Model('Arch2_routing')
        
        # binary variable: c_i,u,k = 1 if connection u uses core k in POD i
        core_usage = {}
        for u in traffic_pairs:
            for k in cores:
                for i in u:
                    core_usage[u,i,k] = model.addVar(vtype=GRB.BINARY)
                    
        suc = {}
        for u in traffic_pairs:
            suc[u] = model.addVar(vtype=GRB.BINARY, obj=-(self.alpha+self.beta*self.tm[u[0],u[1]]))

        model.update()
        
        # one connection uses one core
        for u in traffic_pairs:
            model.addConstr(quicksum(core_usage[u,u[0],k] for k in cores)==suc[u])
            model.addConstr(quicksum(core_usage[u,u[1],k] for k in cores)==suc[u])
            
        # flow per core
        for i in pods:
            tmp = list((i, j) for (i, j) in traffic_pairs.select(i, '*'))
            tmp0 = list((j, i) for (j, i) in traffic_pairs.select('*', i))
            tmp.extend(tmp0)
            for k in cores:
                model.addConstr(quicksum(traffic_capacities[u]*
                core_usage[u, i, k] for u in tmp)<=self.num_slots)

        # params
        if len(kwargs):
            for key, value in kwargs.items():
                setattr(model.params, key, value)
        
        model.optimize()
        toc = time.clock()
        
        self.model_routing = model
        self.runtime = toc-tic
        self.pods = pods
        self.cores = cores
        self.traffic_pairs = traffic_pairs
        self.traffic_capacities = traffic_capacities
        
        pcset = {} # set of connections using pod i, core k
        for i in pods:
            for k in cores:
                pcset[i,k] = set()
        
        for u in traffic_pairs:
            for k in cores:
                for i in u:
                    if core_usage[u,i,k].x==1:
                        pcset[i,k].add(u)
        self.pcset = pcset
                
        suclist = [] # set of successfully allocated connections
        for u in self.traffic_pairs:
            if suc[u].x==1:
               suclist.append(u)
        self.suclist = suclist
        
        core_usagex = {} # core allocation
        for u in traffic_pairs:
            if u in suclist:
                for i in u:
                    for k in cores:
                        if core_usage[u,i,k].x==1:
                            core_usagex[u,i] = k
                            break
            else:
                core_usagex[u,u[0]] = -1
                core_usagex[u,u[1]] = -1
        self.core_usagex = core_usagex
        
        self.connections_ub = len(suclist)
        self.throughput_ub = sum(self.tm[u[0],u[1]] for u in self.suclist)
                    
        
        
    def create_model_sa(self, **kwargs):
        """Spectrum assignment ILP
        """

        smallM = self.num_slots
        bigM = 10*smallM
        
        # Model
        tic = time.clock()
        model_sa = Model('Arch2_sa')

        # binary variable: spectrum order
        spec_order = {}
        for i in self.pods:
            for k in self.cores:
                for c in itertools.combinations(self.pcset[i,k],2):
                    spec_order[c[0],c[1]] = model_sa.addVar(vtype=GRB.BINARY)
        
        # continuous variable: first spectrum slot index
        # binary: fail?
        spec_idx = {}
        isfail = {}
        for u in self.suclist:
            spec_idx[u] = model_sa.addVar(vtype=GRB.CONTINUOUS)
            isfail[u] = model_sa.addVar(vtype=GRB.BINARY, obj=self.alpha+self.beta*self.tm[u[0],u[1]])
            
        model_sa.update()
        
        # constraints: order
        for i in self.pods:
            for k in self.cores:
                for c in itertools.combinations(self.pcset[i,k],2):
                    model_sa.addConstr(spec_idx[c[0]]+self.traffic_capacities[c[0]]-
                    spec_idx[c[1]]+bigM*spec_order[c[0],c[1]]<=bigM)
                    model_sa.addConstr(spec_idx[c[1]]+self.traffic_capacities[c[1]]-
                    spec_idx[c[0]]+bigM*(1-spec_order[c[0],c[1]])<=bigM)
                    
        for u in self.suclist:
            model_sa.addConstr(bigM*isfail[u]>=
            spec_idx[u]+self.traffic_capacities[u]-1-smallM)

        # params
        if len(kwargs):
            for key, value in kwargs.items():
                setattr(model_sa.params, key, value)
                
        model_sa.optimize()
        toc = time.clock()
        
        self.model_sa = model_sa
        self.runtime_sa = toc-tic
        
        try:
            for u in self.suclist:
                if isfail[u].x == 1:
                    self.suclist.remove(u)
            
            self.spec_idxx = {} # spectrum slots allocation
            for u in self.traffic_pairs:
                if u in self.suclist:
                    self.spec_idxx[u] = int(spec_idx[u].x)
                else:
                    self.spec_idxx[u] = -1
                    self.core_usagex[u,u[0]] = -1
                    self.core_usagex[u,u[1]] = -1
                    
            self.connections_lb = len(self.suclist)
            self.throughput_lb = sum(self.tm[u[0],u[1]] for u in self.suclist)
        except:
            self.connections_lb = 0
            self.throughput_lb = 0
            
    def write_result_csv(self, file_name):
        with open(file_name, 'w') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow(['src', 'dst', 'spec', 'core_src', 'core_dst'])
            for u in self.suclist:
                writer.writerow([u[0], u[1], self.spec_idxx[u], self.core_usagex[u,u[0]], self.core_usagex[u,u[1]]])
            
        
if __name__=='__main__':
    np.random.seed(2010)
    
    #%% generate traffic
    num_pods=50
    max_pod_connected=20
    min_pod_connected=10
    mean_capacity=200
    variance_capacity=100
    num_cores=3
    num_slots=60
    t = Traffic(num_pods=num_pods, max_pod_connected=max_pod_connected, 
                min_pod_connected=min_pod_connected, 
                mean_capacity=mean_capacity, 
                variance_capacity=variance_capacity)
    t.generate_traffic()
    tm = t.traffic_matrix
    
    #%% read from file
#    tm = pd.read_csv('simu1_matrix_1.csv',skiprows=12,header=None)
#    tm.dropna(axis=1, how='any', inplace=True)
#    tm = tm.as_matrix()*25

    #%% optimize    
    m = Arch2_decompose(tm, num_slots=num_slots, num_cores=num_cores, alpha=1, beta=0.01)
    m.create_model_routing(mipfocus=1,timelimit=10)
    m.create_model_sa(mipfocus=1,timelimit=20)
    