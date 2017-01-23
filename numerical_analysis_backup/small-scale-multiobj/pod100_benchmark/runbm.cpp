// benchmarks

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

    int num_batch = 20;

    // (connections or throughput)X(forward, backward)
    MatrixFloat arch2(num_batch, RowFloat(8));
    MatrixFloat arch4(num_batch, RowFloat(8));
    MatrixFloat arch5(num_batch, RowFloat(8));
    MatrixFloat arch1(num_batch, RowFloat(8));

    string trafficname = "traffic_matrix_";
    for(int id=0; id<num_batch; ++id){
        // read traffic matrix
        Traffic t(trafficname, id, num_pods, max_cnk, min_cnk, load, tfk_mean, 
            tfk_var, cpst_slot, gb_slot, num_cores, num_specs);
        string filename = "traffic_matrix__matrix_"+to_string(id)+".csv";
        cout<<filename<<endl;
        t.read_traffic(filename,25);

        int num_cnk = t.num_cnk;
        cout<<num_cnk<<endl;

        float tmp, tmp1, tmp2, tmp3;
        int tmpint1, tmpint2;
        ConnectionList reverselist{t.connection_list.begin(), t.connection_list.end()};
        reverse(reverselist.begin(), reverselist.end());
        ConnectionList inlist{t.connection_list.begin(), t.connection_list.end()};

        // connections


        // reverse list
        // architecture 2, connection
        float alpha = 1;
        float beta = 0;
        Energy_hybrid(inlist, num_pods, num_cores, num_specs, alpha, beta, tmp);
        arch2[id][0] = -tmp;
        Energy_hybrid(reverselist, num_pods, num_cores, num_specs, alpha, beta, tmp);
        arch2[id][1] = -tmp;
        // architecture 2, throughput
        alpha = 0;
        beta = 1;
        // sort(inlist.begin(), inlist.end());
        Energy_hybrid(inlist, num_pods, num_cores, num_specs, alpha, beta, tmp);
        arch2[id][2] = -tmp;
        // reverselist = reverse(t.connection_list.begin(), t.connection_list.end());
        Energy_hybrid(reverselist, num_pods, num_cores, num_specs, alpha, beta, tmp);
        arch2[id][3] = -tmp;
        // ajmal backward
        // reverselist = reverse(t.connection_list.begin(), t.connection_list.end());
        t.bench_ajmal_arch2(reverselist, tmpint1, tmp1);
        // ajmal forward
        // inlist = sort(t.connection_list.begin(), t.connection_list.end());
        t.bench_ajmal_arch2_new(inlist, tmpint2, tmp3);
        arch2[id][4] = num_cnk-tmpint2;
        arch2[id][5] = num_cnk-tmpint1;
        arch2[id][6] = tmp3;
        arch2[id][7] = tmp1;
        cout<<"Architecture 2"<<endl;
        cout<<arch2[id][0]<<"|"<<arch2[id][1]<<"|"<<arch2[id][2]<<"|"<<arch2[id][3]
        <<"|"<<arch2[id][4]<<"|"<<arch2[id][5]<<"|"<<arch2[id][6]<<"|"<<arch2[id][7]<<endl;

        // architecture 4, connection
        alpha = 1;
        beta = 0;
        Energy_arch4_new_hybrid(inlist, num_pods, num_cores, num_specs, alpha, beta, tmp);
        arch4[id][0] = -tmp;
        Energy_arch4_new_hybrid(reverselist, num_pods, num_cores, num_specs, alpha, beta, tmp);
        arch4[id][1] = -tmp;
        // architecture 4, throughput
        alpha = 0;
        beta = 1;
        Energy_arch4_new_hybrid(inlist, num_pods, num_cores, num_specs, alpha, beta, tmp);
        arch4[id][2] = -tmp;
        Energy_arch4_new_hybrid(reverselist, num_pods, num_cores, num_specs, alpha, beta, tmp);
        arch4[id][3] = -tmp;
        // ajmal backward
        // reverselist = reverse(t.connection_list.begin(), t.connection_list.end());
        t.bench_ajmal_arch4(reverselist, tmpint1, tmp1);
        // ajmal forward
        // inlist = sort(t.connection_list.begin(), t.connection_list.end());
        t.bench_ajmal_arch4_new(inlist, tmpint2, tmp3);
        arch4[id][4] = num_cnk-tmpint2;
        arch4[id][5] = num_cnk-tmpint1;
        arch4[id][6] = tmp3;
        arch4[id][7] = tmp1;
        cout<<"Architecture 4"<<endl;
        cout<<arch4[id][0]<<"|"<<arch4[id][1]<<"|"<<arch4[id][2]<<"|"<<arch4[id][3]
        <<"|"<<arch4[id][4]<<"|"<<arch4[id][5]<<"|"<<arch4[id][6]<<"|"<<arch4[id][7]<<endl;

        // architecture 5, connection
        alpha = 1;
        beta = 0;
        Energy_arch5_hybrid(inlist, num_pods, num_cores, num_specs, alpha, beta, tmp);
        arch5[id][0] = -tmp;
        Energy_arch5_hybrid(reverselist, num_pods, num_cores, num_specs, alpha, beta, tmp);
        arch5[id][1] = -tmp;
        // throughput
        alpha = 0;
        beta = 1;
        Energy_arch5_hybrid(inlist, num_pods, num_cores, num_specs, alpha, beta, tmp);
        arch5[id][2] = -tmp;
        Energy_arch5_hybrid(reverselist, num_pods, num_cores, num_specs, alpha, beta, tmp);
        arch5[id][3] = -tmp;
        // ajmal backward
        // reverselist = reverse(t.connection_list.begin(), t.connection_list.end());
        t.bench_ajmal_arch5(reverselist, 0, tmpint1, tmp1);
        // ajmal forward
        // inlist = sort(t.connection_list.begin(), t.connection_list.end());
        t.bench_ajmal_arch5_new(inlist, 0,  tmpint2, tmp3);
        arch5[id][4] = num_cnk-tmpint2;
        arch5[id][5] = num_cnk-tmpint1;
        arch5[id][6] = tmp3;
        arch5[id][7] = tmp1;
        cout<<"Architecture 5"<<endl;
        cout<<arch5[id][0]<<"|"<<arch5[id][1]<<"|"<<arch5[id][2]<<"|"<<arch5[id][3]
        <<"|"<<arch5[id][4]<<"|"<<arch5[id][5]<<"|"<<arch5[id][6]<<"|"<<arch5[id][7]<<endl;
    }
    string filename = "result_benchmark.csv";
    ofstream myfile;
    myfile.open(filename);
    myfile
    <<"Arch2_FF_fwd_cnk,"<<"Arch2_FF_fwd_thp,"
    <<"Arch2_FF_bkw_cnk,"<<"Arch2_FF_bkw_thp,"
    <<"Arch2_AJ_fwd_cnk,"<<"Arch2_AJ_bkw_thp,"
    <<"Arch2_AJ_bwd_cnk,"<<"Arch2_AJ_bkw_thp,"
    <<"Arch4_FF_fwd_cnk,"<<"Arch4_FF_fwd_thp,"
    <<"Arch4_FF_bkw_cnk,"<<"Arch4_FF_bkw_thp,"
    <<"Arch4_AJ_fwd_cnk,"<<"Arch4_AJ_bkw_thp,"
    <<"Arch4_AJ_bwd_cnk,"<<"Arch4_AJ_bkw_thp,"
    <<"Arch5_FF_fwd_cnk,"<<"Arch5_FF_fwd_thp,"
    <<"Arch5_FF_bkw_cnk,"<<"Arch5_FF_bkw_thp,"
    <<"Arch5_AJ_fwd_cnk,"<<"Arch5_AJ_bkw_thp,"
    <<"Arch5_AJ_bwd_cnk,"<<"Arch5_AJ_bkw_thp,"<<endl;
    for(int i=0; i<20; ++i){
        myfile
        <<arch2[i][0]<<","<<arch2[i][2]<<","
        <<arch2[i][1]<<","<<arch2[i][3]<<","
        <<arch2[i][4]<<","<<arch2[i][6]<<","
        <<arch2[i][5]<<","<<arch2[i][7]<<","
        <<arch4[i][0]<<","<<arch4[i][2]<<","
        <<arch4[i][1]<<","<<arch4[i][3]<<","
        <<arch4[i][4]<<","<<arch4[i][6]<<","
        <<arch4[i][5]<<","<<arch4[i][7]<<","
        <<arch5[i][0]<<","<<arch5[i][2]<<","
        <<arch5[i][1]<<","<<arch5[i][3]<<","
        <<arch5[i][4]<<","<<arch5[i][6]<<","
        <<arch5[i][5]<<","<<arch5[i][7]<<","
        <<endl;
    }
    myfile.close();
}
