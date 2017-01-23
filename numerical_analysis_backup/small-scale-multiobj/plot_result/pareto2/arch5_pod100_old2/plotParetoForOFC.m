clc;
clear;
close all;

%% Prepare data
connection_ub = zeros(18, 20);
throughput_ub = zeros(18, 20);
obj_ub = zeros(18, 20);
connection_lb = zeros(18, 20);
throughput_lb = zeros(18, 20);
obj_lb = zeros(18, 20);
beta = zeros(18, 1);
for i = 1:20
    fileName1 = sprintf('result_pareto_arch5_old_1_%d.csv', i-1);
    fileName2 = sprintf('result_pareto_arch5_old_2_%d.csv', i-1);
    fileName3 = sprintf('result_pareto_arch5_old_3_%d.csv', i-1);
    fileName4 = sprintf('result_pareto_arch5_old_4_%d.csv', i-1);
    fileName5 = sprintf('result_pareto_arch5_old_5_%d.csv', i-1);
    [beta(1:4),connection_ub(1:4, i),throughput_ub(1:4, i),obj_ub(1:4, i),...
        connection_lb(1:4, i),throughput_lb(1:4, i),obj_lb(1:4, i)] = ...
        importResult14(fileName1);
    [beta(5:8),connection_ub(5:8, i),throughput_ub(5:8, i),obj_ub(5:8, i),...
        connection_lb(5:8, i),throughput_lb(5:8, i),obj_lb(5:8, i)] = ...
        importResult14(fileName2);
    [beta(9:12),connection_ub(9:12, i),throughput_ub(9:12, i),obj_ub(9:12, i),...
        connection_lb(9:12, i),throughput_lb(9:12, i),obj_lb(9:12, i)] = ...
        importResult14(fileName3);
    [beta(13:16),connection_ub(13:16, i),throughput_ub(13:16, i),obj_ub(13:16, i),...
        connection_lb(13:16, i),throughput_lb(13:16, i),obj_lb(13:16, i)] = ...
        importResult14(fileName4);
    [beta(17:18),connection_ub(17:18, i),throughput_ub(17:18, i),obj_ub(17:18, i),...
        connection_lb(17:18, i),throughput_lb(17:18, i),obj_lb(17:18, i)] = ...
        importResult5(fileName5);
end

paretoArch5Old2 = zeros(18, 4);
paretoArch5Old2(:, 1) = mean(connection_ub, 2);
paretoArch5Old2(:, 2) = mean(throughput_ub, 2)*0.001;
paretoArch5Old2(:, 3) = mean(connection_lb, 2);
paretoArch5Old2(:, 4) = mean(throughput_lb, 2)*0.001;
paretoArch5Old2(:, 5) = beta;

paretoArch5Old2(:, 3) = smooth(beta, paretoArch5Old2(:, 3),5);
paretoArch5Old2(:, 4) = smooth(beta, paretoArch5Old2(:, 4),5);

save('paretoArch5Old2.mat', 'paretoArch5Old2')

%% Plot figures
figure1 = figure('units','normalized','Position', [0.1 0.1 0.35 0.3]);
axes1 = axes('Parent', figure1);
box(axes1, 'on')
hold(axes1, 'on')
grid(axes1, 'on')
h(1) = plot(paretoArch5Old2(:, 1),paretoArch5Old2(:, 2), ':',...
    'displayname', 'upper bound', 'linewidth', 3, 'color', [0, 0.45, 0.74]);
h(2) = plot(paretoArch5Old2(:, 3),paretoArch5Old2(:, 4), '',...
    'displayname', 'heuristic', 'linewidth', 3, 'color', [0, 0.45, 0.74]);
h(3) = plot(paretoArch5Old2(:, 1)*0.91,paretoArch5Old2(:, 2)*0.91, ...
    '-.', 'displayname', '91% upper bound', 'linewidth', 3, 'color', [0, 0.45, 0.74]);

text(paretoArch5Old2(1, 1),paretoArch5Old2(1, 2),'\beta=0', ...
    'fontsize', 18, 'horizontalalignment', 'right',...
    'verticalalignment', 'top')
text(paretoArch5Old2(end, 1),paretoArch5Old2(end, 2),...
    '\beta=2000', 'fontsize', 18,'horizontalalignment', 'center',...
    'verticalalignment', 'top')
text(paretoArch5Old2(12, 1)-8,paretoArch5Old2(12, 2)-8,...
    '\beta=0.8', 'fontsize', 18,'horizontalalignment', 'right',...
    'verticalalignment', 'top', 'color', [0.47, 0.67, 0.19])
plot(paretoArch5Old2(12, 1),paretoArch5Old2(12, 2),'marker', 'o', ...
'linewidth', 3, 'markersize', 15, 'color', [0.47, 0.67, 0.19])
plot(paretoArch5Old2(12, 3),paretoArch5Old2(12, 4),'marker', 'o', ...
'linewidth', 3, 'markersize', 15, 'color', [0.47, 0.67, 0.19])

% annotation(figure1,'arrow',[0.8 0.73], [0.6 0.46]);

xlabel('Number of Connections', 'fontsize', 18)
ylabel('Throughput Tbps', 'fontsize', 18)
h = legend(h(1:3), 'location', 'southwest');
h.FontSize = 18;
set(axes1, 'linewidth', 1)
set(axes1, 'gridalpha', 0.5)
set(axes1, 'fontsize', 14)
saveas(figure1, 'paretoArch5Old2ForOFC.jpg')

%%
% figure2 = figure('units','normalized','Position', [0.1 0.1 0.35 0.3]);
% axes2 = axes('parent', figure2);
% 
% x=[beta(2:end); 0.2; 0.4; 0.8; 1; 2; 4; 8; 10]*200;
% y1=[paretoArch5Old2(2:end, 2); paretoArch5Old2(end, 2)*ones(8, 1)];
% y2=[paretoArch5Old2(2:end, 4); paretoArch5Old2(end, 4)*ones(8, 1)];
% 
% h(1) = semilogx(x, y1, 'linewidth', 2, ...
%     'displayname', 'upper bound');
% hold(axes2, 'on')
% h(2) = semilogx(x, y2, 'linewidth', 2, ...
%     'displayname', 'heuristic');
% 
% % h(1) = semilogx(beta, paretoArch5Old2(:, 2), 'linewidth', 2, ...
% %     'displayname', 'upper bound');
% % hold(axes2, 'on')
% % h(2) = semilogx(beta, paretoArch5Old2(:, 4), 'linewidth', 2, ...
% %     'displayname', 'heuristic');
% 
% box(axes2, 'on')
% grid(axes2, 'on')
% % xlim(axes2, [1e-5, 10]);
% xlabel('\beta', 'fontsize', 16)
% ylabel('Throughput Tbps', 'fontsize', 16)
% h = legend(h(1:2), 'location', 'southeast');
% h.FontSize = 12;
% % saveas(figure2, 'connectionsVsBeta.jpg')
