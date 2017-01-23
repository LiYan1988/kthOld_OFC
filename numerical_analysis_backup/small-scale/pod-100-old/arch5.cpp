#include <random>
#include <iostream>
#include <vector>
#include <algorithm>
#include <iomanip>
#include <fstream>
#include <string>
#include <sstream>
#include <math.h>
#include <ostream>
#include <numeric>
#include <thread>
#include <mutex>
#include <ctime>
#include <set>
#include <map>
#include <tuple>
//#include "gurobi_c++.h"

using namespace std;

unsigned NUM_THREADS = thread::hardware_concurrency();

class Connection;

typedef vector<int> Row; // row of matrix
typedef vector<Row> Matrix; // traffic matrix

typedef vector<bool> Row_bool;
typedef vector<Row_bool> Matrix_bool;
typedef vector<Matrix_bool> Tensor3d_bool;
typedef vector<Tensor3d_bool> Tensor4d_bool;
typedef vector<pair<int, int>> Vecpairint;
typedef vector<Vecpairint> Matpairint;

typedef vector<Connection> ConnectionList; // ordered connection list

default_random_engine generator;


mutex mtx;

class Connection{
public:
    int total_slots;
    int nc; // #core
    int ns; // #spec
    int src;
    int dst;
    int gb; // guardband
    vector<int> possible_cores;
    Connection(const int&src, const int&dst,
               const int&num_slots, const int&gb){
        this->src = src;
        this->dst = dst;
        this->total_slots = num_slots;
        this->nc = 1;
        this->ns = num_slots+gb;
        this->gb = gb;
    }
    void change_core(const int&nc){
        this->nc = nc;
        this->ns = ceil(float(total_slots)/nc)+gb;
    }
    void set_possible_cores(const vector<int>&possible_cores)
    {
        this->possible_cores = possible_cores;
    }
    bool operator<(const Connection &other)const{
        if(this->total_slots<other.total_slots){
            return true;
        }
        else if(this->total_slots==other.total_slots){
            if(this->src<other.src) return true;
            else if(this->src==other.src&&
                    this->dst<other.dst) return true;
        }
        return false;
    }
};

/************************* Energy function **********************/

void update_resource(Tensor3d_bool &res, const int &spec_idx,
                     const int &core_idx_src,
                     const int &core_idx_dst, const Connection&c){
    // update the resource tensor
    int nc = c.nc; // #core
    int ns = c.ns; //#slot
    int src = c.src;
    int dst = c.dst;
    for(int i=0; i<nc; ++i){
        for(int j=spec_idx; j<spec_idx+ns; ++j){
            res[src][i+core_idx_src][j] = false;
            res[dst][i+core_idx_dst][j] = false;
        }
    }

}

bool is_avail(const Tensor3d_bool&res, int nc,
              int ns, int core_idx, int spec_idx, int pod){
    for(int i=core_idx; i<core_idx+nc; ++i){
        for(int j=spec_idx; j<spec_idx+ns; ++j){
            if(!res[pod][i][j]) return false;
        }
    }
    return true;
}

bool is_avail_arch2(const Tensor3d_bool res, int nc, int ns,
    int core_idx, int spec_idx, int pod)
{
    for(int j=spec_idx; j<spec_idx+ns; ++j){
        if(!res[pod][core_idx][j]) return false;
    }
    return true;
}

bool first_fit(const Connection &c, Tensor3d_bool &res,
               int num_cores, int num_specs)
{
    int src = c.src;
    int dst = c.dst;
    int nc = c.nc; // #core
    int ns = c.ns; // #slot
    for(int i=0; i<=num_specs-ns; ++i){
        bool dst_avail = true;
        for(int j=0; j<=num_cores-nc; ++j){
            if(dst_avail&&is_avail(res, nc, ns, j, i, src)){
                for(int k=0; k<=num_cores-nc; ++k){
                    if(is_avail(res, nc, ns, k, i, dst)){
                        update_resource(res, i, j, k, c);
                        return true;
                    }
                }
                dst_avail = false;
            }
        }
    }
    return false;
}

bool first_fit_arch2(const Connection& c, Tensor3d_bool& res,
    int num_cores, int num_specs)
{
    // first check all the sltos in one core, then check another core
    int src = c.src;
    int dst = c.dst;
    int nc = c.nc; // #core
    int ns = c.ns; // #slot
    Row slot_avail(num_specs, true);
    for(int i=0; i<=num_cores-nc; ++i){
        for(int j=0; j<=num_specs-ns; ++j){
            if(!slot_avail[j]) continue;
            bool dst_avail = true;
            if(dst_avail&&is_avail_arch2(res, nc, ns, i, j, src)){
                for(int k=0; k<=num_cores-nc; ++k){
                    if(is_avail_arch2(res, nc, ns, k, j, dst)){
                        update_resource(res, j, i, k, c);
                        return true;
                    }
                }
                dst_avail = false;
                slot_avail[j] = false;
            }
        }
    }
    return false;
}

void Energy_arch2(ConnectionList in_list, int num_pods,
    int num_cores, int num_specs, int& energy)
{
    // Calculate blocked demands in arch2 with first fit in core, then slots
    energy = in_list.size();
    Tensor3d_bool res(num_pods, Matrix_bool(num_cores,
        Row_bool(num_specs, true)));
    for(auto c: in_list){
        energy -= first_fit_arch2(c, res, num_cores, num_specs);
    }
}

void Energy(ConnectionList connection_list, int num_pods,
           int num_cores, int num_specs, int&energy)
{
    // Calculate blocked demands in a connection list with first fit
    energy = connection_list.size();
    Tensor3d_bool res(num_pods, Matrix_bool(num_cores,
                  Row_bool(num_specs, true)));
    for(auto c: connection_list)
    {
        energy -= first_fit(c, res, num_cores, num_specs);
    }
}

