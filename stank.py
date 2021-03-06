# Python interpreter for STANK

# Stack with a static amount of memory
# But it can still be increased in size for turing completness if needed
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
        tmp = self.top()
        for i in range(depth - 1):
            self.stack[self.stack_ptr - 1 - i] = self.stack[self.stack_ptr - 2 - i]
        self.stack[self.stack_ptr - depth] = tmp

    def rrot(self, depth):
        tmp = self.stack[self.stack_ptr - depth]
        for i in reversed(range(depth - 1)):
            self.stack[self.stack_ptr - 2 - i] = self.stack[self.stack_ptr - 1 - i]
        self.stack[self.stack_ptr - 1] = tmp

    def nswap(self, n):
        tmp = self.top()
        self.stack[self.stack_ptr - 1] = self.stack[self.stack_ptr - 1 - n]
        self.stack[self.stack_ptr - 1 - n] = tmp

    def swap_top(self):
        tmp = self.top()
        self.stack[self.stack_ptr - 1] = self.stack[self.stack_ptr - 2]
        self.stack[self.stack_ptr - 2] = tmp

    def getstack(self):
        return self.stack[:self.size()]

# Tokenize a file and return array of tokens without whitespace
def tokenize(filename, for_compile = False):
    valid_tokens_non_numeric = set(['+', '/', '*', '-', '<', '>', '<=', '>=', '==','%', 'while', 'if', 'elif', 'else', 'do', 'goto', 'end', 'exit', 'print', 'nprint', 'dup', 'rot','rrot', 'copy2top', 'pop','stacksize','neg', 'top', "swap", 'nswap'])
    labels = {}
    tokens = []
    
    with open(filename, 'r') as f:
        for line in f:
            line = line.lstrip().rstrip().replace('\n','')
            line += ' '
            token_start = 0
            token_end = 0

            token_whole = None

            while(token_start < len(line)):
                while(token_start < len(line) and token_start == token_end and line[token_start] == ' '):
                    token_start+=1
                    token_end+=1
                
                if(token_start == len(line)):
                    continue

                if(line[token_start] == '#'):
                    token_start = len(line)
                    continue

                # string parse
                if(line[token_start] == "'"):
                    reverse = False
                    token_end += 1
                    while(line[token_end] != "'"):
                        token_end+=1
                    if(line[token_end + 1] == 'r'):
                        token_end+=1
                        reverse = True
                    if reverse:
                        token_whole = line[token_start+1:token_end-1]
                    else:
                        token_whole = line[token_start+1:token_end]
                    if reverse:
                        for char in token_whole:
                            tokens.append(ord(char))
                    else:
                        for char in reversed(token_whole):
                            tokens.append(ord(char))
                    tokens.append(len(token_whole))
                    token_end += 1
                    token_start = token_end

                else:
                    while(line[token_end] != ' '):
                        token_end += 1

                    token = line[token_start:token_end]

                    # read numbers onto the stack
                    if token.isnumeric() or token[1:].isnumeric():
                        try:
                            tokens.append(int(token))
                        except ValueError:
                            tokens.append(float(token))

                    elif token[-1] == "!":
                        if for_compile:
                            tokens.append(token[:-1])
                        else:
                            tokens.append(token)

                    elif token[-1] == ":":
                        tokens.append(token)

                    elif token in valid_tokens_non_numeric:
                        tokens.append(token)
                    else:
                        print(f"{token} is not a valid token. Exiting.")
                        exit(1)

                    # tokens.append(line[token_start:token_end])
                    token_start=token_end

    if for_compile:

        for i in range(len(tokens)):
            if tokens[i] == 'goto':
                tokens[i] = tokens[i-1]
                tokens[i-1] = 'goto'
        return tokens

    labels = {}
    num_labels = 0
    for i,token in enumerate(tokens) :
        if type(token) != str:
            continue
        if token[-1] == ":":
            num_labels+=1
        
            labels[token[:-1]] = i - num_labels + 1

    tokens_new = []

    for token in tokens:
        if type(token) != str:
            tokens_new.append(token)
            continue
        if token[-1] == ":":
            continue

        if token[-1] == "!":
            tokens_new.append( labels[token[:-1]] )
        else:
            tokens_new.append(token)
    
    return tokens_new

