#include <stdio.h>
#include <time.h>
#include <stdlib.h>

int RandomNum(int upper) {
  static int i = 0;
  if (i == 0) {
    srand((unsigned)(time(NULL)));
    i = 1;
  }
  return rand() % upper;
};

int main(){
  int count[18] ={0};
  for (int j=0; j<18; j++){count[j]=0;}
    for (int i=0; i< 10000; i++){
        int r = RandomNum(950);
        int freq[18] = {170, 139, 100, 41, 37, 23, 37, 15, 40, 29, 35, 17, 24, 18, 160, 45, 35, 140};
        for (int j=0; j<18; j++){
        if (r%freq[j] == 0){
          count[j] +=1;
        }
        }
    }
    int sum = 0;
  for (int j=0; j<18; j++){sum+=count[j];printf("%d\n", count[j]);}
  printf("%d\n", sum);
}