/***************************** independent set *************************/
class PCList{
public:
    int num_cnk;
    ConnectionList is_list; // IS list
    ConnectionList in_list; // initial list
    set<int> left_cnks; // left connections
    PCList(ConnectionList in_list)
    {
        int num_cnk;
        num_cnk = in_list.size();
        ConnectionList is_list;
        set<int> left_cnks;
        for(int i=0; i<num_cnk; ++i){
            left_cnks.insert(i);
        }
        this->num_cnk = num_cnk;
        this->is_list = is_list;
        this->in_list = in_list;
        this->left_cnks = left_cnks;
    }
    void add_is()
    {
        set<int> tmp_left_cnks{left_cnks};
        while(tmp_left_cnks.size()>0){
            Connection cnk_add = in_list[*tmp_left_cnks.begin()]; // first left cnk index
            is_list.push_back(cnk_add);
            left_cnks.erase(*tmp_left_cnks.begin());
            tmp_left_cnks.erase(tmp_left_cnks.begin());
            int src = cnk_add.src;
            int dst = cnk_add.dst;

            set<int>::iterator it = tmp_left_cnks.begin();
            while(it!=tmp_left_cnks.end()){
                if(in_list[*it].src==src||in_list[*it].dst==src||
                    in_list[*it].src==dst||in_list[*it].dst==dst) tmp_left_cnks.erase(it);
                ++it;

            }
        }
    }
    void find_all_is()
    {
        while(left_cnks.size()>0){
            add_is();
        }
    }
};

int find_ic(ConnectionList&is_list, ConnectionList&in_list)
{
    for(int i=0; i<in_list.size(); ++i){
        bool isfind = true;
        for(int j=0; j<is_list.size(); ++j){
            if(in_list[i].src==is_list[j].src||in_list[i].src==is_list[j].dst||
                in_list[i].dst==is_list[j].src||in_list[i].dst==is_list[j].dst){
                isfind = false;
                break;
            }
        }
        if(isfind) return i;
    }
    return -1;
}

ConnectionList find_is(ConnectionList&in_list)
{
    ConnectionList is_list;
    is_list.push_back(in_list[0]);
    in_list.erase(in_list.begin());
    bool stop = false;
    while(!stop){
        int ind = find_ic(is_list, in_list);
        if(ind!=-1){
            is_list.push_back(in_list[ind]);
            in_list.erase(in_list.begin()+ind);
        }
        else stop = true;
    }
    return is_list;
}

void Energy_is(ConnectionList connection_list, int num_pods,
           int num_cores, int num_specs, int&energy)
{
    // Calculate blocked demands in a connection list with first fit
    energy = connection_list.size();
    Tensor3d_bool res(num_pods, Matrix_bool(num_cores,
                  Row_bool(num_specs, true)));
    ConnectionList is_list, in_list;
    in_list = connection_list;
    is_list = find_is(in_list);
    bool flag = true;
    while(flag){
        for(auto c: is_list){
            energy -= first_fit(c, res, num_cores, num_specs);
        }
        if(in_list.size()>0){
            is_list = find_is(in_list);
        }
        else flag = false;
    }
}

void Energy_is2(ConnectionList connection_list, int num_pods,
           int num_cores, int num_specs, int&energy)
{
    // Calculate blocked demands in a connection list with first fit
    energy = connection_list.size();
    Tensor3d_bool res(num_pods, Matrix_bool(num_cores,
                  Row_bool(num_specs, true)));
    PCList pc(connection_list);
    pc.find_all_is();
    for(auto c: pc.is_list)
    {
        energy -= first_fit(c, res, num_cores, num_specs);
    }
}
/****************************** POD list class *************************/

bool pod_comp(pair<int, int> pod1, pair<int, int> pod2)
{
    return pod1.second < pod2.second;
}

/******************************* Traffic class **************************/

class Traffic{
public:
    // DCN parameters
    int id;
    int num_pods; // number of pods
    int num_cores; // number of cores
    int num_specs; // number of spectrum slots
    int max_cnk; // max connection per pod
    int min_cnk; // min connection per pod
    int tfk_mean; // traffic mean
    int tfk_var; // traffic variance
    int cpst_slot; // capacity of one spectrum slot
    int gb_slot; // number of guardband slots
    int num_cnk; // total number of connections
    float load;
    Matrix tfk_mat; // traffic matrix
    ConnectionList connection_list;
    Row tfk_vals;
    Vecpairint core_spec_sets;
    Vecpairint tfk_stat; // number of each traffic values
    vector<vector<int>> tfk_on_pod; // i-th element: connections on POD i

    // annealing parameters
    float Tmax;
    float Tmin;
    int Smax; // max steps
    float T_cur; // current temperature
    int s_cur; // current step
    vector<pair<ConnectionList, int>> sa_hist;
    float alpha; // annealing factor
    int E_cur; // current energy
    int step_ini; // initial random movement step size
    float step_delta; // step size reducing factor
    int n_iter_ini; // initial number of iterations, in each iteration NUM_THREADS threads
    float n_iter_delta; // 1.05, #iteration increasing factor
    int n_rej_th; // threshold, greater than which step size is finer and reducing slower
    int n_rej; // #non-improvements
    // note: prob1<=prob2<=1
    float prob1; // probability of first movement
    float prob2; // prob2-prob1: probability of second movement

    ofstream myfile;
    string trafficname;
    string matrixfile;
    string logfile;
    string resultfile;

    time_t start = time(NULL);

