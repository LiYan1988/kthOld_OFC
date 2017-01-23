clc;
clear all;
close all;

numPods = 100;
numCores = 3;
numSlots = 80;

trafficMatrix = importFileTrafficMatrix('traffic_matrix.csv');

%% Import tensor data, MILP
% alpha=1, beta=0, MILP
fileName = 'tensor_milp_0.000000e+00.csv';
tensorMILP0 = 1-importFileTensor(fileName, 1, numPods*numCores);
% figure; 
% spy(tensorMILP0)
rupcMILP0 = sum(tensorMILP0,2)/numSlots; % resource utilization per core
rupcMILP0Ave = mean(rupcMILP0);

% alpha=1, beta=0.04, MILP
fileName = 'tensor_milp_4.000000e-02.csv';
tensorMILP1 = 1-importFileTensor(fileName, 1, numPods*numCores);
% figure; 
% spy(tensorMILP1)
rupcMILP1 = sum(tensorMILP1,2)/numSlots; 
rupcMILP1Ave = mean(rupcMILP1);

% alpha=1, beta=0.2, MILP
fileName = 'tensor_milp_2.000000e-01.csv';
tensorMILP2 = 1-importFileTensor(fileName, 1, numPods*numCores);
% figure;
% spy(tensorMILP2)
rupcMILP2 = sum(tensorMILP2,2)/numSlots;
rupcMILP2Ave = mean(rupcMILP2);
subplot(1, 3, 1); spy(tensorMILP0)
subplot(1, 3, 2); spy(tensorMILP1)
subplot(1, 3, 3); spy(tensorMILP2)

%% Import tensor data, heuristic
% alpha=1, beta=0, heuristic
fileName = 'tensor_heuristic_0.000000e+00.csv';
tensorHeuristic0 = 1-importFileTensor(fileName, 1, numPods*numCores);
% figure; 
% spy(tensorHeuristic0)
rupcHeuristic0 = sum(tensorHeuristic0,2)/numSlots; % resource utilization per core
rupcHeuristic0Ave = mean(rupcHeuristic0);

% alpha=1, beta=0.04, heuristic
fileName = 'tensor_heuristic_4.000000e-02.csv';
tensorHeuristic1 = 1-importFileTensor(fileName, 1, numPods*numCores);
% figure; 
% spy(tensorHeuristic1)
rupcHeuristic1 = sum(tensorHeuristic1,2)/numSlots; 
rupcHeuristic1Ave = mean(rupcHeuristic1);

% alpha=1, beta=0.2, heuristic
fileName = 'tensor_heuristic_2.000000e-01.csv';
tensorHeuristic2 = 1-importFileTensor(fileName, 1, numPods*numCores);
% figure;
% spy(tensorHeuristic2)
rupcHeuristic2 = sum(tensorHeuristic2,2)/numSlots;
rupcHeuristic2Ave = mean(rupcHeuristic2);

%% Plot average RUPC
rupcAve = [[rupcHeuristic0Ave, rupcMILP0Ave];...
    [rupcHeuristic1Ave, rupcMILP1Ave];...
    [rupcHeuristic2Ave, rupcMILP2Ave]];
