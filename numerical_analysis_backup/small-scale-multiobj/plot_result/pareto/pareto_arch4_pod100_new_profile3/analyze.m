clc;
close all;
clear;

resultSmallBeta = zeros(49, 7, 20);
for i=0:19
    filename = sprintf('result_pareto_arch4_pod100_nf_%d.csv',i);
    resultSmallBeta(:,:,i+1) = importfile_pareto(filename);
end

resultBigBeta = zeros(size(resultSmallBeta));
for i=0:19
    filename = sprintf('1_result_pareto_arch4_pod100_nf_%d.csv',i);
    resultBigBeta(:,:,i+1) = importfile_pareto(filename);
end

gapSmallBeta = [];
for i=1:20
    gapSmallBeta = [gapSmallBeta; resultSmallBeta(:,7,i)./resultSmallBeta(:,4,i)];
end
gapSmallBetaAve = mean(gapSmallBeta); 

gapBigBeta = [];
for i=1:20
    gapBigBeta = [gapBigBeta; resultBigBeta(:,7,i)./resultBigBeta(:,4,i)];
end
gapBigBetaAve = mean(gapBigBeta); 

% resultSmallBetaAve = mean(resultSmallBeta, 3);
% resultBigBetaAve = mean(resultBigBeta, 3);
resultSmallBetaAve = zeros(49, 7);
for i=1:49
    tmp = zeros(1,7);
    cnt = 0;
    for j = 1:20
        if resultSmallBeta(i,end,j)~=0
            tmp = tmp + resultSmallBeta(i,:,j);
            cnt = cnt+1;
        end
        resultSmallBetaAve(i,:) = tmp/cnt;
    end
end

resultBigBetaAve = zeros(49, 7);
for i=1:49
    tmp = zeros(1,7);
    cnt = 0;
    for j = 1:20
        if resultBigBeta(i,end,j)~=0
            tmp = tmp + resultBigBeta(i,:,j);
            cnt = cnt+1;
        end
        resultBigBetaAve(i,:) = tmp/cnt;
    end
end

resultAve = [resultBigBetaAve(1, :); resultSmallBetaAve; resultBigBetaAve(2:end, :)];
% resultAve(:,2) = smooth(resultAve(:,1), resultAve(:,2), 11)*0.93;
% resultAve(:,3) = smooth(resultAve(:,1), resultAve(:,3), 11)*0.93;
% resultAve(:,4) = smooth(resultAve(:,1), resultAve(:,4), 11);
% resultAve(:,5) = smooth(resultAve(:,1), resultAve(:,5), 11);
% resultAve(:,6) = smooth(resultAve(:,1), resultAve(:,6), 11);
% resultAve(:,7) = smooth(resultAve(:,1), resultAve(:,7), 11);
% resultAve(1,1) = resultAve(2,1)/10; 
%%
figure1 = figure;
axes1 = axes('Parent', figure1);
box(axes1, 'on')
hold(axes1, 'on')
grid(axes1, 'on')
h(1) = plot(resultAve(1:end-28,2),resultAve(1:end-28,3)*0.001, 'displayname', 'optimal (\alpha=1)', 'linewidth', 2);
h(2) = plot(resultAve(1:end-28,5),resultAve(1:end-28,6)*0.001, 'displayname', 'heuristic', 'linewidth', 2);
h(3) = plot(resultAve(1:end-28,2)*0.90,resultAve(1:end-28,3)*0.001*0.90, '--', 'displayname', '90% of optimal', 'linewidth', 2);

paretoArch4New(:,1) = resultAve(1:end-28,2)/0.93;
paretoArch4New(:,2) = resultAve(1:end-28,3)*0.001/0.93;
paretoArch4New(:,3) = resultAve(1:end-28,5);
paretoArch4New(:,4) = resultAve(1:end-28,6)*0.001;
save('paretoArch4New.mat', 'paretoArch4New')

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
h = legend(h(1:3), 'location', 'west');
h.FontSize = 12;
saveas(figure1, 'pareto_arch2.jpg')

%%
figure2 = figure;
axes2 = axes('parent', figure2);
betam = min(resultAve(:,1));

h(1) = semilogx(resultAve(:,1)+betam, resultAve(:,3)*0.001, 'linewidth', 2, 'displayname', 'optimal (\alpha=1)');
hold(axes2, 'on')
h(2) = semilogx(resultAve(:,1)+betam, resultAve(:,6)*0.001, 'linewidth', 2, 'displayname', 'heuristic');
h(3) = semilogx(resultAve(:,1)+betam, resultAve(:,3)*0.001*0.9, '--', 'linewidth', 2, 'displayname', '90% of optimal');
box(axes2, 'on')
grid(axes2, 'on')
xlabel('\beta', 'fontsize', 16)
ylabel('Throughput Tbps', 'fontsize', 16)
h = legend(h(1:3), 'location', 'east');
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