#include <stdlib.h>
#include <stdio.h>

long long program_stack[PROGRAM_STACK_SIZE]; // static stack that is allocated.
size_t sp = 0; // pointer to the program stack header.

long long top(){
    return program_stack[sp - 1];
}

long long pop(){
   long long tmp = top(); 
    --sp;
    return tmp; 
}

void push(long long val){
    program_stack[sp] = val;
    ++sp; 
}

void plus(){
    push(pop() + pop());
}

void minus(){
    push(pop() - pop());
}

void times(){
    push(pop() * pop());
}

void divide(){
    push(pop() / pop());
}

void stacksize(){
    push(sp);
}

void rrot(){
    int depth = pop();
    long long tmp = top();
    int start = sp - 1;
    for(int i = depth - 1; i >= 0; --i){
        program_stack[sp - 2 - i] = program_stack[sp - 1 - i];
    }
    program_stack[sp - 1] = tmp;
}

void nswap(){
    int n = pop();
    long long tmp = top();
    program_stack[sp - 1] = program_stack[sp - 1 - n];
    program_stack[sp - 1 - n] = tmp;
}

void swap(){
    long long tmp = top();
    program_stack[sp - 1] = program_stack[sp - 2];
    program_stack[sp - 2] = tmp;
}

void rot(){
    int depth = pop(); 
    long long tmp = top();

    for(int i = 0; i < depth - 1; ++i){
        program_stack[sp - 1 - i] = program_stack[sp - 2 - i]; 
    }

    program_stack[sp - depth] = tmp;
}

void dup(){
    push(top()); 
}

void stack_print(){
    int str_size = pop();
    for(int i = 0; i < str_size; ++i){
        printf("%c", pop());
    }
}

void copy2top(){
    push( program_stack[sp - 1 - pop()] );
}

void lt(){
    push(pop() < pop());
}

void gt(){
    push(pop() > pop());
}

void le(){
    push(pop() <= pop());
}

void ge(){
    push(pop() >= pop()); 
}

void eq(){
    push(pop() == pop());
}

void mod(){
    push(pop() % pop());
}

void neg(){
    push(!pop()); 
}

void or(){
    push(pop() || pop());
}

void and(){
    push(pop() && pop());
}

void bit_or(){
    push(pop() | pop());
}

void bit_and(){
    push(pop() & pop());
}

void new(){
    push((long long)malloc(pop()));
}

void delete(){
    free((void*)pop()); 
}

void read_ptr(){
    push( *(int*) pop() );
}

void store_ptr(){
    * ((int*) pop()) = pop();
}

void stack_nprint(){
    int str_size = pop();
    for(int i = 0; i < str_size; ++i){
        printf("%i", pop());
    }
}

void exitprogram(){
    exit(pop()); 
}

void print_stack(){
    if(sp == 0){
        printf("[]\n");
        return;
    }

    printf("[");
    for(int i = 0; i < sp - 1; ++i){
        printf("%llu, ", program_stack[i]);
    }
    printf("%llu", program_stack[sp - 1]);
    printf("]\n");
}