clc;
close all;
clear;
% optimality gaps of FF ascending and descending for different architecture
% and number of PODs

%% arch2 connection 
% arch2_cnkopt_aff_cnk100 = 1146.5;
% arch2_cnkopt_opt_cnk100 = 1205.6;
% 
% arch2_cnkopt_aff_cnk150 = 2222.65;
% arch2_cnkopt_opt_cnk150 = 2298.7;
% 
% arch2_cnkopt_aff_cnk200 = 3.483600000000000e+03;
% arch2_cnkopt_opt_cnk200 = 3.513450000000000e+03;
% 
% y = [[arch2_cnkopt_aff_cnk100, arch2_cnkopt_opt_cnk100];...
%     [arch2_cnkopt_aff_cnk150, arch2_cnkopt_opt_cnk150];...
%     [arch2_cnkopt_aff_cnk200, arch2_cnkopt_opt_cnk200]];
% 
% figure1 = figure('units','normalized','Position', [0.1 0.1 0.35 0.3]);
% axes1 = axes('Parent', figure1);
% hold(axes1, 'on');
% box(axes1, 'on');
% grid(axes1, 'on');
% set(axes1, 'xtick', [1, 2, 3]);
% set(axes1, 'xticklabel', ['100'; '150'; '200']);
% % ytick = get(axes1, 'ytick');
% % set(axes1, 'yticklabel', ytick(1:2:end))
% xlabel('Number of PODs', 'fontsize', 12)
% ylabel('Number of connections', 'fontsize', 12)
% bar1 = bar(y);
% bar1(1).FaceColor = [0.85, 0.33, 0.1];
% bar1(2).FaceColor = [0, 0.45, 0.74];
% set(bar1(1), 'displayname', 'Heuristic')
% set(bar1(2), 'displayname', 'MILP')
% h = legend(axes1, 'show', 'location', 'northwest');
% h.FontSize = 12;
% % pbaspect([3 1 1])
% % title('Connection optimization')
% % saveas(figure1, 'pod100_cnkopt_cnk.jpg')

%% arch4 connection 
% arch4_cnkopt_aff_cnk100 = 926;
% arch4_cnkopt_opt_cnk100 = 953;
% 
% arch4_cnkopt_aff_cnk150 = 1675.4;
% arch4_cnkopt_opt_cnk150 = 1647.7;
% 
% arch4_cnkopt_aff_cnk200 = 2.49040e+03;
% arch4_cnkopt_opt_cnk200 = 2.52615e+03;
% 
% y = [[arch4_cnkopt_aff_cnk100, arch4_cnkopt_opt_cnk100];...
%     [arch4_cnkopt_aff_cnk150, arch4_cnkopt_opt_cnk150];...
%     [arch4_cnkopt_aff_cnk200, arch4_cnkopt_opt_cnk200]];
% 
% figure1 = figure;
% axes1 = axes('Parent', figure1);
% hold(axes1, 'on');
% box(axes1, 'on');
% grid(axes1, 'on');
% set(axes1, 'xtick', [1, 2, 3]);
% set(axes1, 'xticklabel', ['100'; '150'; '200']);
% % xlabel('\beta', 'fontsize', 12)
% ylabel('Number of connections', 'fontsize', 12)
% bar1 = bar(y);
% bar1(1).FaceColor = [0.85, 0.33, 0.1];
% bar1(2).FaceColor = [0, 0.45, 0.74];
% set(bar1(1), 'displayname', 'Heuristic')
% set(bar1(2), 'displayname', 'MILP')
% h = legend(axes1, 'show', 'location', 'northwest');
% h.FontSize = 12;
% % title('Connection optimization')
% % saveas(figure1, 'pod100_cnkopt_cnk.jpg')

%% arch5 connection 
% arch5_cnkopt_aff_cnk100 = 1159.5;
% arch5_cnkopt_opt_cnk100 = 1300.3;
% 
% arch5_cnkopt_aff_cnk150 = 2244.6;
% arch5_cnkopt_opt_cnk150 = 2502.5;
% 
% arch5_cnkopt_aff_cnk200 = 3.5121e+03;
% arch5_cnkopt_opt_cnk200 = 3.9062e+03;
% 
% y = [[arch5_cnkopt_aff_cnk100, arch5_cnkopt_opt_cnk100];...
%     [arch5_cnkopt_aff_cnk150, arch5_cnkopt_opt_cnk150];...
%     [arch5_cnkopt_aff_cnk200, arch5_cnkopt_opt_cnk200]];
% 
% figure1 = figure;
% axes1 = axes('Parent', figure1);
% hold(axes1, 'on');
% box(axes1, 'on');
% grid(axes1, 'on');
% set(axes1, 'xtick', [1, 2, 3]);
% set(axes1, 'xticklabel', ['100'; '150'; '200']);
% % xlabel('\beta', 'fontsize', 12)
% ylabel('Number of connections', 'fontsize', 12)
% bar1 = bar(y);
% bar1(1).FaceColor = [0.85, 0.33, 0.1];
% bar1(2).FaceColor = [0, 0.45, 0.74];
% set(bar1(1), 'displayname', 'Heuristic')
% set(bar1(2), 'displayname', 'MILP')
% h = legend(axes1, 'show', 'location', 'northwest');
% h.FontSize = 12;
% % title('Connection optimization')
% % saveas(figure1, 'pod100_cnkopt_cnk.jpg')

