clc;
clear;
close all;

numPods = 100;
numCores = 3;
numSlots = 80;

betav = [0, 0.04, 1];
rupcPerCore = zeros(length(betav), 2); 
rupcPerPod = zeros(length(betav), 2);
obj = zeros(length(betav), 2);
uePerSlot = zeros(length(betav), 2);
uePerCore = zeros(length(betav), 2);
uePerPod = zeros(length(betav), 2);
matrixResource = cell(length(betav), 2);
for i = 1:length(betav)
    method = 'milp';
    [matrixResource{i, 1}, rupcPerCore(i, 1), rupcPerPod(i, 1), ...
        obj(i, 1), uePerSlot(i, 1), uePerCore(i, 1), uePerPod(i, 1)] = ...
        processResult(betav(i), method, numPods, numCores, numSlots);
    
    method = 'heuristic';
    [matrixResource{i, 2}, rupcPerCore(i, 2), rupcPerPod(i, 2), ...
        obj(i, 2), uePerSlot(i, 2), uePerCore(i, 2), uePerPod(i, 2)] = ...
        processResult(betav(i), method, numPods, numCores, numSlots);
end

%% Plot resource utilization per core/pod
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
bar1 = bar(rupcPerCore);
bar1(1).FaceColor = [0, 0.45, 0.74];
bar1(2).FaceColor = [0.85, 0.33, 0.1];
set(bar1(1), 'displayname', 'Heuristic')
set(bar1(2), 'displayname', 'MILP')
h = legend(axes1, 'show', 'location', 'southwest');
h.FontSize = 12;
saveas(figure1, 'RUPCArch4Old.jpg')

%% Plot utilization entropy per core/pod
figure2 = figure;
axes2 = axes('Parent', figure2);
hold(axes2, 'on');
box(axes2, 'on');
grid(axes2, 'on');
set(axes2, 'ytick', [0, 0.02, 0.04, 0.06, 0.08, 0.10]);
set(axes2, 'xtick', [1, 2, 3]);
set(axes2, 'xticklabel', [0, 0.04, 1]);
xlabel('\beta', 'fontsize', 12)
bar2 = bar(uePerPod);
bar2(1).FaceColor = [0, 0.45, 0.74];
bar2(2).FaceColor = [0.85, 0.33, 0.1];
set(bar2(1), 'displayname', 'Heuristic')
set(bar2(2), 'displayname', 'MILP')
h = legend(axes2, 'show', 'location', 'northeast');
h.FontSize = 12;
saveas(figure2, 'UEPCArch4Old.jpg')

%% Save data
uepcArch4Old = uePerPod;
rupcArch4Old = rupcPerCore;
save('Arch4Old.mat', 'uepcArch4Old', 'rupcArch4Old')