    Traffic(string trafficname, int id, int num_pods, int max_cnk, int min_cnk, float load, int tfk_mean, int tfk_var,
            int cpst_slot, int gb_slot, int num_cores, int num_specs)
    {
        this->trafficname = trafficname;
        this->id = id;
        this->num_pods = num_pods;
        this->max_cnk = max_cnk;
        this->min_cnk = min_cnk;
        this->tfk_mean = tfk_mean;
        this->tfk_var = tfk_var;
        this->cpst_slot = cpst_slot;
        this->gb_slot = gb_slot;
        this->num_cores = num_cores;
        this->num_specs = num_specs;
        this->load = load;
        ostringstream ss;
        ss<<this->id;
        this->matrixfile = trafficname+"_matrix_"+ss.str()+".csv";
        this->logfile = trafficname+"_log_"+ss.str()+".txt";
        this->resultfile = trafficname+"_result_"+ss.str()+".csv";
    }

    /************************ Generate traffic *****************************/

    vector<int> find_possible_cores(const int&num)
    {
        vector<int> tmp;
        for(int i=1; i<=num_cores; ++i){
            if(num%i==0 && num/i+gb_slot<=num_specs){
                tmp.push_back(i);
            }
        }
        return tmp;
    }

    Vecpairint find_possible_pairs(const int&num)
    {
        Vecpairint tmp;
        for(int i=1; i<=num_cores; ++i){
            if(num%i==0 && num/i+gb_slot<=num_specs){
                tmp.push_back(make_pair(i, num/i+gb_slot));
            }
        }
        return tmp;
    }

    double cdf(double x)
    {
        // constants
        double a1 =  0.254829592;
        double a2 = -0.284496736;
        double a3 =  1.421413741;
        double a4 = -1.453152027;
        double a5 =  1.061405429;
        double p  =  0.3275911;

        // Save the sign of x
        int sign = 1;
        if (x < 0)
            sign = -1;
        x = fabs(x)/sqrt(2.0);

        // A&S formula 7.1.26
        double t = 1.0/(1.0 + p*x);
        double y = 1.0 - (((((a5*t + a4)*t) + a3)*t + a2)*t + a1)*t*exp(-x*x);

        return 0.5*(1.0 + sign*y);
    }

    void read_traffic(string matrix_file)
    {
        ifstream data(matrix_file);
        string line;
        Row mat;
        int cnt=0;
        while(getline(data,line)){
            stringstream lineStream(line);
            string cell;
            while(getline(lineStream,cell,',')){
                if(cnt>25){
                    mat.push_back(stoi(cell));
                }
                cnt++;
            }
        }
        Matrix tm(num_pods, Row(num_pods, 0));
        cnt = 0;
        for(int i=0; i<this->num_pods; ++i){
            for(int j=0; j<this->num_pods; ++j){
                tm[i][j] = mat[cnt];
                cnt++;
            }
        }
        this->tfk_mat = tm;

        // initialize the connection list according to the required #slots
        ConnectionList tmp_list;
        Row tfk_vals;
        for(int i=0; i<this->num_pods; ++i)
        {
            for(int j=0; j<this->num_pods; ++j)
            {
                if(tm[i][j]>0){
                    Connection tmp_cnk = Connection(i, j, tm[i][j], gb_slot);
                    tmp_cnk.set_possible_cores(find_possible_cores(tm[i][j]));
                    tmp_list.push_back(tmp_cnk);
                    tfk_vals.push_back(tmp_cnk.total_slots);
                }
            }
        }
        Row tfk_slots(tfk_vals);
        set<int> s(tfk_vals.begin(), tfk_vals.end());
        tfk_vals.assign(s.begin(), s.end());
        sort(tmp_list.begin(), tmp_list.end());
        this->connection_list = tmp_list;
        this->num_cnk = tmp_list.size();
        this->tfk_vals = tfk_vals;
        Vecpairint core_spec_sets;
        for(auto i: tfk_vals){
            Vecpairint tmp = find_possible_pairs(i);
            core_spec_sets.insert(core_spec_sets.end(), tmp.begin(), tmp.end());
        }
        this->core_spec_sets = core_spec_sets;

        Vecpairint tfk_stat;
        for(int i=0; i<tfk_vals.size(); ++i){
            int n = count(tfk_slots.begin(), tfk_slots.end(), tfk_vals[i]);
            tfk_stat.push_back(make_pair(tfk_vals[i], n));
        }
        this->tfk_stat = tfk_stat;
    }

    void generate_traffic(){
        Matrix tm(num_pods, Row(num_pods, 0));
        // data rates are generated according to CDF of normal distribution
        double p1 = cdf(double(1-tfk_mean)/tfk_var);
        double p10 = cdf(double(10-tfk_mean)/tfk_var);
        double p100 = cdf(double(100-tfk_mean)/tfk_var);
        double p200 = cdf(double(200-tfk_mean)/tfk_var);
        double p400 = cdf(double(400-tfk_mean)/tfk_var);
        double p1000 = cdf(double(1000-tfk_mean)/tfk_var);
        for(int i=0; i<num_pods; ++i)
        {
            int tmp_cnct = min_cnk+(rand()%(max_cnk-min_cnk+1)); // # connections per POD
            for(int j=0; j<tmp_cnct; ++j)
            {
                double rnd = double(rand())/RAND_MAX;
                if(rnd<p1)tm[i][j] = ceil(float(1)/cpst_slot);
                else if(rnd<p10)tm[i][j] = ceil(float(10)/cpst_slot);
                else if(rnd<p100)tm[i][j] = ceil(float(100)/cpst_slot);
                else if(rnd<p200)tm[i][j] = ceil(float(200)/cpst_slot);
                else if(rnd<p400)tm[i][j] = ceil(float(400)/cpst_slot);
                else tm[i][j] = ceil(float(1000)/cpst_slot);
            }
            random_shuffle(tm[i].begin(), tm[i].end());
            // change the diagonal nonzero element to somewhere else
            if(tm[i][i] != 0){
                Row::iterator p = find(tm[i].begin(), tm[i].end(), 0);
                if(p!=tm[i].end()){
                    *p = tm[i][i];
                }
                tm[i][i] = 0;
            }
        }
        this->tfk_mat = tm;

        // initialize the connection list according to the required #slots
        ConnectionList tmp_list;
        Row tfk_vals;
        for(int i=0; i<this->num_pods; ++i)
        {
            for(int j=0; j<this->num_pods; ++j)
            {
                if(tm[i][j]>0){
                    Connection tmp_cnk = Connection(i, j, tm[i][j], gb_slot);
                    tmp_cnk.set_possible_cores(find_possible_cores(tm[i][j]));
                    tmp_list.push_back(tmp_cnk);
                    tfk_vals.push_back(tmp_cnk.total_slots);
                }
            }
        }
        Row tfk_slots(tfk_vals);
        set<int> s(tfk_vals.begin(), tfk_vals.end());
        tfk_vals.assign(s.begin(), s.end());
        sort(tmp_list.begin(), tmp_list.end());
        this->connection_list = tmp_list;
        this->num_cnk = tmp_list.size();
        this->tfk_vals = tfk_vals;
        Vecpairint core_spec_sets;
        for(auto i: tfk_vals){
            Vecpairint tmp = find_possible_pairs(i);
            core_spec_sets.insert(core_spec_sets.end(), tmp.begin(), tmp.end());
        }
        this->core_spec_sets = core_spec_sets;

        Vecpairint tfk_stat;
        for(int i=0; i<tfk_vals.size(); ++i){
            int n = count(tfk_slots.begin(), tfk_slots.end(), tfk_vals[i]);
            tfk_stat.push_back(make_pair(tfk_vals[i], n));
        }
        this->tfk_stat = tfk_stat;
    }

