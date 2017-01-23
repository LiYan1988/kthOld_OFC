% POD 150, the hybrid points are very strange, because hybrid is not
% optimized?

clc;
clear;
close all;

%% Import data
% import benchmark data
fileName1 = 'pod150_benchmark.csv';
[Arch2_FF_fwd_cnk,Arch2_FF_fwd_thp,...
 Arch2_FF_bwd_cnk,Arch2_FF_bwd_thp,...
 Arch2_AJ_fwd_cnk,Arch2_AJ_fwd_thp,...
 Arch2_AJ_bwd_cnk,Arch2_AJ_bwd_thp,...
 Arch4_FF_fwd_cnk,Arch4_FF_fwd_thp,...
 Arch4_FF_bwd_cnk,Arch4_FF_bwd_thp,...
 Arch4_AJ_fwd_cnk,Arch4_AJ_fwd_thp,...
 Arch4_AJ_bwd_cnk,Arch4_AJ_bwd_thp,...
 Arch5_FF_fwd_cnk,Arch5_FF_fwd_thp,...
 Arch5_FF_bwd_cnk,Arch5_FF_bwd_thp,...
 Arch5_AJ_fwd_cnk,Arch5_AJ_fwd_thp,...
 Arch5_AJ_bwd_cnk,Arch5_AJ_bwd_thp] = ...
 importfile_benchmark_vectors(fileName1);

% import MILP data
% connections
fileName1 = 'pod150_connections.csv';
[id,arch4_cnkopt_lb_cnk,arch4_cnkopt_ub_cnk,...
    arch4_cnkopt_lb_thp,arch4_cnkopt_ub_thp,...
    arch1_cnkopt_cnk,arch1_cnkopt_thp,...
    arch2_cnkopt_lb_cnk,arch2_cnkopt_ub_cnk,...
    arch2_cnkopt_lb_thp,arch2_cnkopt_ub_thp,...
    arch5_cnkopt_lb_cnk,arch5_cnkopt_ub_cnk,...
    arch5_cnkopt_lb_thp,arch5_cnkopt_ub_thp,total_cnk] = ...
    importfile_optimizations_vectors(fileName1);

% throughput
fileName1 = 'pod150_throughput.csv';
[id,arch4_thpopt_lb_cnk,arch4_thpopt_ub_cnk,...
    arch4_thpopt_lb_thp,arch4_thpopt_ub_thp,...
    arch1_thpopt_cnk,arch1_thpopt_thp,...
    arch2_thpopt_lb_cnk,arch2_thpopt_ub_cnk,...
    arch2_thpopt_lb_thp,arch2_thpopt_ub_thp,...
    arch5_thpopt_lb_cnk,arch5_thpopt_ub_cnk,...
    arch5_thpopt_lb_thp,arch5_thpopt_ub_thp,total_cnk] = ...
    importfile_optimizations_vectors(fileName1);

% hybrid
fileName1 = 'pod150_hybrid.csv';
[id,arch4_hybopt_lb_cnk,arch4_hybopt_ub_cnk,...
    arch4_hybopt_lb_thp,arch4_hybopt_ub_thp,...
    arch1_hybopt_cnk,arch1_hybopt_thp,...
    arch2_hybopt_lb_cnk,arch2_hybopt_ub_cnk,...
    arch2_hybopt_lb_thp,arch2_hybopt_ub_thp,...
    arch5_hybopt_lb_cnk,arch5_hybopt_ub_cnk,...
    arch5_hybopt_lb_thp,arch5_hybopt_ub_thp,total_cnk] = ...
    importfile_optimizations_vectors(fileName1);

%% plot scatter for architecture 2
% Show the trade-off of different objectives 
arch2_cnkopt = [mean(arch2_cnkopt_ub_cnk), mean(arch2_cnkopt_ub_thp)];
arch2_thpopt = [mean(arch2_thpopt_ub_cnk), mean(arch2_thpopt_ub_thp)];
% arch2_hybopt = [mean(arch2_hybopt_ub_cnk+arch2_hybopt_lb_cnk)/2, mean(arch2_hybopt_ub_thp+arch2_hybopt_lb_thp)/2];
arch2_hybopt = [mean(arch2_hybopt_ub_cnk), mean(arch2_hybopt_ub_thp)];
arch2_FF_fwd = [mean(Arch2_FF_fwd_cnk), mean(Arch2_FF_fwd_thp)];
arch2_FF_bwd = [mean(Arch2_FF_bwd_cnk),mean(Arch2_FF_bwd_thp)];
arch2_AJ = [mean(Arch2_AJ_bwd_cnk),mean(Arch2_AJ_bwd_thp)];

