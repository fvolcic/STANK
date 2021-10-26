#include <stdio.h>

int main(){

    unsigned long long a = 1;
    unsigned long long b = 1;

    for(int i = 0; i < 100; ++i){
        unsigned long long c = a + b; 
        a = b;
        b = c; 
        printf("%llu\n", c); 
    }

    

}