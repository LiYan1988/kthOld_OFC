clc;
close all;
clear;

result = zeros(49, 7, 20);
for i=0:19
    filename = sprintf('result_pareto_arch2_nf_pod100_%d.csv',i);
    result(:,:,i+1) = importfile_pareto(filename);
end

gap = [];
for i=1:20
    gap = [gap; result(:,7,i)./result(:,4,i)];
end
gapave = mean(gap); % average gap is 88.25%

resultAve = mean(result, 3);
resultAve(23,:) = []; % a wrong result

%%
figure1 = figure;
axes1 = axes('Parent', figure1);
box(axes1, 'on')
hold(axes1, 'on')
grid(axes1, 'on')
h(1) = plot(resultAve(:,2),resultAve(:,3)*0.001, 'displayname', 'optimal (\alpha=1)', 'linewidth', 2);
h(2) = plot(resultAve(:,5),resultAve(:,6)*0.001, 'displayname', 'heuristic', 'linewidth', 2);
h(3) = plot(resultAve(:,2)*0.88,resultAve(:,3)*0.001*0.88, '--', 'displayname', '88% of optimal', 'linewidth', 2);

text(resultAve(1,2),resultAve(1,3)*0.001,'\beta=0', 'fontsize', 12)
text(resultAve(end,2),resultAve(end,3)*0.001-5,'\beta=100', 'fontsize', 12,'horizontalalignment', 'left')

xlabel('Number of Connections', 'fontsize', 16)
ylabel('Throughput Tbps', 'fontsize', 16)
legend(h(1:3), 'location', 'best')

saveas(figure1, 'pareto_arch2.jpg')

%%
figure2 = figure;
axes2 = axes('parent', figure2);
h(1) = semilogx(resultAve(:,1), resultAve(:,3)*0.001, 'linewidth', 2, 'displayname', 'optimal (\alpha=1)');
hold(axes2, 'on')
h(2) = semilogx(resultAve(:,1), resultAve(:,6)*0.001, 'linewidth', 2, 'displayname', 'heuristic');
box(axes2, 'on')
grid(axes2, 'on')
xlabel('\beta', 'fontsize', 16)
ylabel('Throughput Tbps', 'fontsize', 16)
h = legend(h(1:2), 'location', 'best');
h.FontSize = 12;
saveas(figure2, 'connectionsVsBeta.jpg')

% axes3 = axes('position', axes2.Position);
% semilogx(resultAve(:,1), resultAve(:,2), 'linewidth', 2, 'parent', axes3)
% hold(axes3, 'on')
% semilogx(resultAve(:,1), resultAve(:,5), 'linewidth', 2, 'parent', axes3)
% axes3.YAxisLocation = 'right';
% axes3.Color = 'none';
% box(axes3, 'on')
% grid(axes3, 'on')
% xlabel('\beta', 'fontsize', 16)
% ylabel('Number of connections', 'fontsize', 16)
% saveas(figure3, 'connectionsVsBeta.jpg')