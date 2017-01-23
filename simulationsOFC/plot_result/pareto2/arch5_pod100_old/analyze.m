clc;
close all;
clear;

result = zeros(22, 10, 20);
result0 = zeros(size(result));
r = zeros(22,20);
for i=0:19
    newFileName = sprintf('result_pareto_arch5_old_pod100_%d.csv',i);
    result(:,:,i+1) = importPareto(newFileName);
    result0(:,:,i+1) = result(:,:,i+1);
    r(:,1+i) = result(:,9,i+1)./result(:,3,i+1)./result(:,1,i+1);
    for j=1:22
        if r(j,i+1)<1
            result0(j,9,i+1) = result(j,9,i+1)./result(j,1,i+1);
        end
    end
end
result = result0;

gap = [];
for i=1:20
    gap = [gap; result(:,10,i)./result(:,4,i)];
end
gapave = mean(gap); % average gap is 90.39%

resultAve = mean(result, 3);

load cnklistResult.mat
resultAve(:,9) = mean(thp,1)';
% resultAve(:,8) = mean(cnk,1)';

%%
figure1 = figure;
axes1 = axes('Parent', figure1);
box(axes1, 'on')
hold(axes1, 'on')
grid(axes1, 'on')
h(1) = plot(resultAve(:,2),resultAve(:,3)*0.001, 'displayname', 'optimal (\alpha=1)', 'linewidth', 2);
h(2) = plot(resultAve(:,8),resultAve(:,9)*0.001, 'displayname', 'heuristic', 'linewidth', 2);
h(3) = plot(resultAve(:,2)*0.82,resultAve(:,3)*0.001*0.82, '--', 'displayname', '82% of optimal', 'linewidth', 2);

paretoArch5Old(:,1) = resultAve(:,2);
paretoArch5Old(:,2) = resultAve(:,3)*0.001;
paretoArch5Old(:,3) = resultAve(:,8);
paretoArch5Old(:,4) = resultAve(:,9)*0.001;
save('paretoArch5Old.mat', 'paretoArch5Old')

% h(4) = plot(1159.5, 188.82, '+', 'linewidth', 2, 'markersize', 10);
% text(1159.5+15, 188.82, 'Ascending FF', 'fontsize', 12)
% 
% h(5) = plot(618.7, 260.54, '+', 'linewidth', 2, 'markersize', 10);
% text(618.7+15, 260.54, 'Descending FF', 'fontsize', 12)
% 
% h(6) = plot(969.55, 234.54, '+', 'linewidth', 2, 'markersize', 10);
% text(969.55-70, 234.54-5, 'SPSA', 'fontsize', 12);

text(resultAve(1,2),resultAve(1,3)*0.001,'\beta=0', 'fontsize', 12)
text(resultAve(end,2),resultAve(end,3)*0.001,'\beta=100', 'fontsize', 12,'horizontalalignment', 'right',...
    'verticalalignment', 'bottom')

xlabel('Number of Connections', 'fontsize', 16)
ylabel('Throughput Tbps', 'fontsize', 16)
h = legend(h(1:3), 'location', 'southwest');
h.FontSize = 12;
saveas(figure1, 'pareto_arch2.jpg')

%%
figure2 = figure;
axes2 = axes('parent', figure2);
% h(1) = semilogx(resultAve(:,1)+0.001, resultAve(:,3)*0.001, 'linewidth', 2, 'displayname', 'optimal (\alpha=1)');
% hold(axes2, 'on')
% h(2) = semilogx(resultAve(:,1)+0.001, resultAve(:,6)*0.001, 'linewidth', 2, 'displayname', 'heuristic');
% h(3) = semilogx(resultAve(:,1)+0.001, resultAve(:,3)*0.001*0.90, '--', 'linewidth', 2, 'displayname', '90% of optimal');

h(1) = semilogx(resultAve(:,1), resultAve(:,3)*0.001, 'linewidth', 2, 'displayname', 'optimal (\alpha=1)');
hold(axes2, 'on')
h(2) = semilogx(resultAve(:,1), resultAve(:,9)*0.001, 'linewidth', 2, 'displayname', 'heuristic');
% h(3) = semilogx(resultAve(:,1), resultAve(:,3)*0.001*0.87, '--', 'linewidth', 2, 'displayname', '87% of optimal');

box(axes2, 'on')
grid(axes2, 'on')
xlabel('\beta', 'fontsize', 16)
ylabel('Throughput Tbps', 'fontsize', 16)
h = legend(h(1:2), 'location', 'southeast');
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