figure1 = figure; 
axes1 = axes('Parent', figure1);
box(axes1, 'on')
hold(axes1, 'on')
grid(axes1, 'on')
title('Architecture 2')
xlabel('Number of connection')
ylabel('Throughput Gbps')
plot(arch2_cnkopt(1), arch2_cnkopt(2)*0.001, 'o', 'linewidth', 2)
text(arch2_cnkopt(1)-220, arch2_cnkopt(2)*0.001, 'MILP Connection', 'fontsize', 14)

plot(arch2_thpopt(1), arch2_thpopt(2)*0.001, 'o', 'linewidth', 2)
text(arch2_thpopt(1)+10, arch2_thpopt(2)*0.001, 'MILP Throughput', 'fontsize', 14)

plot(arch2_hybopt(1), arch2_hybopt(2)*0.001, 'o', 'linewidth', 2)
text(arch2_hybopt(1)-180, arch2_hybopt(2)*0.001, 'MILP Hybrid', 'fontsize', 14)

plot(arch2_FF_fwd(1), arch2_FF_fwd(2)*0.001, 'o', 'linewidth', 2)
text(arch2_FF_fwd(1)+10, arch2_FF_fwd(2)*0.001, 'Ascending FF', 'fontsize', 14)

plot(arch2_FF_bwd(1), arch2_FF_bwd(2)*0.001, 'o', 'linewidth', 2)
text(arch2_FF_bwd(1)+10, arch2_FF_bwd(2)*0.001, 'Descending FF', 'fontsize', 14)

plot(arch2_AJ(1), arch2_AJ(2)*0.001, 'o', 'linewidth', 2)
text(arch2_AJ(1)+10, arch2_AJ(2)*0.001, 'SPSA', 'fontsize', 14)

figure_size = get(figure1, 'position');
set(figure1, 'position', figure_size*2);
saveas(figure1, 'arch2_pod100_scatter.jpg')

% Conclusion:
% 1. Hybrid optimization results are not good, longer running time

%% plot scatter for architecture 4
% Show the trade-off of different objectives 
arch4_cnkopt = [mean(arch4_cnkopt_ub_cnk), mean(arch4_cnkopt_ub_thp)];
arch4_thpopt = [mean(arch4_thpopt_ub_cnk), mean(arch4_thpopt_ub_thp)];
% arch2_hybopt = [mean(arch2_hybopt_ub_cnk+arch2_hybopt_lb_cnk)/2, mean(arch2_hybopt_ub_thp+arch2_hybopt_lb_thp)/2];
arch4_hybopt = [mean(arch4_hybopt_ub_cnk), mean(arch4_hybopt_ub_thp)];
arch4_FF_fwd = [mean(Arch4_FF_fwd_cnk), mean(Arch4_FF_fwd_thp)];
arch4_FF_bwd = [mean(Arch4_FF_bwd_cnk),mean(Arch4_FF_bwd_thp)];
arch4_AJ = [mean(Arch4_AJ_bwd_cnk),mean(Arch4_AJ_bwd_thp)];

figure1 = figure; 
axes1 = axes('Parent', figure1);
box(axes1, 'on')
hold(axes1, 'on')
grid(axes1, 'on')
title('Architecture 4')
xlabel('Number of connection')
ylabel('Throughput Gbps')
plot(arch4_cnkopt(1), arch4_cnkopt(2)*0.001, 'o', 'linewidth', 2)
text(arch4_cnkopt(1)-220, arch4_cnkopt(2)*0.001, 'MILP Connection', 'fontsize', 14)

plot(arch4_thpopt(1), arch4_thpopt(2)*0.001, 'o', 'linewidth', 2)
text(arch4_thpopt(1)+10, arch4_thpopt(2)*0.001, 'MILP Throughput', 'fontsize', 14)

