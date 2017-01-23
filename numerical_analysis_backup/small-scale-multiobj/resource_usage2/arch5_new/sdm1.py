# -*- coding: utf-8 -*-
"""
Created on Mon Apr  4 11:09:29 2016

@author: liyan

Generate random traffic matrices
"""

import numpy as np
import pandas as pd

class Traffic(object):
    
    def __init__(self, num_pods, max_pod_connected, min_pod_connected=0,
                 mean_capacity=100, variance_capacity=50, 
                 capacity_choices=np.array([1, 10, 100, 200, 400, 1000])):
        # total number of PODs
        self.num_pods = num_pods 
        # max value of PODs each POD is connected, one POD can be connected to 
        # at most num_pods-1 other PODs
        if max_pod_connected >= num_pods:
            max_pod_connected = num_pods-1
        elif max_pod_connected < 0:
            max_pod_connected = min_pod_connected
        self.max_pod_connected = max_pod_connected
        # min value of PODs connected
        if min_pod_connected < 0:
            min_pod_connected = 0
        elif min_pod_connected > max_pod_connected:
            min_pod_connected = max_pod_connected
        self.min_pod_connected = min_pod_connected
        # mean value of capacity of each connection
        self.mean_capacity = mean_capacity
        # variance of capacity
        self.variance_capacity = variance_capacity
        # choices of capacity values
        self.capacity_choices = capacity_choices
        # POD id list
        self.pod_id_list = ['pod_%d' % i for i in range(self.num_pods)]
        
    def generate_traffic(self):
        """Generate random traffic matrix
        """
        # each POD is connected to x_i other PODs, where
        self.pod_connectivity = np.random.randint(self.min_pod_connected, 
                                                  self.max_pod_connected+1, 
                                                self.num_pods)
        self.traffic_matrix = np.zeros((self.num_pods, self.num_pods))
        for i in range(self.num_pods):
            # POD i cannot connect to itself
            pod_choice = np.delete(np.arange(self.num_pods), i)
            connected_pods = np.random.choice(pod_choice, 
                                              self.pod_connectivity[i], 
                                             replace=False)
            connected_capacities = np.random.normal(self.mean_capacity,
                                                    self.variance_capacity,
                                                    self.pod_connectivity[i])
            self.convert_capacity(connected_capacities)
            self.traffic_matrix[i, connected_pods] = connected_capacities

    def convert_capacity(self, connected_capacities):
        """Convert continuous normal distributed variables to capacities within
        the capacity choices
        """
        for n, i in enumerate(connected_capacities):
            w = np.divide(i, self.capacity_choices)
            connected_capacities[n] = self.capacity_choices[np.argmax(w<1)]
            
if __name__=='__main__':
    np.random.seed(2016)
    # generate a list of traffic matrices
    traffic_dict = {}
#    traffic_list = []
    num_pods=100 
    max_pod_connected=20
    min_pod_connected=1
    mean_capacity=200
    variance_capacity=200
    for i in range(20):
        t = Traffic(num_pods=num_pods, max_pod_connected=max_pod_connected, 
                    min_pod_connected=min_pod_connected, 
                    mean_capacity=mean_capacity, 
                    variance_capacity=variance_capacity,
                    capacity_choices=np.arange(10,1100,10))
        t.generate_traffic()
        df = pd.DataFrame(t.traffic_matrix)
        df.to_csv('traffic_matrix.csv', header=False, index_label=False, 
                  index=False)
