function figure1 = createArea(X1, ymatrix1)
%CREATEFIGURE(X1, YMATRIX1)
%  X1:  area x
%  YMATRIX1:  area matrix data

%  Auto-generated by MATLAB on 14-Sep-2016 22:44:55

% Create figure
figure1 = figure;

% Create axes
axes1 = axes('Parent',figure1,'YGrid','on','XGrid','on',...
    'YTickLabel',{'85%','90%','95%','100%'},...
    'XMinorTick','on',...
    'XScale','log',...
    'FontSize',12);
%% Uncomment the following line to preserve the Y-limits of the axes
% ylim(axes1,[0.85 1]);
box(axes1,'on');
hold(axes1,'on');

% Create multiple lines using matrix input to area
area1 = area(X1,ymatrix1,'LineWidth',2,'BaseValue',0.85,'Parent',axes1);
set(area1(3),'DisplayName','one core',...
    'FaceColor',[0 0.447058826684952 0.74117648601532]);
set(area1(2),'DisplayName','two cores',...
    'FaceColor',[0.850980401039124 0.325490206480026 0.0980392172932625]);
set(area1(1),'DisplayName','three cores',...
    'FaceColor',[0.929411768913269 0.694117665290833 0.125490203499794]);

% Create xlabel
xlabel('\beta','FontWeight','bold','FontSize',16);

% Create ylabel
ylabel('Percentage','FontSize',16);

% Create legend
legend1 = legend(axes1,'show');
set(legend1,'Location','southwest');