    void show_traffic_matrix(){
        cout<<"Traffic matrix id:"<<this->id<<endl;
        cout<<"Traffic matrix:"<<endl;
        for(int i=0; i<this->num_pods; ++i)
        {
            for(int j=0; j<this->num_pods; ++j)
            {
                cout<<setw(4)<<this->tfk_mat[i][j]<<" | ";
            }
            cout<<endl;
        }
    }

    /********************** POD list *****************************/
    Vecpairint pod_sort_reverse()
    {
        // construct pod list and sort
        Vecpairint pod_list;
        for(int i=0; i<num_pods; ++i){
            int n=0;
            for(int j=0; j<num_pods; ++j){
                if(tfk_mat[i][j]>0) n++;
                if(tfk_mat[j][i]>0) n++;
            }
            pod_list.push_back(make_pair(i, n));
        }
        sort(pod_list.begin(), pod_list.end(), pod_comp);
        reverse(pod_list.begin(), pod_list.end());
        return pod_list;
    }

    ConnectionList pod2cnklist(const Vecpairint& pod_list)
    {
        ConnectionList out_list;
        Matrix tmp_mat(tfk_mat);
        for(int id=0; id<num_pods; ++id){
            int i = pod_list[id].first;
            ConnectionList tmp_list;
            for(int j=0; j<num_pods; ++j){
                if(tmp_mat[i][j]>0){
                    Connection tmp_cnk = Connection(i, j, tmp_mat[i][j], gb_slot);
                    tmp_list.push_back(tmp_cnk);
                    tmp_mat[i][j]=0;
                }
                if(tmp_mat[j][i]>0){
                    Connection tmp_cnk = Connection(j, i, tmp_mat[j][i], gb_slot);
                    tmp_list.push_back(tmp_cnk);
                    tmp_mat[j][i]=0;
                }
            }
            sort(tmp_list.begin(), tmp_list.end());
            out_list.insert(out_list.end(), tmp_list.begin(), tmp_list.end());
        }
        return out_list;
    }

    /********************** SA: random moves ***********************/

    void random_change_core(ConnectionList &in_list, const int&swap_size)
    {
        for(int i=0; i<swap_size; ++i){
            int n = rand()%num_cnk;
            int m = in_list[n].possible_cores.size();
            int k = rand()%m;
            in_list[n].change_core(in_list[n].possible_cores.at(k));
        }
    }

    void random_swap(ConnectionList &connection_list){
        //randomly swap the order of two demands
        int swap_size = num_pods;
        for(int i=0; i<swap_size; ++i){
            int a, b;
            a = rand()%(num_cnk-1);
            b = a+1+rand()%(num_cnk-a-1);
            iter_swap(connection_list.begin()+a, connection_list.begin()+b);
        }
    }

    void random_swap_sameslt(ConnectionList &in_list, int swap_size, int validx)
    {
        // randomly swap traffic order with the same #slots
        swap_size = min(min(swap_size, num_cnk), tfk_stat[validx].second);
        vector<int> tmp_front(num_cnk);
        iota(tmp_front.begin(), tmp_front.end(), 0);
        random_shuffle(tmp_front.begin(), tmp_front.end());
        int cnt=0;
        ConnectionList::iterator it = in_list.begin();
        for(int i=0; i<num_cnk; i=i+2){
            if(cnt>=swap_size) break;
            if(in_list[tmp_front[i]].total_slots==tfk_vals[validx]&&
                in_list[tmp_front[i+1]].total_slots==tfk_vals[validx]){
                iter_swap(it+tmp_front[i], it+tmp_front[i+1]);
            }
            cnt++;
        }

    }

    void random_swap_b2f(ConnectionList &connection_list, int swap_size){
        //swap unallocated demands to front
        int swap_start = num_cnk-E_cur;
        swap_size = min(swap_size, min(swap_start, E_cur));
        vector<int> tmp_front(swap_start);
        iota(tmp_front.begin(), tmp_front.end(), 0);
        vector<int> tmp_back(E_cur);
        iota(tmp_back.begin(), tmp_back.end(), swap_start);
        random_shuffle(tmp_front.begin(), tmp_front.end());
        random_shuffle(tmp_back.begin(), tmp_back.end());
        for(int i=0; i<swap_size; ++i){
            iter_swap(connection_list.begin()+tmp_front[i],
                      connection_list.begin()+tmp_back[i]);
        }
    }

