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
import copy

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
                pcset[i,k] = []
        
        for u in self.traffic_pairs:
            for k in self.cores:
                for i in u:
                    if core_usage[u,i,k].x==1:
                        pcset[i,k].append(u)
        self.pcset_dc = pcset
                
        suclist = [] # set of successfully allocated connections
        for u in self.traffic_pairs:
            if suc[u].x==1:
               suclist.append(u)
        self.suclist_dc = suclist
        
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
        self.throughput_ub = sum(self.tm[u[0],u[1]] for u in self.suclist_dc)
        
    def create_model_routing_group(self, num_group, **kwargs):
        """Allocate routing by pod groups
        """
        # partition pods into groups
        self.create_model_partition_heuristic(num_group, 1)
        
        # create groups of PODs, in group connections and cross group connections
        pod_group = {i:self.pods_grouped[i] for i in range(num_group)} # group of pods
        cnk_group = {i:self.cnk_in_group[i] for i in range(num_group)} # group of connections within groups
        cnk_cross_group = {}
        for i in range(num_group):
            for j in range(0, i):
                cnk_cross_group[i,j] = []
                for u in pod_group[i]:
                    for v in pod_group[j]:
                        if self.tm[u,v]>0:
                            cnk_cross_group[i,j].append((u,v))
                        if self.tm[v,u]>0:
                            cnk_cross_group[i,j].append((v,u))
                            
        # create variables holding optimization results
        self.pcset_dc = {} # connections in (pod i, core k)
        for i in self.pods:
            for k in self.cores:
                self.pcset_dc[i,k] = []
                
        self.suclist_dc = [] # successfully allocated connections

        self.core_usagex = {} # core usage for each connection allocated
        
        self.flow_on_core = {(i,k):0 for i in self.pods for k in self.cores} # the flow on each core
        
        
        
        # optimize
        for i, tmp in pod_group.items():
            self.create_model_routing_subgroup(tmp, tmp, cnk_group[i], **kwargs)
