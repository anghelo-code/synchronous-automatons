#include <iostream>
#include <cstdlib>
#include <string>
#include <list>

using namespace std;

// To store the input automaton in memory
int    n;        // Vertices from 0 to (n - 1)
int    k;        // Alphabet from 'a' to 'a' + (k - 1)
int  **D;        // Transition matrix

// For higher efficiency we need the transpose of D
int  **T;        

// G is the transpose of the underlying grph of the square-automaton
struct Arc {
  int  s;        // s = i * n + j is tip of this arc, it encodes the pair (i, j)
  char c;        // c is the label of this arc
  Arc *next;
};

Arc **G;

// After a breath-first-search starting from all pairs (i, i):
int *p;         // p[u] = v means that u was "found" through v
char *first;    // first[u] is the first character in a shortest word syncronizing u
int *dist;      // dist[u] is the length of the sortest word syncronizing u

void read_input() {
  cin >> n;
  cin >> k;

  D = new int * [n];

  for (int i = 0; i < n; i ++) {
    D[i] = new int [k];
    for (int j = 0; j < k; j ++)
      cin >> D[i][j];
  }
}

void fill_T() {
  T = new int * [k];

  for (int i = 0; i < k; i ++) {
    T[i] = new int [n];
    for (int j = 0; j < n; j ++)
      T[i][j] = D[j][i];
  }
}

void fill_G() {
  G = new Arc * [n * n];
  for (int s = 0; s < n * n; G[s ++] = NULL);

  for (int a = 0; a < n; a ++)
    for (int b = a; b < n; b ++)
      for (int j = 0; j < k; j ++) {
	int s = a * n + b; 
	int c = D[a][j];
	int d = D[b][j];
	int t = (c > d) ? d * n + c : c * n + d;
	Arc *tmp = new Arc;
	tmp->s = s;
	tmp->c = j;
	tmp->next = G[t];
	G[t] = tmp;
      }     
}

bool is_synchronizing() {
  int N = n * n;
  list<int> queue;                    
  bool visited [N];

  p = new int [n * n];
  first = new char [n * n];
  dist = new int [n * n];

  // Initializes the breath-fisrt-search
  for (int s = 0; s < N; s ++) {
    p[s] = -1;
    visited[s] = false;
    dist[s] = N;
  }
  
  for (int i = 0; i < n; i ++) {
    int s = i * n + i;
    p[s] = s;
    visited[s] = true;
    dist[s] = 0;
    queue.push_back(s);
  }

  // Breath-fisrt-search
  while (!queue.empty()) {
    int s = queue.front();
    queue.pop_front();
    for (Arc *tmp = G[s]; tmp != NULL; tmp = tmp->next) {
      int t = tmp->s;
      if (!visited[t]) {
	visited[t] = true;
	dist[t] = dist[s] + 1;
	p[t] = s;
	first[t] = tmp->c;
	queue.push_back(t);
      }
    }
  }

  /* Debug 
  for (int a = 0; a < n; a ++) {
    for (int b = 0; b <= a; b ++)
      cout << "  ";
    for (int b = a + 1; b < n; b ++) 
      cout << string(1, 'a' + first[a * n + b]) << " ";
    cout << endl;
  }

  cout << endl;
  for (int a = 0; a < n; a ++)
    for (int b = a + 1; b < n; b ++) {
      int t = p[a * n + b];
      int c = t / n, d = t % n;
      cout << a << ", " << b << " --> " << c << ", " << d << endl;
    }

  cout << endl;
  for (int a = 0; a < n; a ++)
    for (int b = a + 1; b < n; b ++) 
      cout << "dist[" << a << ", " << b << "] = " << dist[a * n + b] << " " << endl;
  exit(0);
  */
  
  // Check the automaton is synchronizing
  for (int a = 0; a < n; a ++)
    for (int b = a + 1; b < n; b ++)
      if (!visited[a * n + b])
	return false;

  return true;
}

int find_sync_word(int s, char *w) {
  int length = 0;

  while (dist[s] > 0) {
    w[length ++] = 'a' + first[s];
    s = p[s];
  }

  return length;
}

// Cria lista de estados com base num vetor característico b
int populate(bool *b, int *active) {
  int counter = 0;

  for (int i = 0; i < n; i ++)
    if (b[i]) 
      active[counter ++] = i;

  return counter;
}

void synchronize() {
  int N = n * n;
  
  // Vetor característico de estados ativos
  bool *chi = new bool [n];

  // Lista dos estados ativos
  int *active = new int [n];
  int num_active = n;

  // Para conter palavra que sincroniza dois estados
  char *w = new char [N];
  int length_w;

  // Todos os estados estão ativos
  for (int i = 0; i < n; chi[i ++] = true);

  // Cria lista de estados ativos a partir do vetor característico
  num_active = populate(chi, active);

  // Enquanto o conjunto dos ativos tem pelo menos 2 elementos
  while (num_active > 1) {
    int min_s, min_dist = N;

    // Acha o par que mais rápido se sincroniza
    for (int i = 0; i < num_active; i ++)
      for (int j = i + 1; j < num_active; j ++) {
	int x = active[i];
	int y = active[j];
	int s = (x < y) ? x * n + y : y * n + x;
	if (dist[s] < min_dist) {
	  min_dist = dist[s];
	  min_s = s;
	}
      }

    // Encontra palavra que sincroniza esse par
    length_w = find_sync_word(min_s, w);
    cout << string(w, length_w);

    // Evolui o conjunto todo segundo a palavra encontrada
    for (int i = 0; i < length_w; i ++) 
      for (int j = 0; j < num_active; j ++)
	  active[j] = T[w[i] - 'a'][active[j]];
        
    // Refaz o vetor característico
    for (int i = 0; i < n; chi[i ++] = false);
    for (int j = 0; j < num_active; j ++)
      chi[active[j]] = true;

    // Reconstroi a lista dos ativos
    num_active = populate(chi, active);


    // Debug
    /*
    cerr << "after" << endl;
    for (int j = 0; j < num_active; j ++)
      cerr << active[j] << " ";
    cerr << endl; */
    
    // cerr << string(w, length_w) << endl;
  }

  cout << endl << flush;
}

int main() {
  read_input();
  fill_T();
  fill_G();
  
  if (is_synchronizing())
    synchronize();
  else
    cout << "NAO" << endl;

  return 0;
}
