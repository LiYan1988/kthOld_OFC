clc;
close all;
clear;
% optimality gaps of FF ascending and descending for different architecture
% and number of PODs

%%
% plot optimization gap for arch4 FF forward against connection
% optimization
arch4_FF_fwd_cnkgap_pod100 = 0.9712;
arch4_FF_fwd_thpgap_pod100 = 0.8784;

arch4_FF_fwd_cnkgap_pod150 = 1.0169;
arch4_FF_fwd_thpgap_pod150 = 0.9283;

arch4_FF_fwd_cnkgap_pod200 = 1.0525;
arch4_FF_fwd_thpgap_pod200 = 0.9368;

y = 1-[arch4_FF_fwd_cnkgap_pod100, arch4_FF_fwd_thpgap_pod100;...
    arch4_FF_fwd_cnkgap_pod150, arch4_FF_fwd_thpgap_pod150;...
    arch4_FF_fwd_cnkgap_pod200, arch4_FF_fwd_thpgap_pod200];
title1 = 'Ascending First Fit in Architecture 4 with Connection Optimized';
xlabel1 = 'Number of PODs';
ylabel1 = 'Optimality gap';
figure1 = createfigure_optimality_gap(y, title1, xlabel1, ylabel1, [-0.05, 0.15], 4);
saveas(figure1, 'arch4_FF_ascending.jpg')

% plot optimization gap for arch4 FF backward against throughput
% optimization
arch4_FF_bwd_cnkgap_pod100 = 1.0135;
arch4_FF_bwd_thpgap_pod100 = 1.0197;

arch4_FF_bwd_cnkgap_pod150 = 1.0529;
arch4_FF_bwd_thpgap_pod150 = 0.9935;

arch4_FF_bwd_cnkgap_pod200 = 1.0518;
arch4_FF_bwd_thpgap_pod200 = 0.9809;

y = 1-fliplr([arch4_FF_bwd_cnkgap_pod100, arch4_FF_bwd_thpgap_pod100;...
    arch4_FF_bwd_cnkgap_pod150, arch4_FF_bwd_thpgap_pod150;...
    arch4_FF_bwd_cnkgap_pod200, arch4_FF_bwd_thpgap_pod200]);
title1 = 'Descending First Fit in Architecture 4 with Throughput Optimized';
xlabel1 = 'Number of PODs';
ylabel1 = 'Optimality gap';
figure1 = createfigure_optimality_gap(y, title1, xlabel1, ylabel1, [-0.1, 0.04], 5);
saveas(figure1, 'arch4_FF_descending.jpg')