#            
        for (i,j), tmp in cnk_cross_group.items():
            self.create_model_routing_subgroup(pod_group[i], pod_group[j], tmp, **kwargs)
            
        self.connections_ub = len(self.suclist_dc)
        self.throughput_ub = sum(self.tm[i,j] for (i,j) in self.suclist_dc) 
                            
    def create_model_routing_subgroup(self, pod_group1, pod_group2, cnk_group, **kwargs):
        """Optimize routing subproblem for grouped PODs and connections
        """
        cnk_group = tuplelist(cnk_group)
        if pod_group1==pod_group2:
            pod_group = pod_group1
        else:
            pod_group = list(pod_group1)
            pod_group.extend(pod_group2)
        
        # modeling
        model = Model('routing_model')
        # creating variables, the same for both cases
        core_usage = {}
        for u in cnk_group:
            for k in self.cores:
                core_usage[u,u[0],k] = model.addVar(vtype=GRB.BINARY)
                core_usage[u,u[1],k] = model.addVar(vtype=GRB.BINARY)
        
        suc = {}
        for u in cnk_group:
            suc[u] = model.addVar(vtype=GRB.BINARY, obj=-(self.alpha+self.beta*self.tm[u[0],u[1]]))
            
        flow_max = {}
        for i in pod_group:
            for k in self.cores:
                flow_max[i,k] = model.addVar(vtype=GRB.CONTINUOUS, obj=1e-4)
        
        model.update()
        
        # creating constraints        
        for u in cnk_group:
            model.addConstr(quicksum(core_usage[u,u[0],k] for k in self.cores)==suc[u])
            model.addConstr(quicksum(core_usage[u,u[1],k] for k in self.cores)==suc[u])
            
        for i in pod_group:
            tmp = list((i, j) for (i, j) in cnk_group.select(i, '*'))
            tmp0 = list((j, i) for (j, i) in cnk_group.select('*', i))
            tmp.extend(tmp0)
            for k in self.cores:
                model.addConstr(quicksum(self.traffic_capacities[u]*
                core_usage[u, i, k] for u in tmp)+self.flow_on_core[i,k]<=flow_max[i,k])
                model.addConstr(flow_max[i,k]<=self.num_slots)            
            
        if len(kwargs):
            for key, value in kwargs.items():
                setattr(model.params, key, value)
                    
        model.optimize()
        
        for u in cnk_group:
            for k in self.cores:
                if core_usage[u,u[0],k].x>0.9:
                    self.pcset_dc[u[0],k].append(u)
                if core_usage[u,u[1],k].x>0.9:
                    self.pcset_dc[u[1],k].append(u)
                        
        for u in cnk_group:
            if suc[u].x>0.9:
                self.suclist_dc.append(u)
                
        for u in cnk_group:
            if u in self.suclist_dc:
                self.core_usagex[u,u[0]] = int(round(sum(core_usage[u,u[0],k].x*k for k in self.cores)))
                self.core_usagex[u,u[1]] = int(round(sum(core_usage[u,u[1],k].x*k for k in self.cores)))
        
        for i in pod_group:
            for k in self.cores:
                self.flow_on_core[i,k] = round(flow_max[i,k].x)
                
                
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
                for c in itertools.combinations(self.pcset_dc[i,k],2):
                    spec_order[c[0],c[1]] = model_sa.addVar(vtype=GRB.BINARY)
        
        # continuous variable: first spectrum slot index
        # binary: fail?
        spec_idx = {}
        isfail = {}
        for u in self.suclist_dc:
            spec_idx[u] = model_sa.addVar(vtype=GRB.CONTINUOUS)
            isfail[u] = model_sa.addVar(vtype=GRB.BINARY, obj=self.alpha+self.beta*self.tm[u[0],u[1]])
            
        model_sa.update()
        
        # constraints: order
        for i in self.pods:
            for k in self.cores:
                for c in itertools.combinations(self.pcset_dc[i,k],2):
                    model_sa.addConstr(spec_idx[c[0]]+self.traffic_capacities[c[0]]-
                    spec_idx[c[1]]+bigM*spec_order[c[0],c[1]]<=bigM)
                    model_sa.addConstr(spec_idx[c[1]]+self.traffic_capacities[c[1]]-
                    spec_idx[c[0]]+bigM*(1-spec_order[c[0],c[1]])<=bigM)
                    
        for u in self.suclist_dc:
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
            for u in self.suclist_dc:
                if isfail[u].x == 1:
                    self.suclist_dc.remove(u)
            
            self.spec_idxx = {} # spectrum slots allocation
            for u in self.traffic_pairs:
                if u in self.suclist_dc:
                    self.spec_idxx[u] = int(spec_idx[u].x)
                else:
                    self.spec_idxx[u] = -1
                    self.core_usagex[u,u[0]] = -1
                    self.core_usagex[u,u[1]] = -1
                    
            self.connections_lb = len(self.suclist_dc)
            self.throughput_lb = sum(self.tm[u[0],u[1]] for u in self.suclist_dc)
        except:
            self.connections_lb = 0
            self.throughput_lb = 0
            
    def write_result_csv(self, file_name):
        with open(file_name, 'w') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow(['src', 'dst', 'spec', 'core_src', 'core_dst'])
            for u in self.suclist_dc:
                writer.writerow([u[0], u[1], self.spec_idxx[u], self.core_usagex[u,u[0]], self.core_usagex[u,u[1]]])
                
    def create_model_partition(self, K, **kwargs):
        """Partition traffic matrix into K sub matrices according to routing 
        decomposition
        """
        self.num_groups = K
        self.pod_per_group = int(round(self.num_pods/K))
        self.pods_grouped = []
        self.pods_not_grouped = list(self.pods)

        # iteratively create groups
        for i in range(K-1):
            self.create_model_one_partition(self.pod_per_group, self.suclist_dc, **kwargs)
        self.pods_grouped.append(self.pods_not_grouped)
        
        self.cnk_in_group = {}
        for k in range(K):
            self.cnk_in_group[k] = list()
            for i in self.pods_grouped[k]:
                for j in self.pods_grouped[k]:
                    if self.tm[i,j]>0:
                        self.cnk_in_group[k].append((i,j))
                        
    def create_model_partition_heuristic(self, K, Ksub=2, **kwargs):
        """Simple heuristic to partition traffic matrix
        1. divide pods into groups, each with Ksub pods
        2. use optimization to find submatrices in the Ksub pods in each group
        K: number of submatrices
        Ksub: number of submatrices that uses optimization to partition
        """
        self.cnk_obj = {i:0 for i in self.pods}        
        for i in self.pods:
            for (i,j) in self.traffic_pairs.select(i, '*'):
                self.cnk_obj[i] += self.alpha+self.tm[(i,j)]*self.beta
            for (j,i) in self.traffic_pairs.select('*', i):
                self.cnk_obj[i] += self.alpha+self.tm[(i,j)]*self.beta
        self.cnk_obj = sorted(self.cnk_obj.iteritems(), key=lambda (x,y):y, reverse=True)
        pods_out_bg = [self.cnk_obj[i][0] for i in range(self.num_pods)]
        pods_out_bg.reverse()
        
        # number of bigger groups
        self.num_groups = K
        self.pod_per_group = int(round(self.num_pods/K))
        self.pods_grouped = []
        self.pods_not_grouped = list(self.pods)
        
        self.num_bg = int(np.ceil(float(self.num_groups)/Ksub)) # number of bigger groups
        self.pods_in_bg = {} # list of bigger groups
    
        if hasattr(self, 'suclist_dc'):
            availcnk = tuplelist(self.suclist_dc)
        else:
            availcnk = tuplelist(self.traffic_pairs)
            
        for k in range(self.num_bg-1):
            self.pods_in_bg[k] = []
            self.pods_in_bg[k].append(pods_out_bg.pop())
            for i in range(Ksub*self.pod_per_group-1):
                self.find_max_cnk(self.pods_in_bg[k], pods_out_bg, availcnk)
        self.pods_in_bg[self.num_bg-1] = list(pods_out_bg)
        
        # optimize groups if Ksub>1, 
        if Ksub==1:
            # each bigger group is a group
            for i,x in self.pods_in_bg.items():
                self.pods_grouped.append(x)
        if Ksub>1:
            # optimize within every bigger group
            for k in range(self.num_bg-1):
                availcnk_tmp = [(i,j) for i in self.pods_in_bg[k] 
                                for j in self.pods_in_bg[k] 
                                if (i,j) in availcnk]
                self.pods_not_grouped = list(self.pods_in_bg[k])
                for r in range(Ksub-1):
                    self.create_model_one_partition(self.pod_per_group, availcnk_tmp, **kwargs)
                self.pods_grouped.append(self.pods_not_grouped)
            # the last bigger group, optimize only when needed
            if len(self.pods_grouped)<self.num_groups-1:
                while (len(self.pods_grouped)<self.num_groups-1):
                    availcnk_tmp = [(i,j) for i in self.pods_in_bg[self.num_bg-1]
                                    for j in self.pods_in_bg[self.num_bg-1]
                                    if (i,j) in availcnk]
                    self.pods_not_grouped = list(self.pods_in_bg[self.num_bg-1])
                    self.create_model_one_partition(self.pod_per_group, availcnk_tmp, **kwargs)
                self.pods_grouped.append(self.pods_not_grouped)
            else:
                self.pods_grouped.append(self.pods_in_bg[self.num_bg-1])
        
        self.cnk_in_group = {} # connections in one pod group
        for k in range(K):
            self.cnk_in_group[k] = list()
            for i in self.pods_grouped[k]:
                for j in self.pods_grouped[k]:
                    if self.tm[i,j]>0:
                        self.cnk_in_group[k].append((i,j))
        
    def find_max_cnk(self, pods_in_group, pods_out_group, availcnk):
        """
        Called by create_model_partition_heuristic
        Find the pods not in group which has the highest added object value,
        and add it to the group
        """
        obj_out_group = {} # add object values for pods not in group
        for i in pods_out_group:
            obj_out_group[i] = 0
            for (i,j) in availcnk.select(i, '*'):
                if j in pods_in_group:
                    obj_out_group[i] += self.alpha+self.beta*self.tm[(i,j)]
            for (j,i) in availcnk.select('*', i):
                if j in pods_in_group:
                    obj_out_group[i] += self.alpha+self.beta*self.tm[(i,j)]
        argmax = max(obj_out_group.iteritems(), key=lambda x:x[1])
        pods_out_group.remove(argmax[0])
        pods_in_group.append(argmax[0])
            
    def create_model_one_partition(self, G, availcnk, **kwargs):
        """Find G PODs output the remaining PODs that give max throughput
        """
        
        cnklist = tuplelist([(i,j) for i in self.pods_not_grouped
                                for j in self.pods_not_grouped
                                if (i,j) in availcnk])
        
        model = Model('Partition')
        
        # binary variables: x_i = 1 if POD i is groupped 
        x = {}
        for i in self.pods_not_grouped:
            x[i] = model.addVar(vtype=GRB.BINARY)
            
        # auxiliary variable: w_ij = x_i*x_j
        xprod = {}
        for (i,j) in cnklist:
            xprod[i,j] = model.addVar(vtype=GRB.BINARY)
            
        model.update()
            
        # constraint: maximium K PODs in one group
        model.addConstr(quicksum(x[i] for i in self.pods_not_grouped)==G)

        for (i,j) in cnklist:
            model.addConstr(xprod[i,j]<=x[i])
            model.addConstr(xprod[i,j]<=x[j])
            model.addConstr(xprod[i,j]>=x[i]+x[j]-1)
            
        for i in self.pods_not_grouped:
            model.addConstr(quicksum(xprod[i,j] 
            for (i,j) in cnklist.select(i, '*'))<=G*x[i])
            model.addConstr(quicksum(xprod[j,i] 
            for (j,i) in cnklist.select('*', i))<=G*x[i])
            
        # objective
        obj = 0
        for (i,j) in cnklist:
            obj += (self.alpha+self.beta*self.tm[i,j])*xprod[i,j]
                    
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
        
    def create_model_group(self, flow_limit, sa_flag, **kwargs):
        """Optimize resource allocation within groups
        kwargs has two parts: param_r is for routing, param_s is for SA
        Routing and SA subproblems are solved for each group
        sa_flag: 1 if first solve routing subproblem in create_model_routing
                 0 if solve routing for each subgroup
        """
        # resources allocated to traffic demands, suc, spec, core_out, core_in
        self.cnk_resource = {u:[-1,-1,-1,-1] for u in self.traffic_pairs}
        self.cnk_group_suc = []
        self.cnk_group_fail = []
        self.obj_ = 0
        self.obj_connections_ = 0
        self.obj_throughput_ = 0
        self.flow_per_core_ = {}
        self.resource_tensor = np.ones((self.num_pods, self.num_cores, self.num_slots), dtype=bool)
        
        for i in self.pods:
            for j in self.cores:
                self.flow_per_core_[i,j] = 0
                 
        for k, subgroup in enumerate(self.pods_grouped):
            subgroup_cnk = [u for u in self.cnk_in_group[k] if u in self.suclist_dc]
            if not sa_flag:
                self.create_model_subgroup_diag(flow_limit, subgroup_cnk, subgroup, **kwargs)
            elif sa_flag:
                self.create_model_subgroup_diag_sa(flow_limit, subgroup_cnk, subgroup, **kwargs)
        
        self.fill_holes(self.suclist_dc, 1)
            
    def create_model_subgroup_diag(self, flow_limit, subgroup_cnk, subgroup, **kwargs):
        """Optimize in a subgroup, first routing then sa
        """
                         
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
            
        flowmax = {}
        for i in subgroup:
            for k in self.cores:
                flowmax[i,k] = model_r.addVar(vtype=GRB.CONTINUOUS, obj=1.0e-4)
            
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
                core_usage[u, i, k] for u in tmp)<=flowmax[i,k])
                
        # params
        if len(kwargs):
            for key, value in kwargs.items():
                tmp = key.split('_')
                if tmp[1]=='r':
                    setattr(model_r.params, tmp[0], value)
        
        model_r.update()
        model_r.optimize()
        
        gpcset_ = {} # set of successful connections using pod i, core k
        for i in subgroup:
            for k in self.cores:
                gpcset_[i,k] = []                
        for u in subgroup_cnk:
            for k in self.cores:
                for i in u:
                    if core_usage[u,i,k].x==1 and suc[u].x==1:
                        gpcset_[i,k].append(u)
                        
        gsuclist_ = [] # list of successfully allocated connections
        for u in subgroup_cnk:
            if suc[u].x==1:
                gsuclist_.append(u)
                
        # SA part
        smallM = flow_limit
        bigM = 10*smallM
        
        model_s = Model('SA_subgroup')
        
        # spectrum order
        spec_order = {}
        for i in subgroup:
            for k in self.cores:
                for c in itertools.combinations(gpcset_[i,k],2):
                    spec_order[c[0],c[1]] = model_s.addVar(vtype=GRB.BINARY)
                    
        # first spectrum slot index
        spec_idx = {}
        isfail = {}
        for u in gsuclist_:
            spec_idx[u] = model_s.addVar(vtype=GRB.CONTINUOUS, lb=0)
            isfail[u] = model_s.addVar(vtype=GRB.BINARY, 
                            obj=self.alpha+self.beta*self.tm[u[0],u[1]])
            
        # spectrum usage on each core
        spec_max = {}
        for i in subgroup:
            for k in self.cores:
                spec_max[i,k] = model_s.addVar(vtype=GRB.CONTINUOUS, obj=1e-4)
            
        model_s.update()
        
        # ordering constraint
        for i in subgroup:
            for k in self.cores:
                for c in itertools.combinations(gpcset_[i,k],2):
                    model_s.addConstr(spec_idx[c[0]]+self.traffic_capacities[c[0]]-
                    spec_idx[c[1]]+bigM*spec_order[c[0],c[1]]<=bigM)
                    model_s.addConstr(spec_idx[c[1]]+self.traffic_capacities[c[1]]-
                    spec_idx[c[0]]+bigM*(1-spec_order[c[0],c[1]])<=bigM)
                for u in gpcset_[i,k]:
                    model_s.addConstr(spec_max[i,k]>=spec_idx[u]+self.traffic_capacities[u]-1)
                    
        for u in gsuclist_:
            model_s.addConstr(bigM*isfail[u]>=
#            spec_idx[u]+self.traffic_capacities[u]-1-smallM)
            spec_idx[u]+self.traffic_capacities[u]-smallM)
            
            
        # params
        if len(kwargs):
            for key, value in kwargs.items():
                tmp = key.split('_')
                if tmp[1]=='s':
                    setattr(model_s.params, tmp[0], value)
                    
        model_s.update()
        model_s.optimize()
        
        for u in gsuclist_:
            if isfail[u].x==1:
