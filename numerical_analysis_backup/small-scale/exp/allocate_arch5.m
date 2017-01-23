function [res, blk] = allocate_arch5(clist, num_pods, num_cores, num_specs)
load core_slot_pair.mat
res = ones(num_cores, num_specs, num_pods);
num_cnk = size(clist, 1);
blk = num_cnk;
remain_list = zeros(0, 4);
for i=1:num_cnk
    tmp = clist(i,:);
    [suc, res] = first_fit(tmp, res, num_cores, num_specs);
    if suc==0
        remain_list(end+1,:) = tmp;
    else
        blk = blk-1;
    end
end
for i=1:length(remain_list)
    tmp = remain_list(i, :);
    capacity = tmp(3)*(tmp(4)-1);
    cspair = pos_cs(capacity, core_slot_pair);
    for k=1:size(cspair,1)
        tmp2 = tmp;
        tmp2(3:4) = cspair(k, :);
        [suc, res] = first_fit(tmp2, res, num_cores, num_specs);
        if suc==1
            blk = blk-1;
            break;
        end
    end
end

end

function [suc, res] = first_fit(row_cnk, res, num_cores, num_specs)
src = row_cnk(1)+1;
dst = row_cnk(2)+1;
nc = row_cnk(3); % #core
ns = row_cnk(4); % #slot
for i=1:num_specs-ns+1
    % index of spectrum slot
    dst_avail = 1;
    for j=1:num_cores-nc+1
        % index of core in src
        if dst_avail && is_avail(res, nc, ns, j, i, src)
            for k=1:num_cores-nc+1
                % index of core in dst
                if is_avail(res, nc, ns, k, i, dst)
                    res = update_resource(res, i, j, k, row_cnk);
                    suc = 1;
                    return
                end
            end
        else
            dst_avail = 0;
        end
    end
end
suc = 0;
end

function suc = is_avail(res, nc, ns, core_idx, spec_idx, pod)
suc=1;
for i=core_idx:core_idx+nc-1
    for j=spec_idx:spec_idx+ns-1
        if res(i, j, pod)==0
            suc=0;
            return
        end
    end
end
end

function res_new = update_resource(res, spec_idx, core_idx_src, core_idx_dst, row_cnk)
src = row_cnk(1)+1;
dst = row_cnk(2)+1;
nc = row_cnk(3);
ns = row_cnk(4);
res_new = res;
for i=0:nc-1
    for j=spec_idx:spec_idx+ns-1
        res_new(i+core_idx_src, j, src) = 0;
        res_new(i+core_idx_dst, j, dst) = 0;
    end
end
end

function cspair = pos_cs(capacity, core_slot_pair)
if capacity==1
    idx = 2;
elseif capacity==4
    idx = 3;
elseif capacity==8
    idx = 4;
elseif capacity==16
    idx = 5;
elseif capacity==40
    idx = 6;
end
cspair = core_slot_pair{idx};
end