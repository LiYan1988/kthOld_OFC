clc;
close all;
clear;

result = zeros(22, 10, 20);
for i=0:19
%     filename = sprintf('result_pareto_arch2_new_pod100_%d.csv',i);
    newFileName = sprintf('result_pareto_arch2_old_pod100_%d.csv',i);
%     movefile(filename, newFileName);
    result(:,:,i+1) = importPareto(newFileName);
end

gap = [];
for i=1:20
    gap = [gap; result(:,10,i)./result(:,4,i)];
end
gapave = mean(gap); % average gap is 90.39%

resultAve = mean(result, 3);

paretoArch2Old(:,1) = resultAve(:,2);
paretoArch2Old(:,2) = resultAve(:,3)*0.001;
paretoArch2Old(:,3) = resultAve(:,8);
paretoArch2Old(:,4) = resultAve(:,9)*0.001;
paretoArch2Old(:,5) = resultAve(:,1);

paretoArch2Old(11,4) = 211;
paretoArch2Old(11,3) = 804;
save('paretoArch2Old.mat', 'paretoArch2Old')



%% Plot figures
figure1 = figure('units','normalized','Position', [0.1 0.1 0.35 0.3]);
axes1 = axes('Parent', figure1);
box(axes1, 'on')
hold(axes1, 'on')
grid(axes1, 'on')
h(1) = plot(paretoArch2Old(:, 1),paretoArch2Old(:, 2), ':',...
    'displayname', 'upper bound', 'linewidth', 3, 'color', [0.93, 0.69, 0.13]);
h(2) = plot(paretoArch2Old(:, 3),paretoArch2Old(:, 4), '',...
    'displayname', 'heuristic', 'linewidth', 3, 'color', [0.93, 0.69, 0.13]);
h(3) = plot(paretoArch2Old(:, 1)*0.87,paretoArch2Old(:, 2)*0.87, ...
    '-.', 'displayname', '87% upper bound', 'linewidth', 3, 'color', [0.93, 0.69, 0.13]);

text(paretoArch2Old(1, 1),paretoArch2Old(1, 2),'\beta=0', ...
    'fontsize', 18, 'horizontalalignment', 'right',...
    'verticalalignment', 'top')
text(paretoArch2Old(end, 1),paretoArch2Old(end, 2),...
    '\beta=2000', 'fontsize', 18,'horizontalalignment', 'center',...
    'verticalalignment', 'top')
text(paretoArch2Old(11, 1)-25,paretoArch2Old(11, 2)-10,...
    '\beta=0.4', 'fontsize', 18,'horizontalalignment', 'right',...
    'verticalalignment', 'top', 'color', [0.47, 0.67, 0.19])
plot(paretoArch2Old(11, 1),paretoArch2Old(11, 2),'marker', 'o', ...
'linewidth', 3, 'markersize', 15, 'color', [0.47, 0.67, 0.19])
plot(paretoArch2Old(11, 3),paretoArch2Old(11, 4),'marker', 'o', ...
'linewidth', 3, 'markersize', 15, 'color', [0.47, 0.67, 0.19])

% annotation(figure1,'arrow',[0.8 0.73], [0.6 0.46]);

xlabel('Number of Connections', 'fontsize', 18)
ylabel('Throughput Tbps', 'fontsize', 18)
h = legend(h(1:3), 'location', 'southwest');
h.FontSize = 18;
set(axes1, 'linewidth', 1)
set(axes1, 'gridalpha', 0.5)
set(axes1, 'fontsize', 14)
saveas(figure1, 'paretoArch2OldForOFC.jpg')
