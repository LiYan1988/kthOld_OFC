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

% SA
% fileName1 = 'pod100_arch4_sa.csv';
% pod100Sa = importfile_sa(fileName1);
% pod100SaAvg = mean(pod100Sa);
% pod100SaAvg = [[pod100SaAvg(1); pod100SaAvg(2)],...
%                [pod100SaAvg(3); pod100SaAvg(4)],...
%                [pod100SaAvg(5); pod100SaAvg(6)]];


% Architecture 4, POD 100
figure1 = figure; 
axes1 = axes('Parent', figure1);
box(axes1, 'on')
hold(axes1, 'on')
title('Architecture 4')
xlabel('connection')
ylabel('throughput')
% xlim([200, 1200])
% ylim([1000, 2500])

plot(pod100BmAvg(1, 5), pod100BmAvg(2, 5)*0.01, 'o', 'displayname', 'Arch2 FF FWD', 'linewidth', 2)
text(pod100BmAvg(1, 5)+10, pod100BmAvg(2, 5)*0.01, 'FF FWD')
plot(pod100BmAvg(1, 6), pod100BmAvg(2, 6)*0.01, '*', 'displayname', 'Arch2 FF BWD', 'linewidth', 2)
text(pod100BmAvg(1, 6)+10, pod100BmAvg(2, 6)*0.01, 'FF BWD')
plot(pod100BmAvg(1, 8), pod100BmAvg(2, 8)*0.01, '+', 'displayname', 'Arch2 AJ BWD', 'linewidth', 2)
text(pod100BmAvg(1, 8)+10, pod100BmAvg(2, 8)*0.01, 'AJ')

x = (pod100CoAvg(1, 4));
y = (pod100CoAvg(2, 4)*0.01);
plot(x, y, 'd', 'displayname', 'Arch2 Co MILP UB', 'linewidth', 2)
text(x+10, y, 'MILP Connection')

x = (pod100ThAvg(1, 4));
y = (pod100ThAvg(2, 4)*0.01);
plot(x, y, '^', 'displayname', 'Arch2 Th MILP UB', 'linewidth', 2)
text(x+10, y, 'MILP Throughput')

x = (pod100HyAvg(1, 4));
y = (pod100HyAvg(2, 4)*0.01);
plot(x, y, '^', 'displayname', 'Arch2 Hy MILP UB', 'linewidth', 2)
text(x+10, y, 'MILP Hybrid')

% plot(pod100SaAvg(1, 1), pod100SaAvg(2, 1)*0.01,  '<', 'displayname', 'Arch2 Hy SA', 'linewidth', 2)
% text(pod100SaAvg(1, 1)+10, pod100SaAvg(2, 1)*0.01, 'SA Hybrid')
% plot(pod100SaAvg(1, 2), pod100SaAvg(2, 2)*0.01,  '<', 'displayname', 'Arch2 Co SA', 'linewidth', 2)
% text(pod100SaAvg(1, 2)+10, pod100SaAvg(2, 2)*0.01, 'SA Connection')
% plot(pod100SaAvg(1, 3), pod100SaAvg(2, 3)*0.01,  '<', 'displayname', 'Arch2 Th SA', 'linewidth', 2)
% text(pod100SaAvg(1, 3)+10, pod100SaAvg(2, 3)*0.01, 'SA Throughput')

% legend(axes1, 'show', 'location', 'best');

% Architecture 4, POD 100
% figure2 = figure; 
% axes2 = axes('Parent', figure2);
% box(axes2, 'on')
% hold(axes2, 'on')
% title('Architecture 4')
% xlabel('connection')
% ylabel('throughput')
% 
% plot(pod100BmAvg(1, 1), pod100BmAvg(2, 1), 'o', 'displayname', 'Arch4 FF FWD', 'linewidth', 2)
% plot(pod100BmAvg(1, 2), pod100BmAvg(2, 2), 'o', 'displayname', 'Arch4 FF BWD', 'linewidth', 2)
% % plot(pod100BM(1, 3), pod100BM(2, 3), 'o', 'displayname', 'Arch2_AJ_fwd')
% plot(pod100BmAvg(1, 4), pod100BmAvg(2, 4), 'o', 'displayname', 'Arch4 AJ BWD', 'linewidth', 2)
% plot(pod100CoAvg(1, 1), pod100CoAvg(2, 1), 'o', 'displayname', 'Arch4 MILP LB', 'linewidth', 2)
% plot(pod100CoAvg(1, 2), pod100CoAvg(2, 2), 'o', 'displayname', 'Arch4 MILP UB', 'linewidth', 2)
% 
% legend(axes2, 'show', 'location', 'best');