#                gsuclist_.remove(u)
                self.cnk_group_fail.append(u)
            else:
                self.cnk_resource[u][0] = 1
                self.cnk_resource[u][1] = round(spec_idx[u].x)
                self.cnk_resource[u][2] = round(sum(core_usage[u,u[0],k].x*k for k in self.cores))
                self.cnk_resource[u][3] = round(sum(core_usage[u,u[1],k].x*k for k in self.cores))
                self.cnk_group_suc.append(u)
                self.obj_ += self.alpha+self.beta*self.tm[u[0],u[1]]
                self.obj_connections_ += 1
                self.obj_throughput_ += self.tm[u[0],u[1]]
                core_out = int(self.cnk_resource[u][2])
                core_in = int(self.cnk_resource[u][3])
                specbd = int(self.traffic_capacities[u[0],u[1]]) # bandwidth
                speci = int(self.cnk_resource[u][1]) # start spectrum index
           
                # update resource matrix
                self.resource_tensor[u[0],core_out,speci:(speci+specbd)] = False
                self.resource_tensor[u[1],core_in,speci:(speci+specbd)] = False
                self.flow_per_core_[u[0],core_out] = np.where(self.resource_tensor[u[0],core_out,:]==False)[0][-1] 
                self.flow_per_core_[u[1],core_in] = np.where(self.resource_tensor[u[1],core_in,:]==False)[0][-1] 
                
    def create_model_subgroup_diag_sa(self, flow_limit, subgroup_cnk, subgroup, **kwargs):
        """Solve SA subproblem for each subgroup, the routing is solved globaly
        """
        smallM = flow_limit
        bigM = 10*smallM        
        
        model = Model('SA_subgroup')
        
        spec_order = {}
        spec_max = {}
        for i in subgroup:
            for k in self.cores:
                for c in itertools.combinations(self.pcset_dc[i,k],2):
                    if (c[0] in subgroup_cnk) and (c[1] in subgroup_cnk):
                        spec_order[c[0],c[1]] = model.addVar(vtype=GRB.BINARY)
                spec_max[i,k] = model.addVar(vtype=GRB.CONTINUOUS, obj=1e-4)
                    
        spec_idx = {}
        isfail = {}
        for u in subgroup_cnk:
            spec_idx[u] = model.addVar(vtype=GRB.CONTINUOUS, obj=0)
            isfail[u] = model.addVar(vtype=GRB.BINARY, obj=self.alpha+self.beta*self.tm[u[0],u[1]])
            
            
        model.update()
        
        for i in subgroup:
            for k in self.cores:
                for c in itertools.combinations(self.pcset_dc[i,k],2):
                    if (c[0] in subgroup_cnk) and (c[1] in subgroup_cnk):
                        model.addConstr(spec_idx[c[0]]+self.traffic_capacities[c[0]]-
                        spec_idx[c[1]]+bigM*spec_order[c[0],c[1]]<=bigM)
                        model.addConstr(spec_idx[c[1]]+self.traffic_capacities[c[1]]-
                        spec_idx[c[0]]+bigM*(1-spec_order[c[0],c[1]])<=bigM)
                for u in subgroup_cnk:
                    model.addConstr(spec_max[i,k]>=spec_idx[u]+self.traffic_capacities[u]-1)
               
        for u in subgroup_cnk:
            model.addConstr(bigM*isfail[u]>=
            spec_idx[u]+self.traffic_capacities[u]-smallM)
            
        # params
        if len(kwargs):
            for key, value in kwargs.items():
                tmp = key.split('_')
                if tmp[1]=='s':
                    setattr(model.params, tmp[0], value)
                
        model.optimize()
        
        for u in subgroup_cnk:
            if isfail[u].x==1:
                self.cnk_group_fail.append(u)
            else:
                self.cnk_resource[u][0] = 1
                self.cnk_resource[u][1] = round(spec_idx[u].x)
                self.cnk_resource[u][2] = self.core_usagex[u,u[0]]
                self.cnk_resource[u][3] = self.core_usagex[u,u[1]]
                self.cnk_group_suc.append(u)
                self.obj_ += self.alpha+self.beta*self.tm[u[0],u[1]]
                self.obj_connections_ += 1
                self.obj_throughput_ += self.tm[u[0],u[1]]
                
                core_out = int(self.cnk_resource[u][2])
                core_in = int(self.cnk_resource[u][3])
                specbd = int(self.traffic_capacities[u[0],u[1]]) # bandwidth
                speci = int(self.cnk_resource[u][1]) # start spectrum index
                
                # update resource matrix
                self.resource_tensor[u[0],core_out,speci:(speci+specbd)] = False
                self.resource_tensor[u[1],core_in,speci:(speci+specbd)] = False   
                self.flow_per_core_[u[0],core_out] = np.where(self.resource_tensor[u[0],core_out,:]==False)[0][-1] 
                self.flow_per_core_[u[1],core_in] = np.where(self.resource_tensor[u[1],core_in,:]==False)[0][-1] 
                
    def fill_holes(self, cnklist, fill_end):
        """Fill the spatial-spectral holes in the resource tensor with 
        unallocated traffic demands
        """
        tmpu = [u for u in self.suclist_dc if u not in self.cnk_group_suc]
        tmpo = [self.traffic_capacities[u] for u in tmpu]
        self.suclist_remain_ = [x for (y,x) in sorted(zip(tmpo, tmpu))]
        
        tmpcnk = list(self.suclist_remain_)
        tmpres = np.copy(self.resource_tensor)
        # allocate one by one
        for u in self.suclist_remain_:
            src = u[0]
            dst = u[1]
            tmpsrc = tmpres[src,:,:]
            tmpdst = tmpres[dst,:,:]
            tmpcmb = np.zeros((self.num_cores**2, self.num_slots))
            k = 0
            avail_slots = {}
            for ksrc in self.cores:
                for kdst in self.cores:
                    tmpcmb[k,:] = tmpsrc[ksrc,:]*tmpdst[kdst,:]
                    if not fill_end:
                        endslot = max(self.flow_per_core_[src,ksrc],self.flow_per_core_[dst,kdst])
                        tmpcmb[k,endslot:] = False
                    tmpavail = self.one_runs(tmpcmb[k,:])
                    tmpidx = np.where(tmpavail[:,1]>=self.traffic_capacities[u])[0]
                    if not tmpidx.size: # no hole
                        avail_slots[ksrc,kdst] = np.array([-1, self.num_slots+1]) # not available
                    else:
                        idxm = np.argmin(tmpavail[tmpidx,1])
                        avail_slots[ksrc,kdst] = np.array(tmpavail[tmpidx[idxm],:])
                    k = k+1
            avail_slots = list(sorted(avail_slots.iteritems(), key=lambda (x,y):y[1]))
            # avail_slots[0] has the form of ((core_out,core_in), [spec_idx,available_slots])
            if avail_slots[0][1][1]<=self.num_slots:
                core_out = avail_slots[0][0][0]
                core_in = avail_slots[0][0][1]
                speci = avail_slots[0][1][0]
                specbd = self.traffic_capacities[u]
                self.cnk_resource[u][0] = 1
                self.cnk_resource[u][1] = speci
                self.cnk_resource[u][2] = core_out
                self.cnk_resource[u][3] = core_in
                self.cnk_group_suc.append(u)
                self.obj_ += self.alpha+self.beta*self.tm[u[0],u[1]]
                self.obj_connections_ += 1
                self.obj_throughput_ += self.tm[u[0],u[1]]
                # update resource tensor
                tmpres[u[0],core_out,speci:(speci+specbd)] = False
                tmpres[u[1],core_in,speci:(speci+specbd)] = False
                self.flow_per_core_[u[0],core_out] = np.where(tmpres[u[0],core_out,:]==False)[0][-1] 
                self.flow_per_core_[u[1],core_in] = np.where(tmpres[u[1],core_in,:]==False)[0][-1] 
                
                
        self.suclist_remain_ = [u for u in self.suclist_dc if u not in self.cnk_group_suc]
        self.resource_tensor = tmpres
        
    def one_runs(self, a):
        # Create an array that is 1 where a is 0, and pad each end with an extra 0.
        isone = np.concatenate(([0], np.equal(a, 1).view(np.int8), [0]))
        absdiff = np.abs(np.diff(isone))
        # Runs start and end where absdiff is 1.
        ranges = np.where(absdiff == 1)[0].reshape(-1, 2)
        ranges[:,1] = ranges[:,1]-ranges[:,0]
        return ranges  
                
    def create_model_subgroup_offdiag_sa(self, subgroup1, subgroup2, subgroup_cnk, **kwargs):
        """cross group optimization
        Routing is from create_model_routing, can be improved
        """
        subgroup = list(subgroup1)
        subgroup.extend(subgroup2)
        
        model = Model('SA_offdiag')
        
        spec_order = {}
        spec_max = {}
        for i in subgroup:
            for k in self.cores:
                for c in itertools.combinations(self.pcset_dc[i,k],2):
                    if (c[0] in subgroup_cnk) and (c[1] in subgroup_cnk):
                        spec_order[c[0],c[1]] = model.addVar(vtype=GRB.BINARY)
                spec_max[i,k] = model.addVar(vtype=GRB.CONTINUOUS, obj=1)
                
        spec_idx = {}
        isfail = {}
        for u in subgroup_cnk:
            spec_idx[u] = model.addVar(vtype=GRB.CONTINUOUS, obj=0)
            isfail[u] = model.addVar(vtype=GRB.BINARY, obj=self.alpha+self.beta*self.tm[u[0],u[1]])
            
        model.update()
        
        smallM = self.num_slots
        bigM = 10*smallM
        for i in subgroup:
            for k in self.cores:
                for c in itertools.combinations(self.pcset_dc[i,k],2):
                    if (c[0] in subgroup_cnk) and (c[1] in subgroup_cnk):
                        model.addConstr(spec_idx[c[0]]+self.traffic_capacities[c[0]]-
                        spec_idx[c[1]]+bigM*spec_order[c[0],c[1]]<=bigM)
                        model.addConstr(spec_idx[c[1]]+self.traffic_capacities[c[1]]-
                        spec_idx[c[0]]+bigM*(1-spec_order[c[0],c[1]])<=bigM)
                for u in self.pcset_dc[i,k]:
                    if u in subgroup_cnk:
                        model.addConstr(spec_max[i,k]>=spec_idx[u]
                        +self.traffic_capacities[u]-1)
                    

        for u in subgroup_cnk:
            delta = max(self.flow_per_core_[u[0],self.core_usagex[u,u[0]]], 
                         self.flow_per_core_[u[1],self.core_usagex[u,u[1]]])
            model.addConstr(spec_idx[u]>=delta+1)
            model.addConstr(bigM*isfail[u]>=
            spec_idx[u]+self.traffic_capacities[u]-smallM)
            
        if len(kwargs):
            for key, value in kwargs.items():
                tmp = key.split('_')
                if tmp[1]=='soff':
                    setattr(model.params, tmp[0], value)
                    
        model.optimize()
        
        for u in subgroup_cnk:
            if isfail[u].x==1:
                self.cnk_group_fail.append(u)
            else:
                self.cnk_resource[u][0] = 1
                self.cnk_resource[u][1] = round(spec_idx[u].x)
                self.cnk_resource[u][2] = self.core_usagex[u,u[0]]
                self.cnk_resource[u][3] = self.core_usagex[u,u[1]]
                self.cnk_group_suc.append(u)
                self.obj_ += self.alpha+self.beta*self.tm[u[0],u[1]]
                self.obj_connections_ += 1
                self.obj_throughput_ += self.tm[u[0],u[1]]
                
                core_out = int(self.cnk_resource[u][2])
                core_in = int(self.cnk_resource[u][3])
                specbd = int(self.traffic_capacities[u[0],u[1]]) # bandwidth
                speci = int(self.cnk_resource[u][1]) # start spectrum index
                
                # update resource matrix
                self.resource_tensor[u[0],core_out,speci:(speci+specbd)] = False
                self.resource_tensor[u[1],core_in,speci:(speci+specbd)] = False
                self.flow_per_core_[u[0],core_out] = np.where(self.resource_tensor[u[0],core_out,:]==False)[0][-1] 
                self.flow_per_core_[u[1],core_in] = np.where(self.resource_tensor[u[1],core_in,:]==False)[0][-1] 
                
    def create_model_subgroup_offdiag(self, **kwargs):
        """
        """
        K = len(self.pods_grouped)
        
        for c in itertools.combinations(range(K), 2):
            tmpu = [u for u in self.suclist_dc if u not in self.cnk_group_suc]
            tmpo = [self.traffic_capacities[u] for u in tmpu]
            self.suclist_remain_ = [x for (y,x) in sorted(zip(tmpo, tmpu))]
            cnk1 = [(i,j) for i in self.pods_grouped[c[0]] for j in self.pods_grouped[c[1]] 
                if (i,j) in self.suclist_remain_]
            cnk2 = [(j,i) for i in self.pods_grouped[c[0]] for j in self.pods_grouped[c[1]] 
                if (j,i) in self.suclist_remain_]
            cnk1.extend(cnk2)
            self.create_model_subgroup_offdiag_sa(list(self.pods_grouped[c[0]]), 
                                                  list(self.pods_grouped[c[1]]), 
                                                    cnk1, **kwargs)
                                                    
        self.fill_holes(self.traffic_capacities, 1)
        
    def check(self):
        """Check feasibility of solution
        """
        # check if any two connections are overlapped
        n_overlap=0
        for (u,v) in itertools.combinations(self.cnk_group_suc,2):
            if set(u)&set(v):
                cout_u = self.cnk_resource[u][2]
                cin_u = self.cnk_resource[u][3]
                si_u = self.cnk_resource[u][1]
                sb_u = self.traffic_capacities[u]

                cout_v = self.cnk_resource[v][2]
                cin_v = self.cnk_resource[v][3]
                si_v = self.cnk_resource[v][1]
                sb_v = self.traffic_capacities[v]
                
                if set([(u[0], cout_u), (u[1], cin_u)])&set([(v[0], cout_v), (v[1], cin_v)]):
                    if (si_u>=si_v and si_v+sb_v-1>=si_u) or (si_v>=si_u and si_u+sb_u-1>=si_v):
                        print [(u[0], cout_u), (u[1], cin_u)]
                        print [(v[0], cout_v), (v[1], cin_v)]
                        print 'wrong'
                        n_overlap+=1
        
        # check if any connection is out of range 
        n_oof = 0
        for u in self.cnk_group_suc:
            si = self.cnk_resource[u][1]
            sb = self.traffic_capacities[u]
            if si+sb-1>self.num_slots:
                n_oof+=1
        return (n_overlap, n_oof)
        
    def sa_heuristic(self, ascending1=True,ascending2=True):
        """Spectrum assignment heuristi
        ascending1: order of allocating connections in suclist
        ascending2: order of allocating connections in remain list
        """
        suclist = list(self.suclist_dc)
        suclist_tm = [self.traffic_capacities[u] for u in suclist]
        if ascending1:
            suclist = [x for (y,x) in sorted(zip(suclist_tm, suclist))]
        else:
            suclist = [x for (y, x) in sorted(zip(suclist_tm, suclist), reverse=True)]
            
        IS_list = {} # independent set
        IS_list[0] = []
        cl_list = {}
        cl_list[0] = set()
        i = 0
        while len(suclist):
            tmplist = list(suclist)
            for u in tmplist:
                src = u[0]
                dst = u[1]
                src_core = self.core_usagex[u,src]
                dst_core = self.core_usagex[u,dst]
                if ((src,src_core) not in cl_list[i]) and ((dst, dst_core) not in cl_list[i]):
                    # add connection if it's independent to element in IS_list[i]
                    IS_list[i].append(u)
                    cl_list[i].add((src,src_core))
                    cl_list[i].add((dst,dst_core))
                    tmplist.remove(u)
            i += 1
            IS_list[i] = []
            cl_list[i] = set()
            suclist = tmplist
            
        del cl_list[i]
        del IS_list[i]

        self.obj_sah_ = 0
        self.obj_sah_connection_ = 0
        self.obj_sah_throughput_ = 0
        suclist = []
        restensor = np.ones((self.num_pods, self.num_cores, self.num_slots))        
        for i in range(len(IS_list)):
            for u in IS_list[i]:
                src = u[0]
                dst = u[1]
                src_core = self.core_usagex[u,src]
                dst_core = self.core_usagex[u,dst]
                tmpsrc = restensor[src,src_core,:]
                tmpdst = restensor[dst,dst_core,:]
                tmp = tmpsrc*tmpdst
                tmpavail = self.one_runs(tmp)
                tmpidx = np.where(tmpavail[:,1]>=self.traffic_capacities[u])[0]
                if tmpidx.size:
                   spec_idx = tmpavail[tmpidx[0],0]
                   restensor[src,src_core,spec_idx:(spec_idx+self.traffic_capacities[u])] = 0
                   restensor[dst,dst_core,spec_idx:(spec_idx+self.traffic_capacities[u])] = 0
                   self.obj_sah_ += self.alpha+self.beta*self.tm[src,dst]
                   self.obj_sah_connection_ += 1
                   self.obj_sah_throughput_ += self.tm[src,dst]
                   suclist.append(u)

        remain_cnk = [u for u in self.traffic_pairs if u not in suclist]
        remain_tm = [self.traffic_capacities[u] for u in remain_cnk]
        if ascending2:
            remain_cnk = [x for (y,x) in sorted(zip(remain_tm,remain_cnk))]
        else:
            remain_cnk = [x for (y,x) in sorted(zip(remain_tm,remain_cnk), reverse=False)]
            
        for u in remain_cnk:
            src = u[0]
            dst = u[1]
            tmpsrc = restensor[src,:,:]
            tmpdst = restensor[dst,:,:]
            tmpcmb = np.zeros((self.num_cores**2, self.num_slots))
            k = 0
            avail_slots = {}
            for ksrc in self.cores:
                for kdst in self.cores:
                    tmpcmb[k,:] = tmpsrc[ksrc,:]*tmpdst[kdst,:]
                    tmpavail = self.one_runs(tmpcmb[k,:])
                    tmpidx = np.where(tmpavail[:,1]>=self.traffic_capacities[u])[0]
                    if not tmpidx.size:
                        avail_slots[ksrc,kdst] = np.array([-1, self.num_slots+1])
                    else:
                        idxm = np.argmin(tmpavail[tmpidx,1])
                        avail_slots[ksrc,kdst] = np.array(tmpavail[tmpidx[idxm],:])
                    k += 1
            avail_slots = list(sorted(avail_slots.iteritems(), key=lambda (x,y):y[1]))
            # avail_slots[0] has the form of ((core_out,core_in), [spec_idx,available_slots])
            if avail_slots[0][1][1]<=self.num_slots:
                src_core = avail_slots[0][0][0]
                dst_core = avail_slots[0][0][1]
                spec_idx = avail_slots[0][1][0]
                spec_bd = self.traffic_capacities[u]
                restensor[src,src_core,spec_idx:(spec_idx+spec_bd)] = 0
                restensor[dst,dst_core,spec_idx:(spec_idx+spec_bd)] = 0
                self.obj_sah_ += self.alpha+self.beta*self.tm[src,dst]
                self.obj_sah_connection_ += 1
                self.obj_sah_throughput_ += self.tm[src,dst]
                

        
        
        
            