%% Plot all
arch2_cnkopt_aff_cnk100 = 1146.5;
arch2_cnkopt_opt_cnk100 = 1205.6;

arch2_cnkopt_aff_cnk150 = 2222.65;
arch2_cnkopt_opt_cnk150 = 2298.7;

arch2_cnkopt_aff_cnk200 = 3.483600000000000e+03;
arch2_cnkopt_opt_cnk200 = 3.513450000000000e+03;

y1 = [[arch2_cnkopt_aff_cnk100, arch2_cnkopt_opt_cnk100];...
    [arch2_cnkopt_aff_cnk150, arch2_cnkopt_opt_cnk150];...
    [arch2_cnkopt_aff_cnk200, arch2_cnkopt_opt_cnk200]];

arch4_cnkopt_aff_cnk100 = 926;
arch4_cnkopt_opt_cnk100 = 953;

arch4_cnkopt_aff_cnk150 = 1647.4;
arch4_cnkopt_opt_cnk150 = 1675.7;

arch4_cnkopt_aff_cnk200 = 2.49040e+03;
arch4_cnkopt_opt_cnk200 = 2.52615e+03;

y2 = [[arch4_cnkopt_aff_cnk100, arch4_cnkopt_opt_cnk100];...
    [arch4_cnkopt_aff_cnk150, arch4_cnkopt_opt_cnk150];...
    [arch4_cnkopt_aff_cnk200, arch4_cnkopt_opt_cnk200]];


arch5_cnkopt_aff_cnk100 = 1159.5;
arch5_cnkopt_opt_cnk100 = 1300.3;

arch5_cnkopt_aff_cnk150 = 2244.6;
arch5_cnkopt_opt_cnk150 = 2502.5;

arch5_cnkopt_aff_cnk200 = 3.5121e+03;
arch5_cnkopt_opt_cnk200 = 3.9062e+03;

y3 = [[arch5_cnkopt_aff_cnk100, arch5_cnkopt_opt_cnk100];...
    [arch5_cnkopt_aff_cnk150, arch5_cnkopt_opt_cnk150];...
    [arch5_cnkopt_aff_cnk200, arch5_cnkopt_opt_cnk200]];

y = [y1, y2, y3];

figure1 = figure('units','normalized','Position', [0.1 0.1 0.35 0.3]);
axes1 = axes('Parent', figure1);
hold(axes1, 'on');
box(axes1, 'on');
grid(axes1, 'on');
set(axes1, 'xtick', [1, 2, 3]);
set(axes1, 'xticklabel', ['100'; '150'; '200']);
% xlabel('\beta', 'fontsize', 12)
ylabel('Number of connections', 'fontsize', 12)
bar1 = bar(y);
bar1(1).FaceColor = [0 0.45 0.74];
bar1(2).FaceColor = [0 0.45 0.74];
bar1(2).LineStyle = '--';

bar1(3).FaceColor = [0.85 0.33 0.01];
bar1(4).FaceColor = [0.85 0.33 0.01];
bar1(4).LineStyle = '--';

bar1(5).FaceColor = [0.93 0.69 0.13];
bar1(6).FaceColor = [0.93 0.69 0.13];
bar1(6).LineStyle = '--';

for i=1:6
    bar1(i).LineWidth = 1.5;
end
set(bar1(1), 'displayname', 'Arch 2 Heuristic')
set(bar1(2), 'displayname', 'Arch 2 MILP')
set(bar1(3), 'displayname', 'Arch 3 Heuristic')
set(bar1(4), 'displayname', 'Arch 3 MILP')
set(bar1(5), 'displayname', 'Arch 4 Heuristic')
set(bar1(6), 'displayname', 'Arch 4 MILP')
h = legend(axes1, 'show', 'location', 'southeast');
h.FontSize = 12;
xlabel('Number of PODs')
saveas(figure1, 'cnkAll.jpg')