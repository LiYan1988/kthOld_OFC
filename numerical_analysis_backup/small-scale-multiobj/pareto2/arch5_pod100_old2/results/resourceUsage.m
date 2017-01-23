function [matrixResource, efficiency, outages] = ...
    resourceUsage(numPods, numCores, numSlots, cnkMatrix)

matrixResource = zeros(numPods*numCores, numSlots);
totalTraffic = sum(cnkMatrix(:, 8));
totalResourceUsed = sum(cnkMatrix(:, 4))*25;
outages = 0;
for i = 1:size(cnkMatrix, 1)
    src = cnkMatrix(i, 1)+1;
    dst = cnkMatrix(i, 2)+1;
    spec = cnkMatrix(i, 3)+1;
    slots_used = cnkMatrix(i, 4);
    core_src = cnkMatrix(i, 5)+1;
    core_dst = cnkMatrix(i, 6)+1;
    cores_used = cnkMatrix(i, 7);
    srccol = ((src-1)*numCores+core_src):((src-1)*numCores+core_src+cores_used-1);
    dstcol = ((dst-1)*numCores+core_dst):((dst-1)*numCores+core_dst+cores_used-1);
    specrow = spec:(spec+slots_used-1);
    if sum(sum(matrixResource(srccol, specrow),1),2)==0 && ...
            sum(sum(matrixResource(dstcol, specrow),1),2)==0
        matrixResource(srccol, specrow) = 1;
        matrixResource(dstcol, specrow) = 1;
    else
        outages = outages+1;
    end
end

efficiency = totalTraffic/totalResourceUsed;