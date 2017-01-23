clc;
clear all;
close all;

num_pods = 200;
num_cores = 3;
num_specs = 80;
res1 = importfile_spec80('A2B1.csv', num_pods, num_cores, num_specs);
res2 = importfile_spec80('A2B2.csv', num_pods, num_cores, num_specs);
res3 = importfile_spec80('A2SA.csv', num_pods, num_cores, num_specs);