    void random_swap_f2f(ConnectionList &in_list, int swap_size){
        //swap unallocated demands to front
        int swap_end = num_cnk-E_cur;
        swap_size = min(2*swap_size, swap_end);
        vector<int> tmp_front(swap_end);
        iota(tmp_front.begin(), tmp_front.end(), 0);
        random_shuffle(tmp_front.begin(), tmp_front.end());
        for(int i=0; i<swap_size; i=i+2){
            iter_swap(in_list.begin()+tmp_front[i],
                      in_list.begin()+tmp_front[i+1]);
        }
    }

    void random_swap_a2a(ConnectionList &in_list, int swap_size){
        //swap unallocated demands to front
        int swap_end = num_cnk;
        swap_size = min(2*swap_size, swap_end);
        vector<int> tmp_front(swap_end);
        iota(tmp_front.begin(), tmp_front.end(), 0);
        random_shuffle(tmp_front.begin(), tmp_front.end());
        ConnectionList::iterator it = in_list.begin();
        for(int i=0; i<swap_size; i=i+2){
            iter_swap(it+tmp_front[i], it+tmp_front[i+1]);
        }
    }

    void random_shift_sameslt(ConnectionList&in_list, int block_size, int tfkidx)
    {
        if(tfkidx<tfk_stat.size()&&block_size+2<tfk_stat[tfkidx].second){
            int a,b;
            a = 0;
            b = tfk_stat[0].second;
            for(int i=1; i<tfkidx; ++i){
                a += tfk_stat[i-1].second;
                b += tfk_stat[i].second;
            }
            block_size = min(block_size, b-a-2);
            int block_start = rand()%(b-a-block_size)+a+1;
            int block_end = rand()%(block_start-a)+a;
            move_range(block_start, block_size, block_end, in_list);
        }
    }

    void random_shift_f2f(ConnectionList &in_list, const int&block_size){
        // shift the unallocated traffic to front
        int a = rand()%(num_cnk-block_size);
        int b;
        do{
            b = rand()%(num_cnk);
        }while(b>a&&b<a+block_size);
        move_range(a, block_size, b, in_list);
    }

    void random_shift_b2f(ConnectionList &in_list, const int&block_size){
        // shift the unallocated traffic to front
        int a = rand()%(E_cur-block_size)+(num_cnk-E_cur);
        int b = rand()%(num_cnk-E_cur);
        move_range(a, block_size, b, in_list);
    }

    int step_size()
    {
//        cout<<step_ini<<"|"<<step_delta<<endl;
        if(n_rej<n_rej_th)return max(1, int(ceil(step_ini*pow(step_delta, s_cur))));
        else{
            n_rej = 0;
            step_ini *= 0.95;
            n_iter_ini = round(n_iter_ini*1.5);
//            T_cur = 2*T_cur;
            return min(1, int(ceil(step_ini*pow(step_delta, s_cur))));
        }
    }

    void move_blender(ConnectionList &in_list){
        float rnd = float(rand())/RAND_MAX;
        int movesize = step_size();
        if(rnd<prob1){
            // random_swap_b2f(in_list, movesize);
            // random_swap_f2f(in_list, movesize);
            // random_shift_f2f(in_list, movesize); // this seems better, and set prob1=1
            for(int i=0; i<tfk_vals.size(); ++i){
                random_swap_sameslt(in_list, movesize, i);
            }
            random_shift_f2f(in_list, movesize); // this seems better, and set prob1=1
        }
        else if(rnd<prob2){
            random_swap_sameslt(in_list, movesize, 0);
        }
        else{
            random_change_core(in_list, round(movesize*0.5));
        }
    }

    void move_range(size_t start, size_t length, size_t dst, ConnectionList &v){
        // shift a chunk of elements in v ([start, start+length)) to dst
        const size_t finnal_dst = dst > start ? dst-length : dst;

        ConnectionList tmp(v.begin()+start, v.begin()+start+length);
        v.erase(v.begin()+start, v.begin()+start+length);
        v.insert(v.begin()+finnal_dst, tmp.begin(), tmp.end());
    }

    /********************** SA: acceptance, schedule *************************/

    void set_probs(float prob1, float prob2)
    {
        this->prob1 = prob1;
        this->prob2 = prob2;
    }

    bool acceptance(const int &E_old, const int &E_new){
        // return true if accept the new solution
        float rnd = float(rand())/RAND_MAX;
        bool acc;
        if(E_new<E_old)acc=true;
        else if(rnd<1/(exp(-(E_old-E_new)/T_cur)+1)) acc=true;
        else acc=false;
        // if(s_cur%100==0) 
        write_process(E_old, E_new, rnd);
        return acc;
    }

    void schedule(float Tmax, float Tmin, int Smax,float alpha, int step_ini,
                  float step_delta, int n_iter_ini, float n_iter_delta)
    {
        this->Tmax = Tmax;
        this->Tmin = Tmin;
        this->Smax = Smax;
        this->alpha = alpha;
        this->s_cur = 0;
        int tmp;
        Energy(connection_list, num_pods, num_cores, num_specs, tmp);
        this->E_cur = tmp;
        this->T_cur = Tmax;
        this->step_ini = step_ini; //max(2*num_pods, int(num_cnk*0.01));
        this->step_delta = step_delta;
        this->n_iter_ini = n_iter_ini;
        this->n_iter_delta = n_iter_delta;
        this->n_rej_th = 20;
        sa_hist.clear();
        sa_hist.push_back(make_pair(connection_list, E_cur));
    }

