clc;
clear;
close all;

% import benchmark data
fileName1 = 'pod100_benchmark.csv';
% fileName2 = 'pod150_benchmark.csv';
% fileName3 = 'pod200_benchmark.csv';
pod100BM = importfile_benchmark(fileName1, 2, 21);
% pod150BM = mean(importfile_benchmark(fileName2, 2, 21));
% pod200BM = mean(importfile_benchmark(fileName3, 2, 21));

% pod100BM = reshape(pod100BM, 2, 12);
% pod150BM = reshape(pod150BM, 2, 12);
% pod200BM = reshape(pod200BM, 2, 12);

% import MILP data
% connections
fileName1 = 'pod100_connections.csv';
pod100CO = importfile_milp(fileName1, 2, 21);

% POD100 arch2
% figure1 = figure; 
% axes1 = axes('Parent', figure1);
% box(axes1, 'on')
% hold(axes1, 'on')
% title('Architecture 2')
% xlabel('connection')
% ylabel('throughput')
% 
% plot(pod100BM(1, 1), pod100BM(2, 1), 'o', 'displayname', 'Arch2 FF fwd', 'linewidth', 2)
% plot(pod100BM(1, 2), pod100BM(2, 2), 'o', 'displayname', 'Arch2 FF bkd', 'linewidth', 2)
% % plot(pod100BM(1, 3), pod100BM(2, 3), 'o', 'displayname', 'Arch2_AJ_fwd')
% plot(pod100BM(1, 4), pod100BM(2, 4), 'o', 'displayname', 'Arch2 AJ bkd', 'linewidth', 2)
% 
% legend(axes1, 'show');