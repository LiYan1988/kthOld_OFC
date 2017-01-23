clc;
close all;
clear;
% optimality gaps of FF ascending and descending for different architecture
% and number of PODs

%%
% plot optimization gap for arch2 FF forward against connection
% optimization
arch2_FF_fwd_cnkgap_pod100 = 0.9509;
arch2_FF_fwd_thpgap_pod100 = 0.8585;

arch2_FF_fwd_cnkgap_pod150 = 0.9669;
arch2_FF_fwd_thpgap_pod150 = 0.8808;

arch2_FF_fwd_cnkgap_pod200 = 0.9914;
arch2_FF_fwd_thpgap_pod200 = 0.9373;

y = 1-[arch2_FF_fwd_cnkgap_pod100, arch2_FF_fwd_thpgap_pod100;...
    arch2_FF_fwd_cnkgap_pod150, arch2_FF_fwd_thpgap_pod150;...
    arch2_FF_fwd_cnkgap_pod200, arch2_FF_fwd_thpgap_pod200];
title1 = 'Ascending First Fit in Architecture 2 with Connection Optimized';
xlabel1 = 'Number of PODs';
ylabel1 = 'Optimality gap';
figure1 = createfigure_optimality_gap(y, title1, xlabel1, ylabel1, [0, 0.15], 4);
saveas(figure1, 'arch2_FF_ascending.jpg')

% plot optimization gap for arch2 FF backward against throughput
% optimization
arch2_FF_bwd_cnkgap_pod100 = 0.9980;
arch2_FF_bwd_thpgap_pod100 = 0.9696;

arch2_FF_bwd_cnkgap_pod150 = 0.9980;
arch2_FF_bwd_thpgap_pod150 = 0.9696;

arch2_FF_bwd_cnkgap_pod200 = 0.9941;
arch2_FF_bwd_thpgap_pod200 = 0.9751;

y = 1-fliplr([arch2_FF_bwd_cnkgap_pod100, arch2_FF_bwd_thpgap_pod100;...
    arch2_FF_bwd_cnkgap_pod150, arch2_FF_bwd_thpgap_pod150;...
    arch2_FF_bwd_cnkgap_pod200, arch2_FF_bwd_thpgap_pod200]);
title1 = 'Descending First Fit in Architecture 2 with Throughput Optimized';
xlabel1 = 'Number of PODs';
ylabel1 = 'Optimality gap';
figure1 = createfigure_optimality_gap(y, title1, xlabel1, ylabel1, [0, 0.05], 6);
saveas(figure1, 'arch2_FF_descending.jpg')

