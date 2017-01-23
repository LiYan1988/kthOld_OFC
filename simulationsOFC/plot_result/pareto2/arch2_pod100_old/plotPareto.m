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

%%
figure1 = figure('units','normalized','Position', [0.1 0.1 0.35 0.3]);
axes1 = axes('Parent', figure1);
box(axes1, 'on')
hold(axes1, 'on')
grid(axes1, 'on')
h(1) = plot(resultAve(:,2),resultAve(:,3)*0.001, 'displayname', 'upper bound', 'linewidth', 2);
h(2) = plot(paretoArch2Old(:,3),paretoArch2Old(:,4), 'displayname', 'heuristic', 'linewidth', 2);
h(3) = plot(resultAve(:,2)*0.87,resultAve(:,3)*0.001*0.87, '--', 'displayname', '87% upper bound', 'linewidth', 2);

text(resultAve(1,2),resultAve(1,3)*0.001,'\beta=0', 'fontsize', 12)
text(resultAve(end,2),resultAve(end,3)*0.001,'\beta=100', 'fontsize', 12,'horizontalalignment', 'right',...
    'verticalalignment', 'bottom')

xlabel('Number of Connections', 'fontsize', 16)
ylabel('Throughput Tbps', 'fontsize', 16)
h = legend(h(1:3), 'location', 'southwest');
h.FontSize = 12;
saveas(figure1, 'pareto_arch2.jpg')

%%
figure2 = figure('units','normalized','Position', [0.1 0.1 0.35 0.3]);
axes2 = axes('parent', figure2);

h(1) = semilogx(resultAve(:,1), resultAve(:,3)*0.001, 'linewidth', 2, 'displayname', 'upper bound');
hold(axes2, 'on')
h(2) = semilogx(resultAve(:,1), resultAve(:,9)*0.001, 'linewidth', 2, 'displayname', 'heuristic');

box(axes2, 'on')
grid(axes2, 'on')
xlabel('\beta', 'fontsize', 16)
ylabel('Throughput Tbps', 'fontsize', 16)
h = legend(h(1:2), 'location', 'southeast');
h.FontSize = 12;
saveas(figure2, 'connectionsVsBeta.jpg')
