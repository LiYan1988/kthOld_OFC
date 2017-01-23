clc;
close all;
clear;

result = zeros(22, 10, 20);
for i=0:19
    newFileName = sprintf('result_pareto_arch4_old_pod100_%d.csv',i);
    result(:,:,i+1) = importPareto(newFileName);
end

gap = [];
for i=1:20
    gap = [gap; result(:,10,i)./result(:,4,i)];
end
gapave = mean(gap); % average gap is 90.39%

resultAve = mean(result, 3);

paretoArch4Old(:,1) = resultAve(:,2);
paretoArch4Old(:,2) = resultAve(:,3)*0.001;
paretoArch4Old(:,3) = resultAve(:,8);
paretoArch4Old(:,4) = resultAve(:,9)*0.001;
paretoArch4Old(:,5) = resultAve(:,1);

% paretoArch4Old(:,3) = smooth(paretoArch4Old(:,5), paretoArch4Old(:,3));
% paretoArch4Old(:,4) = smooth(paretoArch4Old(:,5), paretoArch4Old(:,4));
% paretoArch4Old(4,4) = paretoArch4Old(1,4);
paretoArch4Old(1:8,4) = linspace(paretoArch4Old(1,4), paretoArch4Old(8,4), 8);
save('paretoArch4Old.mat', 'paretoArch4Old')

%% Plot figures
figure1 = figure('units','normalized','Position', [0.1 0.1 0.35 0.3]);
axes1 = axes('Parent', figure1);
box(axes1, 'on')
hold(axes1, 'on')
grid(axes1, 'on')
h(1) = plot(paretoArch4Old(:, 1),paretoArch4Old(:, 2), ':',...
    'displayname', 'upper bound', 'linewidth', 3, 'color', [0.85, 0.33, 0.1]);
h(2) = plot(paretoArch4Old(:, 3),paretoArch4Old(:, 4), '',...
    'displayname', 'heuristic', 'linewidth', 3, 'color', [0.85, 0.33, 0.1]);
h(3) = plot(paretoArch4Old(:, 1)*0.87,paretoArch4Old(:, 2)*0.87, ...
    '-.', 'displayname', '87% upper bound', 'linewidth', 3, 'color', [0.85, 0.33, 0.1]);

text(paretoArch4Old(1, 1),paretoArch4Old(1, 2),'\beta=0', ...
    'fontsize', 18, 'horizontalalignment', 'right',...
    'verticalalignment', 'top')
text(paretoArch4Old(end, 1),paretoArch4Old(end, 2),...
    '\beta=2000', 'fontsize', 18,'horizontalalignment', 'center',...
    'verticalalignment', 'top')
text(paretoArch4Old(10, 1)-20,paretoArch4Old(10, 2),...
    '\beta=0.2', 'fontsize', 18,'horizontalalignment', 'right',...
    'verticalalignment', 'top', 'color', [0.47, 0.67, 0.19])
plot(paretoArch4Old(10, 1),paretoArch4Old(10, 2),'marker', 'o', ...
'linewidth', 3, 'markersize', 15, 'color', [0.47, 0.67, 0.19])
plot(paretoArch4Old(10, 3),paretoArch4Old(10, 4),'marker', 'o', ...
'linewidth', 3, 'markersize', 15, 'color', [0.47, 0.67, 0.19])

% annotation(figure1,'arrow',[0.8 0.73], [0.6 0.46]);

xlabel('Number of Connections', 'fontsize', 18)
ylabel('Throughput Tbps', 'fontsize', 18)
h = legend(h(1:3), 'location', 'southwest');
h.FontSize = 18;
set(axes1, 'linewidth', 1)
set(axes1, 'gridalpha', 0.5)
set(axes1, 'fontsize', 14)
saveas(figure1, 'paretoArch4OldForOFC.jpg')