    pair<ConnectionList, int> parrun(int n_iters, ConnectionList in_list)
    {
        vector<ConnectionList> permut_lists;
        Row energies(n_iters*NUM_THREADS);
        for(int i=0; i<n_iters*NUM_THREADS; ++i){
            ConnectionList buffer_list{in_list.begin(), in_list.end()};
            move_blender(buffer_list);
            permut_lists.push_back(buffer_list);
        }
        vector<thread> jobs(NUM_THREADS);
        for(int i=0; i<n_iters; ++i){
            for(int j=0; j<NUM_THREADS; ++j){
                int k = i*NUM_THREADS+j;
                jobs[j] = thread(Energy_is, permut_lists[k], num_pods,
                        num_cores, num_specs, ref(energies[k]));
            }
            for(int j=0; j<NUM_THREADS; ++j){
                jobs[j].join();
            }
        }
        int best_idx = 0;
        for(int i=1; i<n_iters*NUM_THREADS; ++i){
            if(energies[best_idx]>energies[i]) best_idx = i;
        }
        return make_pair(permut_lists[best_idx], energies[best_idx]);
    }

    void choose_stepsize(int step_ini, int range, int interval)
    {
        vector<pair<ConnectionList, int>> res;
        int best_idx=0;
        Row stepvec;
        for(int i=-range; i<=range; ++i){
            stepvec.push_back(step_ini+interval*i);
        }
        for(auto c: stepvec){
            this->step_ini = c;
            // cout<<this->step_ini<<endl;
            res.push_back(parrun(n_iter_ini, connection_list));
            cout<<this->step_ini<<"|"<<res.back().second<<endl;
        }
        for(int i=1; i<2*range+1; ++i){
            if(res[i].second<res[best_idx].second) best_idx = i;
        }
        this->step_ini = stepvec[best_idx];
        // cout<<"Final step is: "<<this->step_ini<<" energy is: "<<res[best_idx].second<<endl;
        this->connection_list = res[best_idx].first;
    }

    int num_iterations()
    {
        return max(1, int(round(n_iter_ini*pow(n_iter_delta, s_cur))));
    }

    /**************************** write files **************************/

    void write_matrix(){
        myfile.open(matrixfile);
        myfile<<"id,"<<this->id<<endl;
        myfile<<"num_pods,"<<this->num_pods<<endl;
        myfile<<"max_cnk,"<<this->max_cnk<<",load,"<<load<<endl;
        myfile<<"min_cnk,"<<this->min_cnk<<endl;
        myfile<<"tfk_mean,"<<this->tfk_mean<<endl;
        myfile<<"tfk_var,"<<this->tfk_var<<endl;
        myfile<<"traffic value,"<<"traffic counts"<<endl;
        for(int i=0; i<tfk_stat.size(); ++i){
            myfile<<tfk_stat[i].first<<","<<tfk_stat[i].second<<endl;
        }
        if(tfk_stat.size()<5){
            for(int i=0; i<5-tfk_stat.size(); ++i) myfile<<endl;
        }
        for(int i=0; i<this->num_pods; ++i)
        {
            for(int j=0; j<this->num_pods; ++j)
            {
                myfile<<this->tfk_mat[i][j]<<",";
            }
            myfile<<endl;
        }
        myfile.close();
    }

    void write_log_head(bool write_head)
    {
        if(write_head) myfile.open(logfile);
        else myfile.open(logfile, ios_base::app);
        myfile<<"Architecture: 2"<<" Simulation ID: "<<id<<endl;
        myfile<<"Max steps: "<<Smax<<". Initial blocked connections: "<<E_cur<<"/"<<num_cnk<<endl;
        myfile<<"========"<<endl;
        myfile.close();
    }

    void write_process(const int&E_old, const int&E_new, const float&rnd)
    {
        myfile.open(logfile, ios_base::app);
        myfile<<"Iteration "<<s_cur<<", #trials: "<<num_iterations()<<", step size:"<<step_size()<<endl;
        myfile<<"Blocked connections: "<<E_new<<"/"<<num_cnk<<endl;
        myfile<<"Improvement: "<<(E_old-E_new)<<", T: "<<T_cur<<endl;
        if(E_new<E_old){
            myfile<<"Accept better result."<<endl;
        }
        else if(rnd<1/(exp(-(E_old-E_new)/T_cur)+1))
        {
            myfile<<"rnd="<<rnd<<" prob.="<<1/(exp(-(E_old-E_new)/T_cur)+1)<<endl;
            myfile<<"Accept worse result."<<endl;
        }
        else{
            myfile<<"rnd="<<rnd<<" prob.="<<1/(exp(-(E_old-E_new)/T_cur)+1)<<endl;
            myfile<<"Reject worse result."<<endl;
        }
        time_t now = time(NULL);
        myfile<<"Time elapsed: "<<difftime(now, start)<<" seconds."<<endl;
        myfile<<"========"<<endl;
        myfile.close();
    }

    void write_result()
    {

        int best_idx = 0;
        for(int i=1; i<sa_hist.size(); ++i){
            if(sa_hist[best_idx].second>sa_hist[i].second)best_idx=i;
        }
        ConnectionList best_list = sa_hist[best_idx].first;
        int best_energy = sa_hist[best_idx].second;
        Tensor3d_bool res(num_pods, Matrix_bool(num_cores,
                    Row_bool(num_specs, true)));
        myfile.open(resultfile);
        myfile<<"Energy: "<<best_energy<<"/"<<num_cnk<<endl;
        myfile<<"source POD, destination POD, #cores, #slots, successful,"<<endl;
        for(auto c: best_list){
            myfile<<c.src<<","<<c.dst<<","<<c.nc<<","<<c.ns<<","<<first_fit(c, res, num_cores, num_specs)<<","<<endl;
        }
        myfile.close();
    }


    /************************* SA process ***************************/

