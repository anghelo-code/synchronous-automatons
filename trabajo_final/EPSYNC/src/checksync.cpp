#include <iostream>
#include <fstream>
#include <string>

using namespace std;

int n;
int k;
int **D;
int **T;

void read(char *filename) {
  ifstream f;

  f.open(filename);

  f >> n;
  f >> k;

  D = new int * [n];

  for (int i = 0; i < n; i ++) {
    D[i] = new int [k];
    for (int j = 0; j < k; j ++)
      f >> D[i][j];
  }

  T = new int * [k];
  for (int i = 0; i < k; i ++) {
    T[i] = new int [n];
    for (int j = 0; j < n; j ++)
      T[i][j] = D[j][i];
  }  

  f.close();
}

int main(int ac, char **av) {
  if (ac < 2) {
    cerr << "modo de usar:\n\n\t\tcheck arquivo.txt\n\nLee un DFA" <<
      "de arquivo.txt y una palabra de la entrada estandar y verifica" <<
      "si la palabra sincroniza el DFA." << endl;
    return 1;
  }

  // Lê o autômato do arquivo
  read(av[1]);

  string w;

  // Characteristic vector
  bool *chi = new bool [n];

  if (ac > 2)
    w = string(av[2]);
  else {
    // Lê a palavra
    getline(cin, w);
  }

  // Declara um vetor
  int *v = new int [n];
  for (int i = 0; i < n; i ++)
    v[i] = i;

  int length = w.size();

  // Verifica que os caractéres da palavra são de 'a' a 'z'
  for (int i = 0; i < length; i ++)
    if (w[i] < 'a' || w[i] > 'z')
      return 1;

  // Número de elementos no vetor v
  int m = n;
  
  // C++ is row oriented, so... we use the transpose
  // of the transition matrix to simulate everything.
  for (int j = 0; j < length; j ++) {
    if (!(length % n)) {
      for (int i = 0; i < n; i ++)
	chi[i] = false;
      
      for (int i = 0; i < m; i ++)
	chi[v[i]] = true;
       
      for (int i = 0, m = 0; i < n; i ++) 
	if (chi[i]) 
	  v[m ++] = i;      
    }
    
    for (int i = 0; i < m; i ++)
      v[i] = T[w[j] - 'a'][v[i]];
  }

  // Characteristic vector
  for (int i = 0; i < n; i ++)
    chi[i] = false;

  int total = 0;
  for (int i = 0; i < m; i ++)
    if (!chi[v[i]]) {
      total ++;
      chi[v[i]] = true;
    }
    
  if (total > 1) {
    cerr << "No sincroniza. Estados restantes:";
    for (int i = 0; i < n; i ++)
      if (chi[v[i]])
	cerr << " " << v[i];
    cerr << endl;
    return 1;
  }
  else
    cerr << "Sincroniza para el estado " << v[0] << "." << endl;

  return 0;
}
