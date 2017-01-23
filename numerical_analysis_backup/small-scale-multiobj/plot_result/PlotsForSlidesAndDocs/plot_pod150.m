clc;
close all;
clear;
% optimality gaps of FF ascending and descending for different architecture
% and number of PODs

%%
% plot optimization gap for arch2 FF forward against connection
% optimization
arch2_cnkopt_aff_cnk = 2222.65;
arch2_cnkopt_aff_thp = 271987.5;
arch2_cnkopt_opt_cnk = 2298.7;
arch2_cnkopt_opt_thp = 308841.3;

arch4_cnkopt_aff_cnk = 1675.4;
arch4_cnkopt_aff_thp = 146472.5;
arch4_cnkopt_opt_cnk = 1647.7;
arch4_cnkopt_opt_thp = 157817.5;

arch5_cnkopt_aff_cnk = 2244.6;
arch5_cnkopt_aff_thp = 279237.5;
arch5_cnkopt_opt_cnk = 2502.5;
arch5_cnkopt_opt_thp = 373092.5;

y = [[arch2_cnkopt_aff_cnk, arch2_cnkopt_opt_cnk];...
    [arch4_cnkopt_aff_cnk, arch4_cnkopt_opt_cnk];...
    [arch5_cnkopt_aff_cnk, arch5_cnkopt_opt_cnk]];

figure1 = figure;
axes1 = axes('Parent', figure1);
hold(axes1, 'on');
box(axes1, 'on');
grid(axes1, 'on');
set(axes1, 'xtick', [1, 2, 3]);
set(axes1, 'xticklabel', ['Arch2'; 'Arch4'; 'Arch5']);
% xlabel('\beta', 'fontsize', 12)
ylabel('Number of connections', 'fontsize', 12)
bar1 = bar(y);
bar1(1).FaceColor = [0.85, 0.33, 0.1];
bar1(2).FaceColor = [0, 0.45, 0.74];
set(bar1(1), 'displayname', 'Heuristic')
set(bar1(2), 'displayname', 'MILP')
h = legend(axes1, 'show', 'location', 'southwest');
h.FontSize = 12;
title('Connection optimization')
saveas(figure1, 'pod150_cnkopt_cnk.jpg')

%%
arch2_thpopt_dff_cnk = 9.163000000000000e+02;
arch2_thpopt_dff_thp = 405475;
arch2_thpopt_opt_cnk = 9.183000000000000e+02;
arch2_thpopt_opt_thp = 4.181762500000000e+05;

arch4_thpopt_dff_cnk = 4.896500000000000e+02;
arch4_thpopt_dff_thp = 3.625762500000000e+05;
arch4_thpopt_opt_cnk = 4.651000000000000e+02;
arch4_thpopt_opt_thp = 3.650162500000000e+05;

arch5_thpopt_dff_cnk = 9.169500000000000e+02;
arch5_thpopt_dff_thp = 405680;
arch5_thpopt_opt_cnk = 6.477000000000000e+02;
arch5_thpopt_opt_thp = 4.210037500000000e+05;

y = [[arch2_thpopt_dff_thp, arch2_thpopt_opt_thp];...
    [arch4_thpopt_dff_thp, arch4_thpopt_opt_thp];...
    [arch5_thpopt_dff_thp, arch5_thpopt_opt_thp]]/1000;

figure2 = figure;
axes2 = axes('Parent', figure2);
hold(axes2, 'on');
box(axes2, 'on');
grid(axes2, 'on');
set(axes2, 'xtick', [1, 2, 3]);
set(axes2, 'xticklabel', ['Arch2'; 'Arch4'; 'Arch5']);
% xlabel('\beta', 'fontsize', 12)
ylabel('Throughput (Tbps)', 'fontsize', 12)
bar2 = bar(y);
bar2(1).FaceColor = [0.85, 0.33, 0.1];
bar2(2).FaceColor = [0, 0.45, 0.74];
set(bar2(1), 'displayname', 'Heuristic')
set(bar2(2), 'displayname', 'MILP')
h = legend(axes2, 'show', 'location', 'southwest');
h.FontSize = 12;
title('Throughput optimization')
saveas(figure2, 'pod150_thpopt_thp.jpg')
