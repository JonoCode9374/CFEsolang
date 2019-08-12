#Curlyfrick Interpreter
#Absolutely no rights reserved


import math 
'''


OpCode | What | Psuedo
0001 | Print Value | PRINT val
0010 | Print Variable | PRINT VAR
0011 | Store value in var | VAR val
0100 | Increment variable ptr | INC PTR val
0101 | Decrement variable ptr | DEC PTR val
0110 | Input Variable | INPUT var
0111 | If condition | IF var
1000 | While loop | WHILE var
1001 | Comment | //
1010 | End statement | END
1011 | Increment variable | INC val
1100 | Decrement variable | DEC val
1101 | Print value as char | PRINT CHR(val)
1110 | Print var as char | PRINT CHR(VAR)
1111 | Zero the value of var | VAR 0
'''


# Opcode made of {}s and " "s
# Value made of {}s, and +-*/%~!√^

CMD = "cmd"
VAL = "val"

OPS = {
    "...{}" : "OUT",
    "..{}." : "OUTV",
    "..{}{}": "STR",
    ".{}.." : "INC PTR",
    ".{}.{}": "DEC PTR",
    ".{}{}.": "PUT",
    ".{}{}{}": "IF",
    "{}..." : "WHILE",
    "{}..{}": "//",
    "{}.{}.": "END",
    "{}.{}{}": "INC",
    "{}{}..": "DEC",
    "{}{}.{}": "OUT CHR",
    "{}{}{}.": "OUTV CHR",
    "{}{}{}{}": "VAR 0"
}

def brackets_to_expr(src):
    src = src.replace("^", "**")
    src = src.replace("√", "math.sqrt(")
    src = src.replace("{}", "1")

    return eval(src)
    

def ast(code):
    bricks = []
    
    for line in code:
        try:
            op, data = line.split("\t")
        except:
            continue
        if op not in OPS:
            continue
        bricks.append({"cmd" : OPS[op], "val" : brackets_to_expr(data)})

    return bricks
        

class Interpreter():
    def __init__(self, code):
        self.registers = []
        self.program = code
        self.raw = ast(self.program)
        self.vp = 0 #variable pointer
        self.ip = 0 #instruction pointer
        self.do_skip = False
        self.jumps = []
        
    def execute(self, num_vars):
        self.registers = [0]*num_vars
        while self.ip < len(self.raw):
            cmd = self.raw[self.ip]
            if self.do_skip:
                if cmd[CMD] == "END":
                    self.do_skip = False
                else:
                    self.ip += 1
                    continue
                
            if cmd[CMD] == "OUT":
                print(cmd[VAL], end="")

            elif cmd[CMD] == "OUTV":
                print(self.registers[self.vp], end="")

            elif cmd[CMD] == "STR":
                registers[self.vp] = cmd[VAL]

            elif cmd[CMD] == "INC PTR":
                self.vp = (self.vp + cmd[VAL]) % len(self.registers)

            elif cmd[CMD] == "DEC PTR":
                self.vp = (self.vp - cmd[VAL]) % len(self.registers)

            elif cmd[CMD] == "PUT":
                temp = input(">")
                try:
                    self.registers[self.vp] = int(temp)
                except:
                    self.registers[self.vp] = temp

            elif cmd[CMD] == "INC":
                if type(registers[self.vp]) is str:
                    temp = ""

                    for char in registers[self.vp]:
                        temp += chr(ord(char) + cmd[VAL])

                    self.registers[self.vp] = temp

                else:
                    self.registers[self.vp] += cmd[VAL]

            elif cmd[CMD] == "DEC":
                if type(self.registers[self.vp]) is str:
                    temp = ""

                    for char in self.registers[self.vp]:
                        temp += chr(ord(char) - cmd[VAL])

                    self.registers[self.vp] = temp

                else:
                    self.registers[self.vp] -= 1

            elif cmd[CMD] == "OUT CHR":
                print(chr(cmd[VAL]), end="")

            elif cmd[CMD] == "OUTV CHR":
                if type(self.registers[self.vp]) is str:
                    print(self.registers[self.vp], end="")
                else:
                    print(ord(self.registers[self.vp]), end="")

            elif cmd[CMD] == "VAR 0":
                self.registers[self.vp] = 0

            elif cmd[CMD] == "IF":
                if not self.registers[self.vp]:
                    self.do_skip = True

            elif cmd[CMD] == "WHILE":
                if self.registers[self.vp]:
                    self.jumps.append(self.ip)
                else:
                    self.do_skip = True

            elif cmd[CMD] == "END":
                if len(self.jumps):
                    if self.registers[self.vp]:
                        self.ip = self.jumps[-1]
                    else:
                        self.jumps.pop()

            self.ip += 1

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="The location of the cf file to open")
    parser.add_argument("-v","--vars",
                        help="The number of variables in the regs",
                        type=int)

    args = parser.parse_args()

    try:
        file = open(args.file)
    except:
        print("File not found")
        exit()

    code = file.read()
    code = code.strip("\n").split("\n")

    x = Interpreter(code)

    if args.vars:
        x.execute(args.var)
    else:
        x.execute(30000)
    print()
