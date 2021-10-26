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

    def swap_top(self):
        tmp = self.top()
        self.stack[self.stack_ptr - 1] = self.stack[self.stack_ptr - 2]
        self.stack[self.stack_ptr - 2] = tmp


# Tokenize a file and return array of tokens without whitespace
def tokenize(filename):
    valid_tokens_non_numeric = set(['+', '/', '*', '-', '<', '>', '<=', '>=', '==', 'while', 'if', 'elif', 'else', 'do', 'goto', 'end', 'exit', 'print', 'dup', 'rot','copy2top', 'pop', 'top', "swap"])
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
                    if token.isnumeric():
                        try:
                            tokens.append(int(token))
                        except ValueError:
                            tokens.append(float(token))

                    elif token in valid_tokens_non_numeric:
                        tokens.append(token)
                    else:
                        print(f"{token} is not a valid token. Exiting.")
                        exit(1)

                    # tokens.append(line[token_start:token_end])
                    token_start=token_end

    return tokens

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

        if(instr == "-"):
            self.stack.push(self.stack.pop() - self.stack.pop())
            self.update_ip()
            return

        if(instr == "=="):
            self.stack.push(self.stack.pop() == self.stack.pop())
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
        
        if(instr == "goto"):
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

import click

@click.command()
@click.argument('filename')
def main(filename):
    p = Program(tokenize(filename))
    while(1):
        #print(p.stack.stack[:p.stack.size()])
        p.run_instruction()

if __name__ == "__main__":
    main()

