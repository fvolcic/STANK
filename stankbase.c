#include <stdlib.h>
#include <stdio.h>

#define NUM_PROGRAM_STACKS_MAX 100

#ifndef PROGRAM_STACK_SIZE
#define PROGRAM_STACK_SIZE 100
#endif

long long * program_stack;//[PROGRAM_STACK_SIZE]; // static stack that is allocated.
size_t sp = 0; // pointer to the program stack header.

long long * program_stacks[NUM_PROGRAM_STACKS_MAX];
size_t program_stacks_sp[NUM_PROGRAM_STACKS_MAX];
size_t num_stacks = 1;
size_t cur_stack = 0;

long long pop();

void add_stack(){
    program_stacks[num_stacks] = (long long*)malloc((sizeof(long long) * pop()));
    program_stacks_sp[num_stacks] = 0; 
    ++num_stacks;
}

void remove_stack(){
    free(program_stacks[num_stacks - 1]);
    num_stacks -= 1; 
}

void set_program_stack(){
    size_t new_stack = pop();
    program_stacks_sp[cur_stack] = sp;
    program_stack = program_stacks[new_stack];
    sp = program_stacks_sp[new_stack]; 
    cur_stack = new_stack; 
}

void setup(){
    program_stack = (long long *) malloc( PROGRAM_STACK_SIZE * sizeof(long long)); 
    program_stacks[0] = program_stack;
    sp = program_stacks_sp[0];
}

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
    push( *(long*) pop() );
}

void store_ptr(){
    long long * mem = (long*)pop();
    * mem = pop();
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

void sps(){
    set_program_stack();
}

void copy2stack(){
    size_t to_stack = pop();
    long long val = pop();
    push(val); 
    program_stacks[to_stack][program_stacks_sp[to_stack]] = val; 
    program_stacks_sp[to_stack] += 1; 

}

void copyfromstack(){
    size_t from_stack = pop();
    push(from_stack); 
}

void numstacks(){
    push(num_stacks);
}

void copy2D(){
    long long stack = pop();
    long long depth = pop();

    push(program_stacks[stack][program_stacks_sp[stack]-depth-1]); 
}

void curstack(){
    push(cur_stack); 
}