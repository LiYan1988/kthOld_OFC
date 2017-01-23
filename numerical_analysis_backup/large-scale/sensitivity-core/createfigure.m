function createfigure(YMatrix1)
%CREATEFIGURE(YMATRIX1)
%  YMATRIX1:  matrix of y data

%  Auto-generated by MATLAB on 19-Jun-2016 18:16:42

% Create figure
figure1 = figure;

% Create axes
axes1 = axes('Parent',figure1,'YGrid','on','XGrid','on');
%% Uncomment the following line to preserve the X-limits of the axes
xlim(axes1,[1 20]);
box(axes1,'on');
hold(axes1,'on');

% Create multiple lines using matrix input to plot
plot1 = plot(YMatrix1,'LineWidth',2,'Parent',axes1);
set(plot1(1),'DisplayName','Arch1 ILP','Marker','^',...
    'Color',[0.494117647409439 0.184313729405403 0.556862771511078]);
set(plot1(2),'DisplayName','Arch2 FF','Marker','x','LineStyle','--');
set(plot1(3),'DisplayName','Arch2 SPSA','Marker','x','LineStyle',':',...
    'Color',[0.850980401039124 0.325490206480026 0.0980392172932625]);
set(plot1(4),'DisplayName','Arch2 SA','Marker','x');
set(plot1(5),'DisplayName','Arch4 FF','Marker','square','LineStyle','--',...
    'Color',[0 0.447058826684952 0.74117648601532]);
set(plot1(6),'DisplayName','Arch4 SPSA','Marker','square','LineStyle',':',...
    'Color',[0.850980401039124 0.325490206480026 0.0980392172932625]);
set(plot1(7),'DisplayName','Arch4 SA','Marker','square',...
    'Color',[0.929411768913269 0.694117665290833 0.125490203499794]);
set(plot1(8),'DisplayName','Arch5 FF','Marker','v','LineStyle','--',...
    'Color',[0 0.447058826684952 0.74117648601532]);
set(plot1(9),'DisplayName','Arch5 SPSA','Marker','v','LineStyle',':',...
    'Color',[0.850980401039124 0.325490206480026 0.0980392172932625]);
set(plot1(10),'DisplayName','Arch5 SA','Marker','v',...
    'Color',[0.929411768913269 0.694117665290833 0.125490203499794]);


% Create xlabel
xlabel('Number of spatial modes','FontSize',11);

% Create ylabel
ylabel('Established connections','FontSize',11);

% Create legend
legend1 = legend(axes1,'show');
set(legend1,'Location','northwest');

