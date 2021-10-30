#include <stdlib.h>
#include <stdio.h>

int program_stack[PROGRAM_STACK_SIZE]; // static stack that is allocated.
size_t sp = 0; // pointer to the program stack header.

int top(){
    return program_stack[sp - 1];
}

int pop(){
   int tmp = top(); 
    --sp;
    return tmp; 
}

void push(int val){
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
    int tmp = top();
    int start = sp - 1;
    for(int i = depth - 1; i >= 0; --i){
        program_stack[sp - 2 - i] = program_stack[sp - 1 - i];
    }
    program_stack[sp - 1] = tmp;
}

void nswap(){
    int n = pop();
    int tmp = top();
    program_stack[sp - 1] = program_stack[sp - 1 - n];
    program_stack[sp - 1 - n] = tmp;
}

void swap(){
    int tmp = top();
    program_stack[sp - 1] = program_stack[sp - 2];
    program_stack[sp - 2] = tmp;
}

void rot(){
    int depth = pop(); 
    int tmp = top();

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

void neg(){
    push(!pop()); 
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
