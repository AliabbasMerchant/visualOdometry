#include <cmath>

#include <limits>

#include <queue>


using namespace std;

//node class
class Node {
  
  public: 
    int idx; //index
    float cost; // cost of traversal
   
  Node(int i, float c){

    idx=i;
    cost=c;

  };

};

//op overloading nodes comparison ops
bool operator<(const Node &n1, const Node &n2) {
  return n1.cost > n2.cost;
}

//op overloading nodes eq ops
bool operator==(const Node &n1, const Node &n2) {
  return n1.idx == n2.idx;
}

// finding the distance
float norm(int i0, int j0, int i1, int j1) {
  return abs(i0 - i1) + abs(j0 - j1);
}


// weights:        cost grid
// h, w:           height, width of grid
// start, goal:    index of start/goal in grid
// paths (output): for each node, stores previous node in path

extern "C" bool astar(float* weights, int h, int w, int start, int goal, int* paths) {

  const float INF = numeric_limits<float>::infinity();

  Node start_node(start, 0.);

  Node goal_node(goal, 0.);

  float* costs = new float[h * w];

  for (int i = 0; (i < h * w) ; ++i)
  {

    costs[i] = INF;
  
  }

  costs[start] = 0.;

  priority_queue<Node> nodes_to_visit;
  
  nodes_to_visit.push(start_node);

  int* nbrs = new int[8];

  bool sol = false;
  
  while (!nodes_to_visit.empty()) {

    Node cur = nodes_to_visit.top();

    if (cur == goal_node) {
      sol = true;
      break;
    }

    nodes_to_visit.pop();

    int row = cur.idx / w;
  
    int col = cur.idx % w;
  
    // check bounds and find neighbors
  
    nbrs[0] = -1;

    nbrs[1] = (row > 0)? (cur.idx - w): -1;

    nbrs[2] = -1;

    nbrs[3] = (col > 0) ? (cur.idx - 1): -1;

    nbrs[4] = (col + 1 < w) ? (cur.idx + 1 ): -1;

    nbrs[5] = -1;

    nbrs[6] = (row + 1 < h) ? (cur.idx + w ): -1;

    nbrs[7] = -1;

    float heuristic_cost;
    for (int i = 0; i < 8; ++i) 
    {

      if (nbrs[i] >= 0) //not -1
      {

        // the sum of the cost so far and the cost of move
        float new_cost = costs[cur.idx] + weights[nbrs[i]];

        if (new_cost < costs[nbrs[i]]) 
        {
          // estimate cost to goal with moves allowed          
          heuristic_cost = norm(nbrs[i] / w, nbrs[i] % w,
                                       goal    / w, goal    % w);

          // paths with lower cost are explored first
          float priority = new_cost + heuristic_cost;

          nodes_to_visit.push(Node(nbrs[i], priority));

          costs[nbrs[i]] = new_cost;
          
          paths[nbrs[i]] = cur.idx;

        }
      }
    }
  }

  delete[] costs;
  delete[] nbrs;
  // g++ -shared -o astar.so -fPIC cppastar.cpp
  return sol;
}