class Program:

    def __init__(self, program, programSize = 50000):
        self.program = program
        self.ip = 0
        self.stack = StaticStack(programSize)
        self.op_stack = StaticStack(100)

    # index must point to either an if or a while 
    # of which you would like to find the complimentary end statement
    def scan_end(self,index):
        index += 1
        instr = self.program[index]
        count = 0
        
        while(count > 0 or instr != 'end'):
            if(instr == 'while' or instr == 'if'):
                count += 1
            
            if(instr == 'end'):
                count -= 1
            
            index += 1
            instr = self.program[index]

        return index

    # index must be a index of an end that is connected to a while
    def find_while_index(self, index):
        index -= 1
        count = 0
        while(self.program[index] != 'while' or count != 0):
            if(self.program[index] == 'end'):
                count += 1
            if(count > 0 and self.program[index] in ['while', 'if']):
                count -= 1
            index -= 1
        return index

    # index must point to end index
    def find_op_index_from_end(self, index):
        count = 0
        index -= 1
        while(count > 0 or (self.program[index] != "where" and self.program[index] != "if")):
            if(self.program[index] == "end"):
                count += 1
            if(self.program[index] == "if" or self.program[index] == "while"):
                count -= 1
            index -= 1
        return index           

    def update_ip(self):
        instr = self.program[self.ip]
        
        if(instr == "do"):
            test = self.stack.pop()
            if test != 0:
                self.ip += 1
                return
            else:
                self.ip = self.scan_end(self.ip) + 1
                self.op_stack.pop()
                return

        elif(instr == "end"):
            op_type = self.op_stack.pop()

            if(op_type == "if"):
                self.ip += 1
                return

            if(op_type == "while"):
                self.ip = self.find_while_index(self.ip)
                return    

        elif(instr == "goto"):
            where = self.stack.pop()
            current = self.ip
            where = where - current
            if(where == 0):
                return
            if(where > 0):
                for _ in range(where):
                    if(self.program[self.ip] == "if" or self.program[self.ip] == "where"):
                        self.op_stack.push(self.program[self.ip])
                    elif(self.program[self.ip] == "end"):
                        self.op_stack.pop()

                    self.ip += 1
                return
            if(where < 0):
                for _ in range(abs(where)):
                    if(self.program[self.ip] == "end"):
                        op_index = self.find_op_index_from_end(self.ip)
                        self.op_stack.push(self.program[op_index])
                    if(self.program[self.ip] in ["where", "if"]):
                        self.op_stack.pop()
                    self.ip -= 1
                if(self.program[self.ip] in ["where", "if"]):
                    self.op_stack.pop()
                return

        else:
            self.ip += 1
        


    def run_instruction(self):
        instr = self.program[self.ip]

        if(type(instr) != str):
            self.stack.push(instr)
            self.update_ip()
            return

        if(instr == "print"):
            length = self.stack.pop()
            for _ in range(length):
                val = self.stack.pop()
                if(val == 1000):
                    print(self.stack.pop(), end='')
                else:
                    print(chr(val), end='')

            self.update_ip()
            return

        if(instr == "goto"):
            self.update_ip()
            return

        if(instr == "stacksize"):
            self.stack.push(self.stack.size())
            self.update_ip()
            return

        if(instr == "nprint"):
            length = self.stack.pop()
            for _ in range(length):
                print(self.stack.pop(), end='')
            self.update_ip()
            return

        if(instr == "rrot"):
            self.stack.rrot(self.stack.pop())
            self.update_ip()
            return

        if(instr == "*"):
            self.stack.push(self.stack.pop() * self.stack.pop())
            self.update_ip()
            return

        if(instr == "%"):
            self.stack.push(self.stack.pop() % self.stack.pop())
            self.update_ip()
            return

        if(instr == "/"):
            self.stack.push(self.stack.pop() / self.stack.pop())
            self.update_ip()
            return
        
        if(instr == "+"):
            self.stack.push(self.stack.pop() + self.stack.pop())
            self.update_ip()
            return

        if(instr == "nswap"):
            self.stack.nswap(self.stack.pop())
            self.update_ip()
            return

        if(instr == "-"):
            self.stack.push(self.stack.pop() - self.stack.pop())
            self.update_ip()
            return

        if(instr == "=="):
            if(self.stack.pop() == self.stack.pop()):
                self.stack.push(1)
            else:
                self.stack.push(0)
            self.update_ip()
            return

        if(instr == "dup"):
            self.stack.push(self.stack.top())
            self.update_ip()
            return
        
        if(instr == "rot"):
            self.stack.rot(self.stack.pop())
            self.update_ip()
            return
        
        if(instr == "neg"):
            val = self.stack.pop()
            if val != 0:
                self.stack.push(0)
            else:
                self.stack.push(1)
            self.update_ip()
            return

        if(instr == "exit"):
            exit(self.stack.pop())

        if(instr == "swap"):
            self.stack.swap_top()
            self.update_ip()
            return

        if(instr == "copy2top"):
            self.stack.push(self.stack.stack[self.stack.size()-self.stack.pop()-1])
            self.update_ip()
            return
        
        if(instr == "if"):
            self.op_stack.push("if")
            self.update_ip()
            return
        
        if(instr == "while"):
            self.op_stack.push("while")
            self.update_ip()
            return
        
        if(instr == "do"):
            self.update_ip()
            return
        
        if(instr == "end"):
            self.update_ip()
            return
                
        if(instr == "elif"):
            self.update_ip()
            return
        
        if(instr == "else"):
            self.update_ip()
            return
        
        if(instr == "pop"):
            self.stack.pop()
            self.update_ip()
            return
        
        if(instr == "<"):
            self.stack.push(int(self.stack.pop() < self.stack.pop()))
            self.update_ip()
            return
        
        if(instr == ">"):
            self.stack.push(int(self.stack.pop() > self.stack.pop()))
            self.update_ip()
            return

        if(instr == "<="):
            self.stack.push(int(self.stack.pop() <= self.stack.pop()))
            self.update_ip()
            return
        
        if(instr == "=>"):
            self.stack.push(int(self.stack.pop() >= self.stack.pop()))
            self.update_ip()
            return

