# A basic stack based language interpreter for the slang language.

class StaticStack:

    def __init__(self, stackSize):
        self.stack = [0 for _ in range(stackSize)]
        self.stack_ptr = 0
    
    def push(self, val):
        self.stack[self.stack_ptr] = val
        self.stack_ptr += 1
    
    def pop(self):
        self.stack_ptr -= 1
        return self.stack[self.stack_ptr]

    def top(self):
        return self.stack[self.stack_ptr - 1]
    
    def data(self):
        return (self.stack, self.stack_ptr)

    def size(self):
        return self.stack_ptr

    def rot(self, depth):
        # import pdb
        # pdb.set_trace()
        tmp = self.top()
        for i in range(depth - 1):
            self.stack[self.stack_ptr - 1 - i] = self.stack[self.stack_ptr - 2 - i]
        self.stack[self.stack_ptr - depth] = tmp

    def swap_top(self):
        tmp = self.stack[self.stack_ptr]
        self.stack[self.stack_ptr] = self.stack[self.stack_ptr - 1]
        self.stack[self.stack_ptr - 1] = tmp
    

# run a program, given a list reprenting the program. 
def run_program(program: list, program_size = 50000):
    stack = StaticStack(program_size)

    op_stack = StaticStack(20)

    instr_index = 0
    ip_val = program[instr_index]

    # interpret the program until we reach a pterm (program terminate) call
    while(ip_val != "pterm"):
        ip_val = program[instr_index]
        
        #print(f"{ip_val} ")
        #print(f"Stack Is{stack.stack[:stack.size()]}")
        input()
        if(ip_val.isnumeric()):
            stack.push(int(ip_val))
            instr_index += 1
            continue
        
        elif(ip_val == "+"):
            v1 = stack.pop()
            v2 = stack.pop()
            stack.push(v1 + v2)
            instr_index += 1
            continue

        elif(ip_val == "-"):
            v1 = stack.pop()
            v2 = stack.pop()
            stack.push(v1 - v2)
            instr_index += 1
            continue

        elif(ip_val == "*"):
            v1 = stack.pop()
            v2 = stack.pop()
            stack.push(v1 * v2)
            instr_index += 1
            continue

        elif(ip_val == "/"):
            v1 = stack.pop()
            v2 = stack.pop()
            stack.push(v1 / v2)
            instr_index += 1
            continue

        elif(ip_val == "<"):
            v1 = stack.pop()
            v2 = stack.pop()
            if(v1 < v2):
                stack.push(1)
            else:
                stack.push(0)
            instr_index += 1
            continue

        elif(ip_val == ">"):
            v1 = stack.pop()
            v2 = stack.pop()
            if(v1 > v2):
                stack.push(1)
            else:
                stack.push(0)
            instr_index += 1
            continue

        elif(ip_val == "=="):
            v1 = stack.pop()
            v2 = stack.pop()
            if(v1 == v2):
                stack.push(1)
            else:
                stack.push(0)
            instr_index += 1
            continue

        elif(ip_val == "neg"):
            # import pdb
             # pdb.set_trace()
            v= stack.pop()
            if(v == 0):
                stack.push(1)
            else:
                stack.push(0) 
            instr_index += 1
            continue
            
        elif(ip_val == "rot"):
            depth = stack.pop()
            stack.rot(depth)
            instr_index += 1
            continue

        elif(ip_val == "<="):
            v1 = stack.pop()
            v2 = stack.pop()
            if(v1 <= v2):
                stack.push(1)
            else:
                stack.push(0)
            instr_index += 1
            continue

        elif(ip_val == ">="):
            v1 = stack.pop()
            v2 = stack.pop()
            if(v1 >= v2):
                stack.push(1)
            else:
                stack.push(0)
            instr_index += 1
            continue

        elif(ip_val == "print"):
            depth = stack.pop()

            for _ in range(depth):
                print( chr(stack.pop()), end='' )
            instr_index += 1
            continue

        elif(ip_val == "nprint"):
            depth = stack.pop()
            for _ in range(depth):
                print( stack.pop(), end='' )
            instr_index += 1
            continue

        elif(ip_val == "if"):
            #import pdb
            #pdb.set_trace()
            op_stack.push("if")
            instr_index += 1
            continue
        
        elif(ip_val == "while"):
            op_stack.push("while")
            instr_index += 1
            continue

        elif(ip_val == "ask"):
            #import pdb
            #pdb.set_trace()
            x = input(" ")
            x = x.lstrip().rstrip().split()
            for v in x:
                stack.push(int(v))
            instr_index += 1
            continue

        elif(ip_val == "r_ask"):
            x = input(" ")
            x = x.lstrip().rstrip().split()
            for v in reversed(x):
                stack.push(int(v))
            instr_index += 1
            continue

        elif(ip_val == "goto"):
            change = stack.pop()
            if (change == 0):
                continue
            sign = change / abs(change)
            change = abs(change)

            if(op_stack.size() == 0):
                instr_index += sign * change 
                continue 
        
            
            if(sign == 1):
                for _ in range(change):
                    instr_index+=1
                    if program[instr_index] == "end":
                        op_stack.pop()
                continue

            if(sign == -1):
                for _ in range(change):
                    instr_index -= 1 
                    if program[instr_index] == op_stack.top():
                        op_stack.pop()
                continue
        
        elif(ip_val == "end"):
            if(op_stack.top() == "if"):
                op_stack.pop()
                instr_index+=1
                continue
            if(op_stack.top() == "while"):
                while(program[instr_index] != "while"):
                    instr_index-=1
                instr_index += 1
                continue
        
        elif(ip_val == "do"):
            if(op_stack.top() == "if"):
                if(stack.pop() != 0):
                    instr_index += 1
                    continue
                else:
                    count = 0
                    while(program[instr_index] != "end" or count != 0):
                        if(program[instr_index] == "if" or program[instr_index] == "while"):
                            count += 1
                        if(program[instr_index] == "end"):
                            count -= 1
                        instr_index += 1
                    instr_index += 1
                    op_stack.pop()
            
            if(op_stack.top() == "while"):
                if(stack.pop() != 0):
                    instr_index += 1
                    continue
                else:
                    count = 0
                    while(program[instr_index] != "end" or count != 0):
                        if(program[instr_index] == "if" or program[instr_index] == "while"):
                            count += 1
                        if(program[instr_index] == "end"):
                            count -= 1
                        instr_index += 1
                    instr_index += 1
                    op_stack.pop()
                    continue

        elif(ip_val == "dup"):
            stack.push(stack.top())
            instr_index += 1
            continue

        elif(ip_val == "swp"):
            stack.swap_top()
            instr_index += 1
            continue


import click


def read_file(filename):
    program = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.lstrip().rstrip().split(" ")
            program += line
    
    return program

@click.command()
@click.argument("filename")
def main(filename):
    program = read_file(filename)
    import pdb
    pdb.set_trace()
    run_program(program)
    print("\n")

if __name__ == "__main__":
    main()