    ConnectionList find_bestcnk()
    {
        int best_idx = 0;
        for(int i=1; i<sa_hist.size(); ++i){
            if(sa_hist[best_idx].second>sa_hist[i].second)best_idx=i;
        }
        ConnectionList best_list = sa_hist[best_idx].first;
        return best_list;
    }

    ConnectionList sa(ConnectionList in_list, bool write_head)
    {
        // simulated annealing process
        s_cur = 0;
        T_cur = Tmax;
        n_rej = 0;
        write_log_head(write_head);
        while(T_cur>Tmin && s_cur<Smax && E_cur>0)
        {
            int i = 0;
            int E_best_local;
            ConnectionList list_best_local;

            int n_iters = num_iterations(); // n_iters*NUM_THREADS energy evaluations
            vector<ConnectionList> permut_lists;
            Row energies(n_iters*NUM_THREADS);
            for(int i=0; i<n_iters*NUM_THREADS; ++i){
                ConnectionList buffer_list(in_list.begin(), in_list.end());
                move_blender(buffer_list);
                permut_lists.push_back(buffer_list);
            }
            vector<thread> jobs(NUM_THREADS);
            for(int i=0; i<n_iters; ++i){
                for(int j=0; j<NUM_THREADS; ++j){
                    int k = i*NUM_THREADS+j;
                    jobs[j] = thread(Energy, permut_lists[k], num_pods,
                            num_cores, num_specs, ref(energies[k]));
                }
                for(int j=0; j<NUM_THREADS; ++j){
                    jobs[j].join();
                }
            }
            int best_idx = 0;
            for(int i=1; i<n_iters*NUM_THREADS; ++i){
                if(energies[best_idx]>energies[i]) best_idx = i;
            }
//            for(auto i:energies) cout<<i<<endl;
            E_best_local = energies[best_idx];
            list_best_local = permut_lists[best_idx];

            if(acceptance(E_cur, E_best_local))
            {// accept the new solution
                E_cur = E_best_local;
                in_list = list_best_local;
            }
            else n_rej++;
            sa_hist.push_back(make_pair(in_list, E_cur));

            T_cur = T_cur*alpha;
            s_cur++;
        }
        return in_list;
    }

    ConnectionList sa_is(ConnectionList in_list, bool write_head)
    {
        // simulated annealing process
        s_cur = 0;
        T_cur = Tmax;
        n_rej = 0;
        Energy_is(in_list, num_pods, num_cores, num_specs, E_cur);
        write_log_head(write_head);
        while(T_cur>Tmin && s_cur<Smax && E_cur>0)
        {
            int i = 0;
            int E_best_local;
            ConnectionList list_best_local;

            int n_iters = num_iterations(); // n_iters*NUM_THREADS energy evaluations
            vector<ConnectionList> permut_lists;
            Row energies(n_iters*NUM_THREADS);
            for(int i=0; i<n_iters*NUM_THREADS; ++i){
                ConnectionList buffer_list(in_list.begin(), in_list.end());
                move_blender(buffer_list);
                permut_lists.push_back(buffer_list);
            }
            vector<thread> jobs(NUM_THREADS);
            for(int i=0; i<n_iters; ++i){
                for(int j=0; j<NUM_THREADS; ++j){
                    int k = i*NUM_THREADS+j;
                    jobs[j] = thread(Energy_is, permut_lists[k], num_pods,
                            num_cores, num_specs, ref(energies[k]));
                }
                for(int j=0; j<NUM_THREADS; ++j){
                    jobs[j].join();
                }
            }
            int best_idx = 0;
            for(int i=1; i<n_iters*NUM_THREADS; ++i){
                if(energies[best_idx]>energies[i]) best_idx = i;
            }
//            for(auto i:energies) cout<<i<<endl;
            E_best_local = energies[best_idx];
            list_best_local = permut_lists[best_idx];

            if(acceptance(E_cur, E_best_local))
            {// accept the new solution
                E_cur = E_best_local;
                in_list = list_best_local;
            }
            else n_rej++;
            sa_hist.push_back(make_pair(in_list, E_cur));

            T_cur = T_cur*alpha;
            s_cur++;
        }
        return in_list;
    }

    ConnectionList sa_is2(ConnectionList in_list, bool write_head)
    {
        // simulated annealing process
        s_cur = 0;
        T_cur = Tmax;
        n_rej = 0;
        Energy_is2(in_list, num_pods, num_cores, num_specs, E_cur);
        write_log_head(write_head);
        while(T_cur>Tmin && s_cur<Smax && E_cur>0)
        {
            int i = 0;
            int E_best_local;
            ConnectionList list_best_local;

            int n_iters = num_iterations(); // n_iters*NUM_THREADS energy evaluations
            vector<ConnectionList> permut_lists;
            Row energies(n_iters*NUM_THREADS);
            for(int i=0; i<n_iters*NUM_THREADS; ++i){
                ConnectionList buffer_list(in_list.begin(), in_list.end());
                move_blender(buffer_list);
                permut_lists.push_back(buffer_list);
            }
            vector<thread> jobs(NUM_THREADS);
            for(int i=0; i<n_iters; ++i){
                for(int j=0; j<NUM_THREADS; ++j){
                    int k = i*NUM_THREADS+j;
                    jobs[j] = thread(Energy_is2, permut_lists[k], num_pods,
                            num_cores, num_specs, ref(energies[k]));
                }
                for(int j=0; j<NUM_THREADS; ++j){
                    jobs[j].join();
                }
            }
            int best_idx = 0;
            for(int i=1; i<n_iters*NUM_THREADS; ++i){
                if(energies[best_idx]>energies[i]) best_idx = i;
            }
//            for(auto i:energies) cout<<i<<endl;
            E_best_local = energies[best_idx];
            list_best_local = permut_lists[best_idx];

            if(acceptance(E_cur, E_best_local))
            {// accept the new solution
                E_cur = E_best_local;
                in_list = list_best_local;
            }
            else n_rej++;
            sa_hist.push_back(make_pair(in_list, E_cur));

            T_cur = T_cur*alpha;
            s_cur++;
        }
        return in_list;
    }