figure1 = figure;
axes1 = axes('Parent', figure1);
hold(axes1, 'on');
box(axes1, 'on');
grid(axes1, 'on');
set(axes1, 'ytick', [0, 0.2, 0.4, 0.6, 0.8, 1]);
pct = [cellstr(num2str(get(axes1, 'ytick')'*100))];
pct = [char(pct), char(ones(size(pct,1),1)*'%')];
set(axes1, 'yticklabel', pct);
set(axes1, 'xtick', [1, 2, 3]);
set(axes1, 'xticklabel', [0, 0.04, 1]);
xlabel('\beta', 'fontsize', 12)
ylabel('Resource utilization', 'fontsize', 12)
bar1 = bar(rupcAve);
bar1(1).FaceColor = [0.85, 0.33, 0.1];
bar1(2).FaceColor = [0, 0.45, 0.74];
set(bar1(1), 'displayname', 'Heuristic')
set(bar1(2), 'displayname', 'MILP')
h = legend(axes1, 'show', 'location', 'northwest');
h.FontSize = 12;
saveas(figure1, 'RUPCArch2Old.jpg')

%% Calculate utilization entropy
% alpha=1, beta=0, MILP
[utilizationEntropyPerSlotMILP0, utilizationEntropyPerCoreMILP0, ...
    utilizationEntropyPerPodMILP0] = ...
    utilizationEntropy(tensorMILP0, numCores);
% average core utilization entropy
ueCoreMILP0Ave = mean(utilizationEntropyPerCoreMILP0); 
% average pod utilization entropy
uePodMILP0Ave = mean(utilizationEntropyPerPodMILP0);

% alpha=1, beta=0.04, MILP
[utilizationEntropyPerSlotMILP1, utilizationEntropyPerCoreMILP1, ...
    utilizationEntropyPerPodMILP1] = ...
    utilizationEntropy(tensorMILP1, numCores);
% average core utilization entropy
ueCoreMILP1Ave = mean(utilizationEntropyPerCoreMILP1); 
% average pod utilization entropy
uePodMILP1Ave = mean(utilizationEntropyPerPodMILP1);

% alpha=1, beta=0.2, MILP
[utilizationEntropyPerSlotMILP2, utilizationEntropyPerCoreMILP2, ...
    utilizationEntropyPerPodMILP2] = ...
    utilizationEntropy(tensorMILP2, numCores);
% average core utilization entropy
ueCoreMILP2Ave = mean(utilizationEntropyPerCoreMILP2); 
% average pod utilization entropy
uePodMILP2Ave = mean(utilizationEntropyPerPodMILP2);

% alpha=1, beta=0, heuristic
[utilizationEntropyPerSlotHeuristic0, ...
    utilizationEntropyPerCoreHeuristic0, ...
    utilizationEntropyPerPodHeuristic0] = ...
    utilizationEntropy(tensorHeuristic0, numCores);
% average core utilization entropy
ueCoreHeuristic0Ave = mean(utilizationEntropyPerCoreHeuristic0); 
% average pod utilization entropy
uePodHeuristic0Ave = mean(utilizationEntropyPerPodHeuristic0);

% alpha=1, beta=0.04, heuristic
[utilizationEntropyPerSlotHeuristic1, ...
    utilizationEntropyPerCoreHeuristic1, ...
    utilizationEntropyPerPodHeuristic1] = ...
    utilizationEntropy(tensorHeuristic1, numCores);
% average core utilization entropy
ueCoreHeuristic1Ave = mean(utilizationEntropyPerCoreHeuristic1); 
% average pod utilization entropy
uePodHeuristic1Ave = mean(utilizationEntropyPerPodHeuristic1);

% alpha=1, beta=0.2, heuristic
[utilizationEntropyPerSlotHeuristic2, ...
    utilizationEntropyPerCoreHeuristic2, ...
    utilizationEntropyPerPodHeuristic2] = ...
    utilizationEntropy(tensorHeuristic2, numCores);
% average core utilization entropy
ueCoreHeuristic2Ave = mean(utilizationEntropyPerCoreHeuristic2); 
% average pod utilization entropy
uePodHeuristic2Ave = mean(utilizationEntropyPerPodHeuristic2);

ueCoreAve = [[ueCoreHeuristic0Ave,ueCoreMILP0Ave];...
    [ueCoreHeuristic1Ave,ueCoreMILP1Ave];...
    [ueCoreHeuristic2Ave,ueCoreMILP2Ave]];
figure2 = figure;
axes2 = axes('Parent', figure2);
hold(axes2, 'on');
box(axes2, 'on');
grid(axes2, 'on');
% set(axes1, 'ytick', [0, 0.2, 0.4, 0.6, 0.8, 1]);
% pct = [cellstr(num2str(get(axes1, 'ytick')'*100))];
% pct = [char(pct), char(ones(size(pct,1),1)*'%')];
% set(axes1, 'yticklabel', pct);
set(axes2, 'xtick', [1, 2, 3]);
set(axes2, 'xticklabel', [0, 0.04, 1]);
xlabel('\beta', 'fontsize', 12)
ylabel('Utilization Entropy', 'fontsize', 12)
bar2 = bar(ueCoreAve);
set(bar2(1), 'displayname', 'Heuristic')
set(bar2(2), 'displayname', 'MILP')
bar2(1).FaceColor = [0.85, 0.33, 0.1];
bar2(2).FaceColor = [0, 0.45, 0.74];
h = legend(axes2, 'show', 'location', 'northeast');
h.FontSize = 12;
saveas(figure2, 'UEPCArch2Old.jpg')

%% Save data
uepcArch2Old = ueCoreAve;
rupcArch2Old = rupcAve;
save('Arch2Old.mat', 'uepcArch2Old', 'rupcArch2Old')