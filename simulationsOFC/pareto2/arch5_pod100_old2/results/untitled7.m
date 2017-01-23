clc;
close all;
clear;

betav = [0, 1e-5, 2e-5, 4e-5, 8e-5, 1e-4, 2e-4, 4e-4, 8e-4, ...
    1e-3, 2e-3, 4e-3, 8e-3, 1e-2, 2e-2, 4e-2, 8e-2, 1e-1];


cores_used = cell(18, 1);
core_hist = zeros(18, 3);
for i = 1:18
    for j = 1:20
        fileName = sprintf('cnklist_heuristic_%d_%.2e.csv', j-1, betav(i));
        [src,dst,spec,slots_used,core_src,core_dst,tmp,tfk_slot] = importA5(fileName);
        cores_used{i} = [cores_used{i};tmp];
    end
    core_hist(i,:) = hist(cores_used{i}, 3);
    core_hist(i,:) = core_hist(i,:)./sum(core_hist(i,:));
end

figure1 = createArea(betav, core_hist);
% saveas(figure1, 'arch5coreUsage.jpg')