plot(arch4_hybopt(1), arch4_hybopt(2)*0.001, 'o', 'linewidth', 2)
text(arch4_hybopt(1)+10, arch4_hybopt(2)*0.001, 'MILP Hybrid', 'fontsize', 14)

plot(arch4_FF_fwd(1), arch4_FF_fwd(2)*0.001, 'o', 'linewidth', 2)
text(arch4_FF_fwd(1)+10, arch4_FF_fwd(2)*0.001, 'Ascending FF', 'fontsize', 14)

plot(arch4_FF_bwd(1), arch4_FF_bwd(2)*0.001, 'o', 'linewidth', 2)
text(arch4_FF_bwd(1)+10, arch4_FF_bwd(2)*0.001, 'Descending FF', 'fontsize', 14)

plot(arch4_AJ(1), arch4_AJ(2)*0.001, 'o', 'linewidth', 2)
text(arch4_AJ(1)+10, arch4_AJ(2)*0.001, 'SPSA', 'fontsize', 14)

figure_size = get(figure1, 'position');
set(figure1, 'position', figure_size*2);
saveas(figure1, 'arch4_pod100_scatter.jpg')
% Conclusion:
% 1. Hybrid optimization results are not good, longer running time

%% plot scatter for architecture 5
% Show the trade-off of different objectives 
arch5_cnkopt = [mean(arch5_cnkopt_ub_cnk), mean(arch5_cnkopt_ub_thp)];
arch5_thpopt = [mean(arch5_thpopt_ub_cnk), mean(arch5_thpopt_ub_thp)];
% arch2_hybopt = [mean(arch2_hybopt_ub_cnk+arch2_hybopt_lb_cnk)/2, mean(arch2_hybopt_ub_thp+arch2_hybopt_lb_thp)/2];
arch5_hybopt = [mean(arch5_hybopt_ub_cnk), mean(arch5_hybopt_ub_thp)];
arch5_FF_fwd = [mean(Arch5_FF_fwd_cnk), mean(Arch5_FF_fwd_thp)];
arch5_FF_bwd = [mean(Arch5_FF_bwd_cnk),mean(Arch5_FF_bwd_thp)];
arch5_AJ = [mean(Arch5_AJ_bwd_cnk),mean(Arch5_AJ_bwd_thp)];

figure1 = figure; 
axes1 = axes('Parent', figure1);
box(axes1, 'on')
hold(axes1, 'on')
grid(axes1, 'on')
title('Architecture 5')
xlabel('Number of connection')
ylabel('Throughput Gbps')
plot(arch5_cnkopt(1), arch5_cnkopt(2)*0.001, 'o', 'linewidth', 2)
text(arch5_cnkopt(1)-300, arch5_cnkopt(2)*0.001, 'MILP Connection', 'fontsize', 14)

plot(arch5_thpopt(1), arch5_thpopt(2)*0.001, 'o', 'linewidth', 2)
text(arch5_thpopt(1)+10, arch5_thpopt(2)*0.001, 'MILP Throughput', 'fontsize', 14)

plot(arch5_hybopt(1), arch5_hybopt(2)*0.001, 'o', 'linewidth', 2)
text(arch5_hybopt(1)-210, arch5_hybopt(2)*0.001, 'MILP Hybrid', 'fontsize', 14)

plot(arch5_FF_fwd(1), arch5_FF_fwd(2)*0.001, 'o', 'linewidth', 2)
text(arch5_FF_fwd(1)+10, arch5_FF_fwd(2)*0.001, 'Ascending FF', 'fontsize', 14)

plot(arch5_FF_bwd(1), arch5_FF_bwd(2)*0.001, 'o', 'linewidth', 2)
text(arch5_FF_bwd(1)+10, arch5_FF_bwd(2)*0.001, 'Descending FF', 'fontsize', 14)

plot(arch5_AJ(1), arch5_AJ(2)*0.001, 'o', 'linewidth', 2)
text(arch5_AJ(1)+10, arch5_AJ(2)*0.001, 'SPSA', 'fontsize', 14)

figure_size = get(figure1, 'position');
set(figure1, 'position', figure_size*2);
saveas(figure1, 'arch5_pod100_scatter.jpg')
% Conclusion:
% 1. Hybrid optimization results are not good, longer running time