if __name__=='__main__':
    np.random.seed(2014)
    
    #%% generate traffic
    num_pods=100
    max_pod_connected=300
    min_pod_connected=150
    mean_capacity=200
    variance_capacity=100
    num_cores=10
    num_slots=320
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
    
    #%% test heuristic
    m.create_model_routing(mipfocus=1,timelimit=100,mipgap=0.1,method=2) # Method=2 or 3
    m.sa_heuristic(ascending=True)
#    #    m.create_model_sa(mipfocus=1,timelimit=40)
#    m.create_model_partition_heuristic(6,2,timelimit=400,mipgap=0.5) # timelimit=120 is enough
#    # submatrices    
#    sa_flag = 0
#    m.create_model_group(num_slots, sa_flag, mipfocus_r=1, timelimit_r=180, mipgap_r=0.05, 
#                         mipfocus_s=1,timelimit_s=180, mipgap_s=0.2) 
#    # routing solved instantly, sa uses 180 and stopped prematurely
#
#    m.create_model_subgroup_offdiag(mipfocus_soff=1,timelimit_soff=180,mipgap=0.01) 
#    # solved instantly
#
#    print m.obj_connections_
#    print m.obj_throughput_
#    print m.check()
    
#    m.create_model_routing_group(15, timelimit=100, mipfocus=1, mipgap=0.1)
#    print m.alpha*m.connections_ub+m.beta*m.throughput_ub
    # optimal: 154574, 2: 130496.55, 5: 129383.02, 10: 145800.58, 15: 145156.37, 

#    m.create_model_routing_group(10, timelimit=100, mipfocus=1, mipgap=0.1)
#    m.create_model_partition_heuristic(10,2,timelimit=400,mipgap=0.5) # timelimit=120 is enough
#    sa_flag=0
#    m.create_model_group(num_slots, sa_flag, mipfocus_r=1, timelimit_r=180, mipgap_r=0.05, 
#                     mipfocus_s=1,timelimit_s=300, mipgap_s=0.1) # sa should run long enough time
#    m.create_model_subgroup_offdiag(mipfocus_soff=1,timelimit_soff=180,mipgap_soff=0.01) 
#    print m.obj_connections_ / float(m.connections_ub)
#    print m.obj_throughput_ / float(m.throughput_ub)
#    print m.check()