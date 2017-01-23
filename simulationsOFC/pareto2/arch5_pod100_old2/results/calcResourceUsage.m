clc;
clear;
close all;

%% Data processing
betav = [0, 1e-5, 2e-5, 4e-5, ...
    8e-5, 1e-4, 2e-4, 4e-4, ...
    8e-4, 1e-3, 2e-3, 4e-3, ...
    8e-3, 1e-2, 2e-2, 4e-2, ...
    8e-2, 1e-1];

numPods = 100;
numCores = 3;
numSlots = 80;

efficiencies = zeros(20, length(betav));
utilizationEntropyAve = zeros(20, length(betav));
utilizationEntropyStd = zeros(20, length(betav));
resourceUsageAve = zeros(20, 18);
outages = zeros(20, 18);

tfkhist = zeros(6, length(betav));
tfktmp = zeros(6, length(betav));

for i = 1:20
    for j = 1:length(betav)
        fileName = sprintf('cnklist_heuristic_%d_%.2e.csv', i-1, betav(j));
        [src1,dst1,spec1,slots_used1,core_src1,core_dst1,...
            cores_used,tfk_slot,cnkMatrix] = importCnk(fileName);
        [matrixResource, efficiencies(i, j), outages(i, j)] = ...
            resourceUsage(numPods, numCores, numSlots, cnkMatrix);
        [~, utilizationEntropyPerCore, ~] = ...
            utilizationEntropy(matrixResource, numCores);
        utilizationEntropyAve(i, j) = mean(utilizationEntropyPerCore);
        utilizationEntropyStd(i, j) = std(utilizationEntropyPerCore);
        resourceUsageAve(i, j) = sum(matrixResource(:))/(numPods*numCores*numSlots);
        
        a = unique(tfk_slot);
        b = hist(tfk_slot, a);
        tmp = zeros(6, 1);
        for k=1:length(a)
            if a(k)==1
                tmp(1) = b(k);
            elseif a(k)==10
                tmp(2) = b(k);
            elseif a(k)==100
                tmp(3) = b(k);
            elseif a(k)==200
                tmp(4) = b(k);
            elseif a(k)==400
                tmp(5) = b(k);
            elseif a(k)==1000
                tmp(6) = b(k);
            end
        end
        tmp = tmp/sum(tmp);
        tfkhist(:,j) = tfkhist(:,j)+tmp;
        tfktmp(:, j) = tmp;
    end
end

ueAveVsBetaA5 = mean(utilizationEntropyAve, 1);
ueStdVsBetaA5 = mean(utilizationEntropyStd, 1);
efVsBetaA5 = mean(efficiencies, 1);
ruVsBetaA5 = mean(resourceUsageAve, 1);

tfkhistAve = (tfkhist./repmat(sum(tfkhist, 1), 6, 1))';
%% Plot
figure1 = figure;
axes1 = axes('parent', figure1);

h(1) = semilogx(betav, ueAveVsBetaA5, 'linewidth', 2, ...
    'displayname', 'Architecture 2');

box(axes1, 'on')
grid(axes1, 'on')
xlabel('\beta', 'fontsize', 16)
ylabel('Usage entropy', 'fontsize', 16)
ytick = get(axes1, 'ytick');
set(axes1, 'ytick', ytick(1:2:end))
h = legend(h(:), 'location', 'northeast');
h.FontSize = 12;
% saveas(figure1, 'usageEntropyVsBeta.jpg')

%%
figure2 = figure;
axes2 = axes('parent', figure2);

h(1) = semilogx(betav, ruVsBetaA5, 'linewidth', 2, ...
    'displayname', 'resource usage');
% h(2) = semilogx(betav, efVsBeta, 'linewidth', 2, ...
%     'displayname', 'efficiency');

box(axes2, 'on')
grid(axes2, 'on')
xlabel('\beta', 'fontsize', 16)
ylabel('Usage entropy', 'fontsize', 16)
ytick = get(axes2, 'ytick');
set(axes2, 'ytick', ytick(1:2:end))
h = legend(h(1), 'location', 'southeast');
h.FontSize = 12;

save('arch5RU.mat', 'ruVsBetaA5', 'efVsBetaA5', 'ueAveVsBetaA5', 'efVsBetaA5')

%% 
figure4 = figure;
axes4 = axes('Parent', figure4);
tfkhistPlot = zeros(length(betav), 5);
tfkhistPlot(:,1) = tfkhistAve(:,1)+tfkhistAve(:,2);
tfkhistPlot(:,2) = tfkhistAve(:,3);
tfkhistPlot(:,3) = tfkhistAve(:,4);
tfkhistPlot(:,4) = tfkhistAve(:,5);
tfkhistPlot(:,5) = tfkhistAve(:,6);
% tfkhistPlot(end+1, :) = tfkhistPlot(end, :);
% tfkhistPlot(end+2, :) = tfkhistPlot(end, :);
% tfkhistPlot(end+3, :) = tfkhistPlot(end, :);
% tfkhistPlot(end+4, :) = tfkhistPlot(end, :);
betav2 = [betav, 2e-1, 4e-1, 1, 10];
area1 = area(betav, tfkhistPlot);
legend('<=10Gbps', '100Gbps', '200Gbps', '400Gbps', '1000Gbps')
set (gca, 'Xscale', 'log');
ylim([0, 1])
xlim([1e-5, 10])
set(axes4, 'xtick', [1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1e0, 1e1])
area1(1).FaceColor = [0, 0.45, 0.74];
area1(2).FaceColor = [217, 83, 25]/255;
area1(3).FaceColor = [0.47, 0.67, 0.19];
area1(4).FaceColor = [0, 0.75, 0.75];
area1(5).FaceColor = [0.929411768913269 0.694117665290833 0.125490203499794];

saveas(figure4, 'areaA4tfkhist.jpg')