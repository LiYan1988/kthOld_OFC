% POD 100, arch2

clc;
clear;
close all;

% import benchmark data
fileName1 = 'pod100_benchmark.csv';
pod100Bm = importfile_benchmark(fileName1, 2, 21);
pod100BmAvg = mean(pod100Bm);
pod100BmAvg = reshape(pod100BmAvg, 2, 12); % [connection; throughput]

% import MILP data
% connections
fileName1 = 'pod100_connections.csv';
pod100Co = importfile_milp(fileName1, 2, 21);
pod100TotalTraffic = pod100Co(:, end);
pod100CoAvg = mean(pod100Co(:, 1:end-1));
pod100CoAvg = [[pod100CoAvg(7);pod100CoAvg(9)], ...
               [pod100CoAvg(8); pod100CoAvg(10)],...
               [pod100CoAvg(1);pod100CoAvg(3)], ...
               [pod100CoAvg(2); pod100CoAvg(4)],...
               [pod100CoAvg(11);pod100CoAvg(13)], ...
               [pod100CoAvg(12); pod100CoAvg(14)]];
% throughput
fileName1 = 'pod100_throughput.csv';
pod100Th = importfile_milp(fileName1, 2, 21);
pod100ThAvg = mean(pod100Th(:, 1:end-1));
pod100ThAvg = [[pod100ThAvg(7);pod100ThAvg(9)], ...
               [pod100ThAvg(8); pod100ThAvg(10)],...
               [pod100ThAvg(1);pod100ThAvg(3)], ...
               [pod100ThAvg(2); pod100ThAvg(4)],...
               [pod100ThAvg(11);pod100ThAvg(13)], ...
               [pod100ThAvg(12); pod100ThAvg(14)]];
% hybrid
fileName1 = 'pod100_hybrid.csv';
pod100Hy = importfile_milp(fileName1, 2, 21);
pod100HyAvg = mean(pod100Hy(:, 1:end-1));
pod100HyAvg = [[pod100HyAvg(7);pod100HyAvg(9)], ...
               [pod100HyAvg(8); pod100HyAvg(10)],...
               [pod100HyAvg(1);pod100HyAvg(3)], ...
               [pod100HyAvg(2); pod100HyAvg(4)],...
               [pod100HyAvg(11);pod100HyAvg(13)], ...
               [pod100HyAvg(12); pod100HyAvg(14)]];

% Architecture 4, POD 100
figure1 = figure; 
axes1 = axes('Parent', figure1);
box(axes1, 'on')
hold(axes1, 'on')
title('Architecture 2 vs 5, only optimal solutions')
xlabel('connection')
ylabel('throughput')
% xlim([200, 1200])
% ylim([1000, 2500])

%% arch2
% plot(pod100BmAvg(1, 1), pod100BmAvg(2, 1)*0.01, 'o', 'displayname', 'Arch2 FF FWD', 'linewidth', 2)
% text(pod100BmAvg(1, 1)+10, pod100BmAvg(2, 1)*0.01, 'FF FWD')
% plot(pod100BmAvg(1, 2), pod100BmAvg(2, 2)*0.01, '*', 'displayname', 'Arch2 FF BWD', 'linewidth', 2)
% text(pod100BmAvg(1, 2)+10, pod100BmAvg(2, 2)*0.01, 'FF BWD')
% plot(pod100BmAvg(1, 4), pod100BmAvg(2, 4)*0.01, '+', 'displayname', 'Arch2 AJ BWD', 'linewidth', 2)
% text(pod100BmAvg(1, 4)+10, pod100BmAvg(2, 4)*0.01, 'AJ')

x = (1*pod100CoAvg(1, 2)+0*pod100CoAvg(1, 1));
y = (1*pod100CoAvg(2, 2)*0.01+0*pod100CoAvg(2, 1)*0.01);
plot(x, y, 'd', 'displayname', 'Arch2 Co MILP UB', 'linewidth', 2)
text(x-50, y-10, 'Arch 2 MILP Connection')

x = (0*pod100ThAvg(1, 1)+pod100ThAvg(1, 2));
y = (0*pod100ThAvg(2, 1)*0.01+pod100ThAvg(2, 2)*0.01);
plot(x, y, '^', 'displayname', 'Arch2 Th MILP UB', 'linewidth', 2)
text(x+10, y, 'Arch 2 MILP Throughput')

