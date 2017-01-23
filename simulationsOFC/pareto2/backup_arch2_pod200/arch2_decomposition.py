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
        
        self.pods = pods
        self.traffic_pairs = traffic_pairs
        self.traffic_capacities = traffic_capacities
        self.cores = cores
        
    def create_model_routing(self, **kwargs):
        """ILP
        """
        # Model
        tic = time.clock()
        model = Model('Arch2_routing')
        
        # binary variable: c_i,u,k = 1 if connection u uses core k in POD i
        core_usage = {}
        for u in self.traffic_pairs:
            for k in self.cores:
                for i in u:
                    core_usage[u,i,k] = model.addVar(vtype=GRB.BINARY)
                    
        suc = {}
        for u in self.traffic_pairs:
            suc[u] = model.addVar(vtype=GRB.BINARY, obj=-(self.alpha+self.beta*self.tm[u[0],u[1]]))

        model.update()
        
        # one connection uses one core
        for u in self.traffic_pairs:
            model.addConstr(quicksum(core_usage[u,u[0],k] for k in self.cores)==suc[u])
            model.addConstr(quicksum(core_usage[u,u[1],k] for k in self.cores)==suc[u])
            
        # flow per core
        for i in self.pods:
            tmp = list((i, j) for (i, j) in self.traffic_pairs.select(i, '*'))
            tmp0 = list((j, i) for (j, i) in self.traffic_pairs.select('*', i))
            tmp.extend(tmp0)
            for k in self.cores:
                model.addConstr(quicksum(self.traffic_capacities[u]*
                core_usage[u, i, k] for u in tmp)<=self.num_slots)

        # params
        if len(kwargs):
            for key, value in kwargs.items():
                setattr(model.params, key, value)
        
        model.optimize()
        toc = time.clock()
        
        self.model_routing = model
        self.runtime = toc-tic
        
        pcset = {} # set of connections using pod i, core k
        for i in self.pods:
            for k in self.cores:
                pcset[i,k] = set()
        
        for u in self.traffic_pairs:
            for k in self.cores:
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
        for u in self.traffic_pairs:
            if u in suclist:
                for i in u:
                    for k in self.cores:
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
                
    def create_model_partition(self, K, **kwargs):
        """Partition traffic matrix into K sub matrices
        """
        self.num_groups = K
        self.pod_per_group = int(round(self.num_pods/K))
        self.pods_grouped = []
        self.pods_not_grouped = list(self.pods)

        # iteratively create groups
        for i in range(K-1):
            self.create_model_one_partition(self.pod_per_group, **kwargs)
        self.pods_grouped.append(self.pods_not_grouped)
        
        self.cnk_in_group = {}
        for k in range(K):
            self.cnk_in_group[k] = set()
            for i in self.pods_grouped[k]:
                for j in self.pods_grouped[k]:
                    if self.tm[i,j]>0:
                        self.cnk_in_group[k].add((i,j))
            
    def create_model_one_partition(self, G, **kwargs):
        """Find G PODs output the remaining PODs that give max throughput
        """
        
        model = Model('Partition')
        
        # binary variables: x_i = 1 if POD i is groupped 
        x = {}
        for i in self.pods_not_grouped:
            x[i] = model.addVar(vtype=GRB.BINARY)
            
        # auxiliary variable: w_ij = x_i*x_j
        xprod = {}
        for i in self.pods_not_grouped:
            for j in self.pods_not_grouped:
                xprod[i,j] = model.addVar(vtype=GRB.BINARY)
            
        model.update()
            
        # constraint: maximium K PODs in one group
        model.addConstr(quicksum(x[i] for i in self.pods_not_grouped)==G)
        for i in self.pods_not_grouped:
            for j in self.pods_not_grouped:
                model.addConstr(xprod[i,j]<=x[i])
                model.addConstr(xprod[i,j]<=x[j])
                model.addConstr(xprod[i,j]>=x[i]+x[j]-1)
            model.addConstr(quicksum(xprod[i,j] for j in self.pods_not_grouped)
            ==G*x[i])
            model.addConstr(quicksum(xprod[j,i] for j in self.pods_not_grouped)
            ==G*x[i])
            model.addConstr(xprod[i,i]==x[i])
            
        # objective
        obj = 0
        for i in self.pods_not_grouped:
            for j in self.pods_not_grouped:
                obj = obj + (self.alpha*int(self.tm[i,j]>0)
                +self.beta*self.tm[i,j])*xprod[i,j]
        model.setObjective(obj, GRB.MAXIMIZE)
        
        model.update()
        
        # params
        if len(kwargs):
            for key, value in kwargs.items():
                setattr(model.params, key, value)
        
        model.optimize()
            
        new_group = []
        remain_group = list(self.pods_not_grouped)
        for i in self.pods_not_grouped:
#            print x[i].x
            if x[i].x>=0.5:
                new_group.append(i)
                remain_group.remove(i)
                
        self.pods_grouped.append(new_group)
        self.pods_not_grouped = remain_group
        
    def create_model_group(self, flow_limit, **kwargs):
        """Optimize resource allocation within groups
        kwargs has two parts: param_r is for routing, param_s is for SA
        """
        # resources allocated to traffic demands, suc, spec, core_out, core_in
        self.cnk_resource = {u:[-1,-1,-1,-1] for u in self.traffic_pairs}
        self.cnk_group_suc = []
        self.cnk_group_fail = []
        self.obj_ = 0
        self.obj_connections_ = 0
        self.obj_throughput_ = 0
        self.flow_per_core_ = {}
        for i in self.pods:
            for j in self.cores:
                self.flow_per_core_[i,j] = 0
        for k, subgroup in enumerate(self.pods_grouped):
            self.create_model_subgroup_diag(k, flow_limit, **kwargs)
            
    def create_model_subgroup_diag(self, k, flow_limit, **kwargs):
        """Optimize in a subgroup
        """
        
        subgroup_cnk = self.cnk_in_group[k]
        subgroup = self.pods_grouped[k]
                         
        # Routing part
        model_r = Model("Routing_subgroup")
        
        # binary v
        core_usage = {}
        for u in subgroup_cnk:
            for k in self.cores:
                for i in u:
                    core_usage[u,i,k] = model_r.addVar(vtype=GRB.BINARY)
                    
        suc = {}
        for u in subgroup_cnk:
            suc[u] = model_r.addVar(vtype=GRB.BINARY, obj=-(self.alpha+self.beta*self.tm[u[0],u[1]]))
            
        flowmax = model_r.addVar(vtype=GRB.CONTINUOUS, obj=0.1)
            
        model_r.update()
        
        # one connection uses one core
        for u in subgroup_cnk:
            model_r.addConstr(quicksum(core_usage[u,u[0],k] for k in self.cores)==suc[u])
            model_r.addConstr(quicksum(core_usage[u,u[1],k] for k in self.cores)==suc[u])
            
        # flow per core
        for i in subgroup:
            tmp = list((i, j) for (i, j) in self.traffic_pairs.select(i, '*') if (i,j) in subgroup_cnk)
            tmp0 = list((j, i) for (j, i) in self.traffic_pairs.select('*', i) if (j,i) in subgroup_cnk)
            tmp.extend(tmp0)
            for k in self.cores:
                model_r.addConstr(quicksum(self.traffic_capacities[u]*
                core_usage[u, i, k] for u in tmp)<=flow_limit)
                model_r.addConstr(quicksum(self.traffic_capacities[u]*
                core_usage[u, i, k] for u in tmp)<=flowmax)
                
        # params
        if len(kwargs):
            for key, value in kwargs.items():
                tmp = key.split('_')
                if tmp[1]=='r':
                    setattr(model_r.params, tmp[0], value)
        
        model_r.update()
        model_r.optimize()
        
        pcset = {} # set of connections using pod i, core k
        for i in subgroup:
            for k in self.cores:
                pcset[i,k] = set()                
        for u in subgroup_cnk:
            for k in self.cores:
                for i in u:
                    if core_usage[u,i,k].x==1:
                        pcset[i,k].add(u)
                        
        suclist = [] # list of successfully allocated connections
        for u in subgroup_cnk:
            if suc[u].x==1:
                suclist.append(u)
                
        # SA part
        smallM = flow_limit
        bigM = 10*smallM
        
        model_s = Model('SA_subgroup')
        
        # spectrum order
        spec_order = {}
        for i in subgroup:
            for k in self.cores:
                for c in itertools.combinations(pcset[i,k],2):
                    spec_order[c[0],c[1]] = model_s.addVar(vtype=GRB.BINARY)
                    
        # first spectrum slot index
        spec_idx = {}
        isfail = {}
        for u in subgroup_cnk:
            spec_idx[u] = model_s.addVar(vtype=GRB.CONTINUOUS, obj=1)
            isfail[u] = model_s.addVar(vtype=GRB.BINARY, obj=self.alpha+self.beta*self.tm[u[0],u[1]])
            
        model_s.update()
        
        # ordering constraint
        for i in subgroup:
            for k in self.cores:
                for c in itertools.combinations(pcset[i,k],2):
                    model_s.addConstr(spec_idx[c[0]]+self.traffic_capacities[c[0]]-
                    spec_idx[c[1]]+bigM*spec_order[c[0],c[1]]<=bigM)
                    model_s.addConstr(spec_idx[c[1]]+self.traffic_capacities[c[1]]-
                    spec_idx[c[0]]+bigM*(1-spec_order[c[0],c[1]])<=bigM)
                    
        for u in suclist:
            model_s.addConstr(bigM*isfail[u]>=
            spec_idx[u]+self.traffic_capacities[u]-1-smallM)
            
        # params
        if len(kwargs):
            for key, value in kwargs.items():
                tmp = key.split('_')
                if tmp[1]=='s':
                    setattr(model_s.params, tmp[0], value)
                    
        model_s.update()
        model_s.optimize()
        
        for u in suclist:
            if isfail[u].x==1:
                suclist.remove(u)
                self.cnk_group_fail.append(u)
            else:
                self.cnk_resource[u][0] = 1
                self.cnk_resource[u][1] = int(spec_idx[u].x)
                self.cnk_resource[u][2] = int(sum(core_usage[u,u[0],k].x*k for k in self.cores))
                self.cnk_resource[u][3] = int(sum(core_usage[u,u[1],k].x*k for k in self.cores))
                self.cnk_group_suc.append(u)
                self.obj_ += self.alpha+self.beta*self.tm[u[0],u[1]]
                self.obj_connections_ += 1
                self.obj_throughput_ += self.tm[u[0],u[1]]
                self.flow_per_core_[u[0],self.cnk_resource[u][2]] = \
                max(self.cnk_resource[u][1], self.flow_per_core_[u[0],self.cnk_resource[u][2]])
                self.flow_per_core_[u[1],self.cnk_resource[u][3]] = \
                max(self.cnk_resource[u][1], self.flow_per_core_[u[1],self.cnk_resource[u][3]])
        
        
if __name__=='__main__':
    np.random.seed(2010)
    
    #%% generate traffic
    num_pods=50
    max_pod_connected=20
    min_pod_connected=10
    mean_capacity=200
    variance_capacity=100
    num_cores=3
    num_slots=80
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
#    m.create_model_routing(mipfocus=1,timelimit=10)
#    m.create_model_sa(mipfocus=1,timelimit=200)
    m.create_model_partition(5, mipfocus=1, timelimit=30)
    m.create_model_group(80, mipfocus_r=1, timelimit_r=10, mipfocus_s=1,timelimit_s=30)