def gen_func_decls(tokens):
    decls = []

    for token in tokens:
        if token in ["while", "do"]:
            decls.append(f"bool conditional{len(decls)}()")

def compile_token(token):
    if token == "goto":
        return "goto"
    elif token == "pop":
        return "pop()"
    elif token == "dup":
        return "dup()"
    elif token == "rot":
        return "rot()"
    elif token == "rrot()":
        return "rrot()"
    elif token == "+":
        return "plus()"
    elif token == "-":
        return "minus()"
    elif token == "*":
        return "times()"
    elif token == "/":
        return "divide()"
    elif token == "stacksize":
        return "stacksize()"
    elif token == "exit":
        return "exit()"

def output_boilerplate(fp, headers, program_size=1000):
    fp.print("#include <stdio.h>")

    for header in headers:
        fp.print(header)
        fp.print(";\n")
    
    fp.print(f"#define PROGRAM_STACK_SIZE {program_size}")

    with open("stankbase.c", 'r') as f:
        for line in f:
            fp.print(line)

# outputs a C stank file that can be run
def generate_c(input_file, output_file):
    tokens = tokenize(input_file, True) # Program is only valid if it can be tokenized.
    
    headers = gen_func_decls(tokens)

    output_boilerplate()

    # maps a function name to the function represented as a string.
    functions = {}
    num_funcs = 0
    with open(output_file, 'w') as f:
        for token in tokens:
            if not token in ["if", "while"]:
                f.write(compile_token(token)+";\n")
    

import click

@click.command()
@click.argument('filename')
@click.option('-c', '--com', is_flag=True)
@click.option('-o', '--output', type=str, default=None)
@click.option('-sp', '--print-stack', 'print_stack', is_flag=True)
@click.option('-osp', '--print-op-stack', is_flag=True)
@click.option('-ss', '--stack-size', type=int, default=1000)
@click.option('-v', '--verbose', 'verbose', is_flag=True)
@click.option('-t', '--tokenize-file', 'tokenize_file', type=str, default=None)
def main(filename, print_stack,print_op_stack,verbose, tokenize_file, stack_size, com, output):
    
    if output != None and com:
        generate_c(filename, output+".stanky.c")
        exit(0)

    if tokenize_file != None:
        with open(tokenize_file, 'w') as f:
            for token in tokenize(filename, com):
                f.write(str(token) + '\n')
        exit(0)
    p = Program(tokenize(filename), stack_size)
    while(1):
        if verbose:
            print(p.program[p.ip], end=' ')
        if print_stack or verbose:
            print(p.stack.getstack())
        if print_op_stack:
            print(p.op_stack.getstack())
        p.run_instruction()

if __name__ == "__main__":
    main()

