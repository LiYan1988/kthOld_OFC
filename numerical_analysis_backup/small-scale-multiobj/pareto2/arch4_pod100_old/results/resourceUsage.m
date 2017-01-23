function [matrixResource, efficiency, outages] = ...
    resourceUsage(numPods, numCores, numSlots, cnkMatrix)

matrixResource = zeros(numPods*numCores, numSlots);
totalTraffic = sum(cnkMatrix(:, 7));
totalResourceUsed = sum(cnkMatrix(:, 4))*75;
outages = 0;
for i = 1:size(cnkMatrix, 1)
    src = cnkMatrix(i, 1)+1;
    dst = cnkMatrix(i, 2)+1;
    spec = cnkMatrix(i, 3)+1;
    slots_used = cnkMatrix(i, 4);
    specrow = spec:(spec+slots_used-1);
    if sum(matrixResource(src, specrow))==0 && ...
            sum(matrixResource(dst, specrow))==0
        matrixResource(src, specrow) = 1;
        matrixResource(dst, specrow) = 1;
    else
        outages = outages+1;
    end
end

efficiency = totalTraffic/totalResourceUsed;