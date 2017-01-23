#include "../../heuristics/sa_sdm.h"

typedef vector<float> RowFloat;
typedef vector<RowFloat> MatrixFloat;

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
    int step_ini = 100;
    float step_delta = 0.99;
    int n_iter_ini = 5;
    float n_iter_delta = 1.01;
    float prob1 = 1;
    float prob2 = 1;

    int num_pods = 100;
    int total_cnk = num_pods*(num_pods-1)*load;
    int min_cnk = max(float(1), 2*(num_pods-1)*load-num_pods);
    int max_cnk = 2*(num_pods-1)*load - min_cnk;

    int num_batch = 5;

    // (connections or throughput or hybrid)X(forward, backward, sa)
    MatrixFloat arch2_ff1(num_batch, RowFloat(9)), arch2_ff2(num_batch, RowFloat(9)), arch2_sa(num_batch, RowFloat(9));
    MatrixFloat arch4(num_batch, RowFloat(9));
    MatrixFloat arch5(num_batch, RowFloat(9));

    string trafficname = "traffic_matrix_";
    for(int id=0; id<5; ++id){
        Traffic t(trafficname, id, num_pods, max_cnk, min_cnk, load, tfk_mean, 
            tfk_var, cpst_slot, gb_slot, num_cores, num_specs);
        string filename = "traffic_matrix__matrix_"+to_string(id)+".csv";
        cout<<filename<<endl;
        t.read_traffic(filename,25);

        int num_cnk = t.num_cnk;
        cout<<num_cnk<<endl;

        float tmp;
        ConnectionList reverselist{t.connection_list.begin(), t.connection_list.end()};
        reverse(reverselist.begin(), reverselist.end());
        ConnectionList in_list{t.connection_list.begin(), t.connection_list.end()};

        // connections
        float alpha = 1;
        float beta = 0;

        // reverse list
        // architecture 2
        Energy_hybrid(reverselist, num_pods, num_cores, num_specs, alpha, beta, tmp);
        arch2_connection_rev.push_back(-ea2b1);.
        Energy_arch4_new_hybrid(reverselist, num_pods, num_cores, num_specs, alpha, beta, ea4b1);
        arch4_connection_rev.push_back(-ea4b1);
        Energy_arch5_hybrid(reverselist, num_pods, num_cores, num_specs, alpha, beta, ea5b1);
        arch5_connection_rev.push_back(-ea5b1);
        cout<<"Connections Reverse"<<endl;
        cout<<arch2_connection_rev[id]<<"|"<<arch4_connection_rev[id]<<"|"<<arch5_connection_rev[id]<<endl;

        // ordinary list
        Energy_hybrid(in_list, num_pods, num_cores, num_specs, alpha, beta, ea2b2);
        arch2_connection_in.push_back(-ea2b2);
        Energy_arch4_new_hybrid(in_list, num_pods, num_cores, num_specs, alpha, beta, ea4b2);
        arch4_connection_in.push_back(-ea4b2);
        Energy_arch5_hybrid(in_list, num_pods, num_cores, num_specs, alpha, beta, ea5b2);
        arch5_connection_in.push_back(-ea5b2);
        cout<<"Connections Sorted"<<endl;
        cout<<arch2_connection_in[id]<<"|"<<arch4_connection_in[id]<<"|"<<arch5_connection_in[id]<<endl;

        alpha = 0;
        beta = 0.01;
        float a, b, c, d, e, f;
        // reverse list
        Energy_hybrid(reverselist, num_pods, num_cores, num_specs, alpha, beta, a);
        arch2_throughput_rev.push_back(-a);
        Energy_arch4_new_hybrid(reverselist, num_pods, num_cores, num_specs, alpha, beta, b);
        arch4_throughput_rev.push_back(-b);
        Energy_arch5_hybrid(reverselist, num_pods, num_cores, num_specs, alpha, beta, c);
        arch5_throughput_rev.push_back(-c);
        cout<<"Throughput Reverse"<<endl;
        cout<<arch2_throughput_rev[id]<<"|"<<arch4_throughput_rev[id]<<"|"<<arch5_throughput_rev[id]<<endl;

        // ordinary list
        Energy_hybrid(in_list, num_pods, num_cores, num_specs, alpha, beta, d);
        arch2_throughput_in.push_back(-d);
        Energy_arch4_new_hybrid(in_list, num_pods, num_cores, num_specs, alpha, beta, e);
        arch4_throughput_in.push_back(-e);
        Energy_arch5_hybrid(in_list, num_pods, num_cores, num_specs, alpha, beta, f);
        arch5_throughput_in.push_back(-f);
        cout<<"Throughput Sorted"<<endl;
        cout<<arch2_throughput_in[id]<<"|"<<arch4_throughput_in[id]<<"|"<<arch5_throughput_in[id]<<endl;


        // ConnectionList order = t.bench_ajmal_arch2(reverselist, ea2b2);
        // arch2_bench2.push_back(num_cnk-ea2b2);
        // t.bench_ajmal_arch4(reverselist, ea4b2);
        // arch4_bench2.push_back(num_cnk-ea4b2);
        // t.bench_ajmal_arch5(order, 0, ea5b2);
        // arch5_bench2.push_back(num_cnk-ea5b2);
        // cout<<arch2_bench2[id]<<"|"<<arch4_bench2[id]<<"|"<<arch5_bench2[id]<<endl;

        /*SA*/
        // int ea1s, ea2s, ea4s, ea5s;
        // t.set_probs(prob1, prob2);
        // t.schedule(Tmax, Tmin, Smax, alpha, step_ini, step_delta, n_iter_ini, n_iter_delta);
        // bool flag_write = false;
        // in_list = t.connection_list;
        // t.sais_arch2(in_list, flag_write, ea2s);
        // arch2_sa.push_back(num_cnk-ea2s);
        // in_list = t.connection_list;
        // t.sais_arch4(in_list, flag_write, ea4s);
        // arch4_sa.push_back(num_cnk-ea4s);
        // in_list = t.connection_list;
        // t.sais_arch5(in_list, flag_write, ea5s);
        // arch5_sa.push_back(num_cnk-ea5s);
        // cout<<arch2_sa[id]<<"|"<<arch4_sa[id]<<"|"<<arch5_sa[id]<<endl;
    }
    // string filename = "result_sa.csv";
    // ofstream myfile;
    // myfile.open(filename);
    // myfile<<"Arch2_bench1,"<<"Arch2_bench2,"<<"Arch2_sa,"<<"Arch4_bench1,"<<"Arch4_bench2,"<<"Arch4_sa,"<<"Arch5_bench1,"<<"Arch5_bench2,"<<"Arch5_sa,"<<endl;
    // for(int i=0; i<20; ++i){
    //     myfile<<arch2_bench1[i]<<","<<arch2_bench2[i]<<","<<arch2_sa[i]<<","<<arch4_bench1[i]<<","<<arch4_bench2[i]<<","<<arch4_sa[i]<<","<<arch5_bench1[i]<<","<<arch5_bench2[i]<<","<<arch5_sa[i]<<","<<endl;
    // }
    // myfile.close();
}
