#include <random>


using namespace std;

class Connection{
public:
	int total_slots; // without guardband
	int nc;
	int ns;
	int src;
	int dst;
	int gb;
	vector<int> possible_cores;
	Connection()
};