    void sa_arch2(ConnectionList in_list, bool write_head)
    {
        // simulated annealing process with first fit core then slot
        s_cur = 0;
        T_cur = Tmax;
        n_rej = 0;
        Energy_arch2(in_list, num_pods, num_cores, num_specs, E_cur);
        write_log_head(write_head);
        while(T_cur>Tmin && s_cur<Smax && E_cur>0)
        {
            int i = 0;
            int E_best_local;
            ConnectionList list_best_local;

            int n_iters = num_iterations(); // n_iters*NUM_THREADS energy evaluations
            vector<ConnectionList> permut_lists;
            Row energies(n_iters*NUM_THREADS);
            for(int i=0; i<n_iters*NUM_THREADS; ++i){
                ConnectionList buffer_list(in_list.begin(), in_list.end());
                move_blender(buffer_list);
                permut_lists.push_back(buffer_list);
            }
            vector<thread> jobs(NUM_THREADS);
            for(int i=0; i<n_iters; ++i){
                for(int j=0; j<NUM_THREADS; ++j){
                    int k = i*NUM_THREADS+j;
                    jobs[j] = thread(Energy_arch2, permut_lists[k], num_pods,
                            num_cores, num_specs, ref(energies[k]));
                }
                for(int j=0; j<NUM_THREADS; ++j){
                    jobs[j].join();
                }
            }
            int best_idx = 0;
            for(int i=1; i<n_iters*NUM_THREADS; ++i){
                if(energies[best_idx]>energies[i]) best_idx = i;
            }
//            for(auto i:energies) cout<<i<<endl;
            E_best_local = energies[best_idx];
            list_best_local = permut_lists[best_idx];

            if(acceptance(E_cur, E_best_local))
            {// accept the new solution
                E_cur = E_best_local;
                in_list = list_best_local;
            }
            else n_rej++;
            sa_hist.push_back(make_pair(in_list, E_cur));

            T_cur = T_cur*alpha;
            s_cur++;
        }
    }

/************************ Optimize *************************/
    void find_tfkonpod()
    {
        vector<vector<int>> tfk_on_pod(num_pods);
        for(int i=0; i<num_pods; ++i){
            for(int j=0; j<num_cnk; ++j){
                if(connection_list[j].src==i||connection_list[j].dst==j){
                    tfk_on_pod[i].push_back(j);
                }
            }
        }
        this->tfk_on_pod = tfk_on_pod;
    }

    // void Model_routing()
    // {
    //     GRBEnv env = GRBEnv();
    //     GRBModel model = GRBModel(env);

    //     map<tuple<int, int, int>, GRBVar> core_usage; // (cnk,src/dst,core)
    //     for(int i=0; i<num_cnk; ++i){
    //         for(int j=0; j<num_cores; ++j){
    //             int src = connection_list[i].src;
    //             int dst = connection_list[i].dst;
    //             core_usage[make_tuple(i,src,j)] = model.addVar(0,1,0,GRB_BINARY);
    //             core_usage[make_tuple(i,dst,j)] = model.addVar(0,1,0,GRB_BINARY);
    //         }
    //     }
    //     model.update();

    //     int bigM = 9999;
    //     GRBVar flow[num_pods][num_cores]; // (pod,core)
    //     for(int i=0; i<num_pods; ++i){
    //         for(int j=0; j<num_cores; ++j){
    //             flow[i][j] = model.addVar(0,bigM,0,GRB_CONTINUOUS);
    //             model.update();
    //         }
    //     }


    //     GRBVar flow_max[num_pods]; // (pod)
    //     for(int i=0; i<num_pods; ++i){
    //         flow_max[i] = model.addVar(0,bigM,1,GRB_CONTINUOUS);
    //     }

    //     model.update();

    //     for(int i=0; i<num_cnk; ++i){
    //         GRBLinExpr expr1,expr2;
    //         expr1=0;
    //         expr2=0;
    //         int src = connection_list[i].src;
    //         int dst = connection_list[i].dst;
    //         for(int j=0; j<num_cores; ++j){
    //             expr1 += core_usage[make_tuple(i,src,j)];
    //             expr2 += core_usage[make_tuple(i,dst,j)];
    //         }
    //         model.addConstr(expr1==1);
    //         model.addConstr(expr2==1);
    //     }

    //     model.update();

    //     find_tfkonpod();
    //     for(int i=0; i<num_pods; ++i){
    //         for(int j=0; j<num_cores; ++j){
    //             GRBLinExpr expr=0;
    //             for(int k=0; k<tfk_on_pod[i].size(); ++k){
    //                 expr+=core_usage[make_tuple(tfk_on_pod[i][k],i,j)];
    //             }
    //             try{
    //                 model.addConstr(expr<=100);
    //                 model.addConstr(10<=flow[i][j]);
    //             } catch(GRBException e){
    //                 cout<< "Error code = " <<e.getErrorCode()<<endl;
    //                 cout<<e.getMessage()<<endl;
    //             }

    //         }
    //     }

    //     // model.getEnv().set(GRB_DoubleParam_TimeLimit, 200);
    //     // model.getEnv().set(GRB_IntParam_MIPFocus, 1);
    //     model.update();
    //     model.optimize();
    // }

};

void print3dTensor(const Tensor3d_bool &res)
{
    for(size_t i=0; i<res.size(); ++i)
    {
        cout<<"POD "<<i<<endl;
        for(size_t j=0; j<res[i].size(); ++j)
        {
            for(size_t k=0; k<res[i][j].size(); ++k)
            {
                cout<<setw(1)<<res[i][j][k];
            }
            cout<<endl;
        }
        cout<<endl;
    }
}