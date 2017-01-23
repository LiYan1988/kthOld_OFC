clc;
close all;
clear;
% optimality gaps of FF ascending and descending for different architecture
% and number of PODs

%%
% plot optimization gap for arch2 FF forward against connection
% optimization
arch2_cnkopt_aff_cnk = 1146.5;
arch2_cnkopt_aff_thp = 183400;
arch2_cnkopt_opt_cnk = 1205.6;
arch2_cnkopt_opt_thp = 213638.7;

arch4_cnkopt_aff_cnk = 926;
arch4_cnkopt_aff_thp = 111870;
arch4_cnkopt_opt_cnk = 953;
arch4_cnkopt_opt_thp = 127427.5;

arch5_cnkopt_aff_cnk = 1159.5;
arch5_cnkopt_aff_thp = 188820;
arch5_cnkopt_opt_cnk = 1300.3;
arch5_cnkopt_opt_thp = 248123.7;

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
saveas(figure1, 'pod100_cnkopt_cnk.jpg')

%%
arch2_thpopt_dff_cnk = 617.8;
arch2_thpopt_dff_thp = 260348.7;
arch2_thpopt_opt_cnk = 626.3;
arch2_thpopt_opt_thp = 272377.5;

arch4_thpopt_dff_cnk = 347.5;
arch4_thpopt_dff_thp = 230967.5;
arch4_thpopt_opt_cnk = 343.0;
arch4_thpopt_opt_thp = 236568.8;

arch5_thpopt_dff_cnk = 618.7;
arch5_thpopt_dff_thp = 260539.8;
arch5_thpopt_opt_cnk = 497.1;
arch5_thpopt_opt_thp = 280682.5;

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
saveas(figure2, 'pod100_thpopt_thp.jpg')
