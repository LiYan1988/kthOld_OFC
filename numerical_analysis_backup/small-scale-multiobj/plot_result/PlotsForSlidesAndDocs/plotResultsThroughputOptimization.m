clc;
close all;
clear;
% optimality gaps of FF ascending and descending for different architecture
% and number of PODs

%% Plot all
arch2_thpopt_dff_thp100 = 260348.7;
arch2_thpopt_opt_thp100 = 272377.5;

arch2_thpopt_dff_thp150 = 405475;
arch2_thpopt_opt_thp150 = 4.1817e+05;

arch2_thpopt_dff_thp200 = 546035;
arch2_thpopt_opt_thp200 = 5.59983e+05;

y1 = [[arch2_thpopt_dff_thp100, arch2_thpopt_opt_thp100];...
    [arch2_thpopt_dff_thp150, arch2_thpopt_opt_thp150];...
    [arch2_thpopt_dff_thp200, arch2_thpopt_opt_thp200]];

arch4_thpopt_dff_thp100 = 230967.5;
arch4_thpopt_opt_thp100 = 236568.8;

arch4_thpopt_dff_thp150 = 3.6257e+05;
arch4_thpopt_opt_thp150 = 3.6501e+05;

arch4_thpopt_dff_thp200 = 4.922862e+05;
arch4_thpopt_opt_thp200 = 501945;

y2 = [[arch4_thpopt_dff_thp100 , arch4_thpopt_opt_thp100];...
    [arch4_thpopt_dff_thp150, arch4_thpopt_opt_thp150];...
    [arch4_thpopt_dff_thp200, arch4_thpopt_opt_thp200]];


arch5_thpopt_dff_thp100 = 260539.8;
arch5_thpopt_opt_thp100 = 280682.5;

arch5_thpopt_dff_thp150 = 405680;
arch5_thpopt_opt_thp150 = 4.2100e+05;

arch5_thpopt_dff_thp200 = 546225;
arch5_thpopt_opt_thp200 = 559915;

y3 = [[arch5_thpopt_dff_thp100, arch5_thpopt_opt_thp100];...
    [arch5_thpopt_dff_thp150, arch5_thpopt_opt_thp150];...
    [arch5_thpopt_dff_thp200, arch5_thpopt_opt_thp200]];

y = [y1, y2, y3]/1000;

figure1 = figure('units','normalized','Position', [0.1 0.1 0.35 0.3]);
axes1 = axes('Parent', figure1);
hold(axes1, 'on');
box(axes1, 'on');
grid(axes1, 'on');
set(axes1, 'xtick', [1, 2, 3]);
set(axes1, 'xticklabel', ['100'; '150'; '200']);
% xlabel('\beta', 'fontsize', 12)
ylabel('Throughput (THz)', 'fontsize', 12)
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
set(bar1(1), 'displayname', 'A1 Heuristic')
set(bar1(2), 'displayname', 'A1 MILP')
set(bar1(3), 'displayname', 'A2 Heuristic')
set(bar1(4), 'displayname', 'A2 MILP')
set(bar1(5), 'displayname', 'A3 Heuristic')
set(bar1(6), 'displayname', 'A3 MILP')
h = legend(axes1, 'show', 'location', 'southeast');
h.FontSize = 12;
xlabel('Number of PODs')
saveas(figure1, 'thpAll.jpg')