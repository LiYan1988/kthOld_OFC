#include "../../heuristics/sa_sdm_hybrid.h"

typedef vector<float> RowFloat;
typedef vector<RowFloat> MatrixFloat;

int main()
{
    srand(0);
    float load = 0.5;
    int tfk_mean = 200;
    int tfk_var = 200;
    int cpst_slot = 25;
    int gb_slot = 1;
    int num_cores = 10;
    int num_specs = 320;
    float Tmax = 5;
    float Tmin = 1;
    float alpha = 0.9999;
    int Smax = 25;
    int step_ini = 100;
    float step_delta = 0.95;
    int n_iter_ini = 100;
    float n_iter_delta = 1;
    float prob1 = 1;
    float prob2 = 1;

    int num_pods = 250;
    int min_cnk = max(float(1), 2*(num_pods-1)*load-num_pods);
    int max_cnk = 2*(num_pods-1)*load - min_cnk;

    string trafficname = "traffic_matrix_";
    int N=1; // number of cores
    int M=2; // number of matrices
    Matrix total_cnk(N, Row(M, 0));
    Row total_connections(N,0);
    MatrixFloat arch2_fwd_connections(N, RowFloat(M));
    MatrixFloat arch2_fwd_throughput(N, RowFloat(M));
    MatrixFloat arch2_fwd_hybrid(N, RowFloat(M));
    MatrixFloat arch2_bwd_connections(N, RowFloat(M));
    MatrixFloat arch2_bwd_throughput(N, RowFloat(M));
    MatrixFloat arch2_bwd_hybrid(N, RowFloat(M));

    MatrixFloat arch4_fwd_connections(N, RowFloat(M));
    MatrixFloat arch4_fwd_throughput(N, RowFloat(M));
    MatrixFloat arch4_fwd_hybrid(N, RowFloat(M));
    MatrixFloat arch4_bwd_connections(N, RowFloat(M));
    MatrixFloat arch4_bwd_throughput(N, RowFloat(M));
    MatrixFloat arch4_bwd_hybrid(N, RowFloat(M));

    MatrixFloat arch5_fwd_connections(N, RowFloat(M));
    MatrixFloat arch5_fwd_throughput(N, RowFloat(M));
    MatrixFloat arch5_fwd_hybrid(N, RowFloat(M));
    MatrixFloat arch5_bwd_connections(N, RowFloat(M));
    MatrixFloat arch5_bwd_throughput(N, RowFloat(M));
    MatrixFloat arch5_bwd_hybrid(N, RowFloat(M));

    for(int id=0; id<N; ++id){
        num_cores = 1+id;
        step_ini = num_pods;

        for(int rep=0; rep<M; ++rep){
            Traffic t(trafficname, num_cores-1, num_pods, max_cnk, min_cnk, load, tfk_mean, 
                tfk_var, cpst_slot, gb_slot, num_cores, num_specs);
            string filename = "traffic_matrix__matrix_"+to_string(rep)+".csv";
            cout<<filename<<endl;
            t.read_traffic(filename,25);
            total_connections[id] = t.num_cnk;

            float tmp, tmp1, tmp2, tmp3;
            int tmpint1, tmpint2;
            ConnectionList reverselist{t.connection_list.begin(), t.connection_list.end()};
            reverse(reverselist.begin(), reverselist.end());
            ConnectionList inlist{t.connection_list.begin(), t.connection_list.end()};

            // arch 2, forward
            float alpha=1;
            float beta=0;
            Energy_arch2_hybrid(inlist, num_pods, num_cores, num_specs, alpha, beta, tmp);
            arch2_fwd_connections[id][rep] = tmp;
            cout<<tmp<<endl;
            alpha=0;
            beta=1;
            Energy_arch2_hybrid(inlist, num_pods, num_cores, num_specs, alpha, beta, tmp);
            arch2_fwd_throughput[id][rep] = tmp;
            cout<<tmp<<endl;
            // arch 2, backward
            alpha=1;
            beta=0;
            Energy_arch2_hybrid(reverselist, num_pods, num_cores, num_specs, alpha, beta, tmp);
            arch2_bwd_connections[id][rep] = tmp;
            cout<<tmp<<endl;
            alpha=0;
            beta=1;
            Energy_arch2_hybrid(reverselist, num_pods, num_cores, num_specs, alpha, beta, tmp);
            arch2_bwd_throughput[id][rep] = tmp;
            cout<<tmp<<endl;

            // arch 5, forward
            alpha=1;
            beta=0;
            Energy_arch5_hybrid(inlist, num_pods, num_cores, num_specs, alpha, beta, tmp);
            arch5_fwd_connections[id][rep] = tmp;
            cout<<tmp<<endl;
            alpha=0;
            beta=1;
            Energy_arch5_hybrid(inlist, num_pods, num_cores, num_specs, alpha, beta, tmp);
            arch5_fwd_throughput[id][rep] = tmp;
            cout<<tmp<<endl;
            // arch 5, backward
            alpha=1;
            beta=0;
            Energy_arch5_hybrid(reverselist, num_pods, num_cores, num_specs, alpha, beta, tmp);
            arch5_bwd_connections[id][rep] = tmp;
            cout<<tmp<<endl;
            alpha=0;
            beta=1;
            Energy_arch5_hybrid(reverselist, num_pods, num_cores, num_specs, alpha, beta, tmp);
            arch5_bwd_throughput[id][rep] = tmp;
            cout<<tmp<<endl;

            // arch 4, forward
            alpha=1;
            beta=0;
            Energy_arch4_hybrid(inlist, num_pods, num_cores, num_specs, alpha, beta, tmp);
            arch4_fwd_connections[id][rep] = tmp;
            cout<<tmp<<endl;
            alpha=0;
            beta=1;
            Energy_arch4_hybrid(inlist, num_pods, num_cores, num_specs, alpha, beta, tmp);
            arch4_fwd_throughput[id][rep] = tmp;
            cout<<tmp<<endl;
            // arch 4, backward
            alpha=1;
            beta=0;
            Energy_arch4_hybrid(reverselist, num_pods, num_cores, num_specs, alpha, beta, tmp);
            arch4_bwd_connections[id][rep] = tmp;
            cout<<tmp<<endl;
            alpha=0;
            beta=1;
            Energy_arch4_hybrid(reverselist, num_pods, num_cores, num_specs, alpha, beta, tmp);
            arch4_bwd_throughput[id][rep] = tmp;
            cout<<tmp<<endl;
        }
    }
    ofstream myfile;
    myfile.open("test.csv");
    myfile<<"ok"<<endl;
    myfile.close();

    // string filename = "runcore.csv";
    // cout<<filename<<endl;
    // ofstream myfile;
    // myfile<<"arch2_fwd_connections,"<<"arch2_fwd_throughput,"
    //     <<"arch2_bwd_connections,"<<"arch2_bwd_throughput,"
    //     <<"arch4_fwd_connections,"<<"arch4_fwd_throughput,"
    //     <<"arch4_bwd_connections,"<<"arch4_bwd_throughput,"
    //     <<"arch5_fwd_connections,"<<"arch5_fwd_throughput,"
    //     <<"arch5_bwd_connections,"<<"arch5_bwd_throughput,"<<endl;
    // for(int id=0; id<N; ++id){
    //     for(int rep=0; rep<M; ++rep){
    //         myfile<<arch2_fwd_connections[id][rep]<<","
    //         <<arch2_fwd_throughput[id][rep]<<","
    //         <<arch2_bwd_connections[id][rep]<<","
    //         <<arch2_bwd_throughput[id][rep]<<","
    //         <<arch4_fwd_connections[id][rep]<<","
    //         <<arch4_fwd_throughput[id][rep]<<","
    //         <<arch4_bwd_connections[id][rep]<<","
    //         <<arch4_bwd_throughput[id][rep]<<","
    //         <<arch5_fwd_connections[id][rep]<<","
    //         <<arch5_fwd_throughput[id][rep]<<","
    //         <<arch5_bwd_connections[id][rep]<<","
    //         <<arch5_bwd_throughput[id][rep]<<endl;
    //     }
    // }
    // myfile.close();
}
