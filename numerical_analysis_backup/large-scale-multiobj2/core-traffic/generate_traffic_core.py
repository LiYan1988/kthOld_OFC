import numpy as np
import pandas as pd
from sdm1 import Traffic

np.random.seed(2016)

#corev = np.array([1, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20])
#for i in range(20):
#    num_pods = 
num_pods = 250
max_pod_connected=249
min_pod_connected=0
mean_capacity=100
variance_capacity=100
s = []
for i in range(20):
    t = Traffic(num_pods=num_pods, max_pod_connected=max_pod_connected, 
                    min_pod_connected=min_pod_connected, 
                    mean_capacity=mean_capacity, 
                    variance_capacity=variance_capacity)
    t.generate_traffic()
    filename='traffic_matrix_pod250_load50_%d.csv' % i
    df = pd.DataFrame(t.traffic_matrix)
    df.to_csv(filename, index=False, header=False)
    s.append(np.sum(t.traffic_matrix))
print np.mean(s)