import os
import timeit

import click

valid_tokens_non_numeric = set(['+', '/', '*', '-', '<', '>', '<=', '>=', '==','%', 'while', 'if', 'elif', 'else', 'do', 'goto', 'end', 'exit', 'print', 'nprint', 'dup', 'rot','rrot', 'copy2top', 'pop','stacksize','neg', 'top', "swap", 'nswap'])

def tokenize(filename, for_compile = False):
    global valid_tokens_non_numeric
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

    for i in range(len(tokens)):
        if tokens[i] == 'goto':
            tokens[i] = tokens[i-1]
            tokens[i-1] = 'goto'
    return tokens

def is_operator(token):
    operators = {
        '+':"plus()",
        '-':"minus()",
        '*':"times()",
        '/':"divide()",
        '<':"lt()",
        '>':"gt()",
        '<=':"le()",
        '>=':"ge()",
        '==':"eq()"
    }

    if token not in operators.keys():
        return False
    return operators[token]
    

def token_to_c(token):

    global valid_tokens_non_numeric

    if token == "end":
        return "}"
    if token == "do":
        return ""
    if token == "exit":
        return "exitprogram()"
    if token == "print":
        return "stack_print()"
    if token == "nprint":
        return "stack_nprint()"
    if is_operator(token) != False:
        return is_operator(token)
    if type(token) != str:
        return f"push({token})"
    return token + "()"

# setup all the boilerplate for the compilable c file.
def setup_file(fp, program_size=100):
    fp.write(f"#define PROGRAM_STACK_SIZE {program_size}\n")
    with open("stankbase.c", 'r') as f:
        for line in f:
            fp.write(line)

def setup_main(fp):
    fp.write("\n\n//MAIN DEFINITION\nint main(){\n")

def close_main(fp):
    fp.write("}")

class file_generator:
    def __init__(self, tokens, outfile, program_size):
        self.tokens = tokens
        self.index = 0
        
        self.program_size = program_size

        self.outfile = outfile

        self.functions = {}
        self.num_functions = 0
    
    def generate_output(self):
        output_string = ""
        if self.tokens[self.index] not in valid_tokens_non_numeric and type(self.tokens[self.index]) == str:
            output_string+=(self.tokens[self.index] + "\n")
            self.index += 1
            return output_string

        if self.tokens[self.index] not in ["if", "while", "goto"]:
            output_string+=(token_to_c(self.tokens[self.index])+";\n")
            self.index += 1
            return output_string

        elif self.tokens[self.index] in ["if", "while"]:
            output_string += self.parse_conditional()
            return output_string

        elif self.tokens[self.index] == "goto":
            output_string+=(f"goto {self.tokens[self.index + 1]};\n")
            self.index += 2
            return output_string



    def place_next_statement(self):        
        self.outfile.write(self.generate_output())

    def place_functions(self):
        self.outfile.write("\n\n//CONDITIONAL FUNCTIONS\n")
        for func in self.functions:
            self.outfile.write(self.functions[func])

    # return a string that represents the literal
    def parse_conditional(self):
        conditional_name = f"conditional{self.num_functions}"
        self.functions[conditional_name] = "int " +conditional_name + "(){\n"
        out_conditional_string = self.tokens[self.index] + "(" + conditional_name + "()){"
        self.num_functions += 1
        self.index += 1
        
        while self.tokens[self.index] != "do":
            if self.tokens[self.index] in ["while", "if"]:
                self.functions[conditional_name] += self.parse_conditional()
            else:
                self.functions[conditional_name] += self.generate_output()
        
        self.functions[conditional_name] += "return pop();\n}\n"
        self.index += 1
        return out_conditional_string

    def generate_statements(self):
        while(self.index != len(self.tokens)):
            self.place_next_statement()

    def generate_functions(self):
        pass

    def generate_function_headers(self):
        num_funcs = 0
        for token in self.tokens:
            if token in ["if", "while"]:
                self.outfile.write(f"int conditional{num_funcs}();\n")
                num_funcs += 1

    def generate(self):
        setup_file(self.outfile, self.program_size)
        self.generate_function_headers()
        setup_main(self.outfile)
        self.generate_statements()
        close_main(self.outfile)
        self.place_functions()

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

@click.command()
@click.argument("filename")
@click.option("-o", "--output", default="stank.out")
@click.option("-ps", "--program-size", type=int, default=100)
@click.option("-c", "--get-c", is_flag = True)
def main(filename, output, program_size, get_c):

    start = timeit.timeit()

    with open(output+".tmp.c", 'w') as fout:
        generator = file_generator(tokenize(filename, True), fout, program_size)

        generator.generate()

    end = timeit.timeit()

    if get_c:
        print(bcolors.BOLD + bcolors.OKGREEN + "Successfully " + \
            bcolors.ENDC + f"generated C output file {output+'.tmp.c'} \
                in {end - start:.2f} seconds!")
        exit(0)

    os.system(f"gcc {output+'.tmp.c'} -o {output}")
    os.system(f"rm {output+'.tmp.c'}")

    end = timeit.timeit()
    print(bcolors.BOLD + bcolors.OKGREEN + "\nCompliation Successful!" + bcolors.ENDC)
    print( f"Output written to {output}" )
    print( f"Compliation took {end - start:.2f} seconds.\n")

if __name__ == "__main__":
    main()