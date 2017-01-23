# -*- coding: utf-8 -*-
"""
Created on Mon Apr  4 11:09:29 2016

@author: liyan

Generate random traffic matrices
"""

import numpy as np
#import pandas as pd

class Traffic(object):
    
    def __init__(self, num_pods, max_pod_connected, min_pod_connected=0,
                 mean_capacity=100, variance_capacity=50):
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
        self.capacity_choices = [1, 10, 100, 200, 400, 1000]
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
    num_pods=250 
    max_pod_connected=200
    min_pod_connected=100
    mean_capacity=200
    variance_capacity=600
    for i in range(10):
        t = Traffic(num_pods=num_pods, max_pod_connected=max_pod_connected, 
                    min_pod_connected=min_pod_connected, 
                    mean_capacity=mean_capacity, 
                    variance_capacity=variance_capacity)
        t.generate_traffic()
        item = 'matrix_%d' % i
        traffic_dict[item] = t.traffic_matrix
#        traffic_list.append(t)
#    pod_id_src = [i+'_src' for i in t.pod_id_list]
#    pod_id_dst = [i+'_dst' for i in t.pod_id_list]
#    traffic_panel = pd.Panel(traffic_dict, major_axis=pod_id_src, 
#                             minor_axis=pod_id_dst)
#    file_name = 'traffic_panel_pods_%d_max_%d_min_%d_tmean_%d_tvar_%d' \
#    % (num_pods, max_pod_connected, min_pod_connected, mean_capacity, variance_capacity)
#    traffic_panel.to_excel('%s.xls' % (file_name))
#    print(file_name)
#    traffic_df = pd.Series(traffic_list)