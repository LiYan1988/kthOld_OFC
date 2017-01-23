clc;
clear all;
close all;

numPods = 100;
numCores = 1;
numSlots = 80;

trafficMatrix = importFileTrafficMatrix('traffic_matrix.csv');

%%
% 
%  PREFORMATTED
%  For the MILP to be better than the heuristic in architecture 4, the MILP
%  needs to be run for long enough time, I think at least one hour.
% 


%% Import tensor data, MILP
% alpha=1, beta=0, MILP
fileName = 'tensor_milp_0.000000e+00.csv';
tensorMILP0 = 1-importFileTensor(fileName, 1, numPods*numCores);
% figure; 
% spy(tensorMILP0)
rupcMILP0 = sum(tensorMILP0,2)/numSlots; % resource utilization per core
rupcMILP0Ave = mean(rupcMILP0);

%% Import tensor data, heuristic
% alpha=1, beta=0, heuristic
fileName = 'tensor_heuristic_0.000000e+00.csv';
tensorHeuristic0 = 1-importFileTensor(fileName, 1, numPods*numCores);
% figure; 
% spy(tensorHeuristic0)
rupcHeuristic0 = sum(tensorHeuristic0,2)/numSlots; % resource utilization per core
rupcHeuristic0Ave = mean(rupcHeuristic0);

%% Plot 
subplot(1, 2, 1)
spy(tensorMILP0)
subplot(1, 2, 2)
spy(tensorHeuristic0)