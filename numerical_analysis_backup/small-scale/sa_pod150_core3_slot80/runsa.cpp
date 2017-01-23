#include "sa_sdm.h"

int main()
{
    srand(0);
    float load = 0.2;
    int tfk_mean = 200;
    int tfk_var = 200;
    int cpst_slot = 25;
    int gb_slot = 1;
    int num_cores = 3;
    int num_specs = 80;
    float Tmax = 5;
    float Tmin = 1;
    float alpha = 0.9999;
    int Smax = 50;
    int step_ini = 150;
    float step_delta = 0.99;
    int n_iter_ini = 200;
    float n_iter_delta = 1.05;
    float prob1 = 1;
    float prob2 = 1;

    int num_pods = 150;
    int total_cnk = num_pods*(num_pods-1)*load;
    int min_cnk = max(float(1), 2*(num_pods-1)*load-num_pods);
    int max_cnk = 2*(num_pods-1)*load - min_cnk;

    Row arch2_bench1, arch2_bench2, arch2_sa;
    Row arch4_bench1, arch4_bench2, arch4_sa;
    Row arch5_bench1, arch5_bench2, arch5_sa;

    string trafficname = "traffic_matrix_";
    for(int id=0; id<20; ++id){
        Traffic t(trafficname, id, num_pods, max_cnk, min_cnk, load, tfk_mean, 
            tfk_var, cpst_slot, gb_slot, num_cores, num_specs);
        string filename = "traffic_matrix__matrix_"+to_string(id)+".csv";
        cout<<filename<<endl;
        t.read_traffic(filename,25);

        int num_cnk = t.num_cnk;
        cout<<num_cnk<<endl;

        int ea2b1, ea2b2, ea4b1, ea4b2, ea5b1, ea5b2;
        ConnectionList reverselist{t.connection_list.begin(), t.connection_list.end()};
        reverse(reverselist.begin(), reverselist.end());
        ConnectionList in_list{t.connection_list.begin(), t.connection_list.end()};

        Energy_arch2(reverselist, num_pods, num_cores, num_specs,ea2b1);
        arch2_bench1.push_back(num_cnk-ea2b1);
        Energy_arch4(reverselist, num_pods, num_cores, num_specs, ea4b1);
        arch4_bench1.push_back(num_cnk-ea4b1);
        Energy_arch5(reverselist, num_pods, num_cores, num_specs, ea5b1);
        arch5_bench1.push_back(num_cnk-ea5b1);
        cout<<arch2_bench1[id]<<"|"<<arch4_bench1[id]<<"|"<<arch5_bench1[id]<<endl;

        ConnectionList order = t.bench_ajmal_arch2(reverselist, ea2b2);
        arch2_bench2.push_back(num_cnk-ea2b2);
        t.bench_ajmal_arch4(reverselist, ea4b2);
        arch4_bench2.push_back(num_cnk-ea4b2);
        t.bench_ajmal_arch5(order, 0, ea5b2);
        arch5_bench2.push_back(num_cnk-ea5b2);
        cout<<arch2_bench2[id]<<"|"<<arch4_bench2[id]<<"|"<<arch5_bench2[id]<<endl;

        /*SA*/
        int ea1s, ea2s, ea4s, ea5s;
        t.set_probs(prob1, prob2);
        t.schedule(Tmax, Tmin, Smax, alpha, step_ini, step_delta, n_iter_ini, n_iter_delta);
        bool flag_write = false;
        in_list = t.connection_list;
        t.sais_arch2(in_list, flag_write, ea2s);
        arch2_sa.push_back(num_cnk-ea2s);
        in_list = t.connection_list;
        t.sais_arch4(in_list, flag_write, ea4s);
        arch4_sa.push_back(num_cnk-ea4s);
        in_list = t.connection_list;
        t.sais_arch5(in_list, flag_write, ea5s);
        arch5_sa.push_back(num_cnk-ea5s);
        cout<<arch2_sa[id]<<"|"<<arch4_sa[id]<<"|"<<arch5_sa[id]<<endl;
    }
    string filename = "result_sa.csv";
    ofstream myfile;
    myfile.open(filename);
    myfile<<"Arch2_bench1,"<<"Arch2_bench2,"<<"Arch2_sa,"<<"Arch4_bench1,"<<"Arch4_bench2,"<<"Arch4_sa,"<<"Arch5_bench1,"<<"Arch5_bench2,"<<"Arch5_sa,"<<endl;
    for(int i=0; i<20; ++i){
        myfile<<arch2_bench1[i]<<","<<arch2_bench2[i]<<","<<arch2_sa[i]<<","<<arch4_bench1[i]<<","<<arch4_bench2[i]<<","<<arch4_sa[i]<<","<<arch5_bench1[i]<<","<<arch5_bench2[i]<<","<<arch5_sa[i]<<","<<endl;
    }
    myfile.close();
}