x = (0*pod100HyAvg(1, 1)+pod100HyAvg(1, 2));
y = (0*pod100HyAvg(2, 1)*0.01+pod100HyAvg(2, 2)*0.01);
plot(x, y, '^', 'displayname', 'Arch2 Hy MILP UB', 'linewidth', 2)
text(x+10, y, 'Arch 2 MILP Hybrid')

%% arch4
% plot(pod100BmAvg(1, 5), pod100BmAvg(2, 5)*0.01, 'o', 'displayname', 'Arch2 FF FWD', 'linewidth', 2)
% text(pod100BmAvg(1, 5)+10, pod100BmAvg(2, 5)*0.01, 'FF FWD')
% plot(pod100BmAvg(1, 6), pod100BmAvg(2, 6)*0.01, '*', 'displayname', 'Arch2 FF BWD', 'linewidth', 2)
% text(pod100BmAvg(1, 6)+10, pod100BmAvg(2, 6)*0.01, 'FF BWD')
% plot(pod100BmAvg(1, 8), pod100BmAvg(2, 8)*0.01, '+', 'displayname', 'Arch2 AJ BWD', 'linewidth', 2)
% text(pod100BmAvg(1, 8)+10, pod100BmAvg(2, 8)*0.01, 'AJ')
% 
% x = 0.5*(pod100CoAvg(1, 4)+pod100CoAvg(1, 3));
% y = 0.5*(pod100CoAvg(2, 4)*0.01+pod100CoAvg(2, 3)*0.01);
% plot(x, y, 'd', 'displayname', 'Arch2 Co MILP UB', 'linewidth', 2)
% text(x+10, y, 'MILP Connection')
% 
% x = 0.5*(pod100ThAvg(1, 3)+pod100ThAvg(1, 4));
% y = 0.5*(pod100ThAvg(2, 3)*0.01+pod100ThAvg(2, 4)*0.01);
% plot(x, y, '^', 'displayname', 'Arch2 Th MILP UB', 'linewidth', 2)
% text(x+10, y, 'MILP Throughput')
% 
% x = (0.25*pod100HyAvg(1, 3)+0.75*pod100HyAvg(1, 4));
% y = (0.25*pod100HyAvg(2, 3)*0.01+0.75*pod100HyAvg(2, 4)*0.01);
% plot(x, y, '^', 'displayname', 'Arch2 Hy MILP UB', 'linewidth', 2)
% text(x+10, y, 'MILP Hybrid')

%% arch5
% plot(pod100BmAvg(1, 9), pod100BmAvg(2, 9)*0.01, 'o', 'displayname', 'Arch2 FF FWD', 'linewidth', 2)
% text(pod100BmAvg(1, 9)+10, pod100BmAvg(2, 9)*0.01, 'FF FWD')
% plot(pod100BmAvg(1, 10), pod100BmAvg(2, 10)*0.01, '*', 'displayname', 'Arch2 FF BWD', 'linewidth', 2)
% text(pod100BmAvg(1, 10)+10, pod100BmAvg(2, 10)*0.01, 'FF BWD')
% plot(pod100BmAvg(1, 12), pod100BmAvg(2, 12)*0.01, '+', 'displayname', 'Arch2 AJ BWD', 'linewidth', 2)
% text(pod100BmAvg(1, 12)+10, pod100BmAvg(2, 12)*0.01, 'AJ')

x = 0.5*(2*pod100CoAvg(1, 6)+0*pod100CoAvg(1, 5));
y = 0.5*(2*pod100CoAvg(2, 6)*0.01+0*pod100CoAvg(2, 5)*0.01);
plot(x, y, 'd', 'displayname', 'Arch2 Co MILP UB', 'linewidth', 2)
text(x-50, y+10, 'Arch 5 MILP Connection')

x = 0.5*(0*pod100ThAvg(1, 5)+2*pod100ThAvg(1, 6));
y = 0.5*(0*pod100ThAvg(2, 5)*0.01+2*pod100ThAvg(2, 6)*0.01);
plot(x, y, '^', 'displayname', 'Arch2 Th MILP UB', 'linewidth', 2)
text(x+10, y, 'Arch 5 MILP Throughput')

x = (0.*pod100HyAvg(1, 5)+1*pod100HyAvg(1, 6));
y = (0.*pod100HyAvg(2, 5)*0.01+1*pod100HyAvg(2, 6)*0.01);
plot(x, y, '^', 'displayname', 'Arch2 Hy MILP UB', 'linewidth', 2)
text(x+10, y, 'Arch 5 MILP Hybrid')