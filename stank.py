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


# Tokenize a file and return array of tokens without whitespace
def tokenize(filename):
    valid_tokens_non_numeric = set(['+', '/', '*', '-', '<', '>', '<=', '>=', 'while', 'if', 'elif', 'else', 'do', 'goto', 'end', 'exit', 'print', 'dup', 'rot','copy2top', 'pop', 'top'])
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

def main():
    
    print(tokenize('Example.stanky'))

if __name__ == "__main__":
    main()

