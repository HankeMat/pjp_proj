import sys

# Interpret zásobníkového kódu
class Interpreter:
    def __init__(self, instructions):
        self.instructions = [line.strip() for line in instructions if line.strip()]
        self.stack = []
        self.variables = {}
        self.labels = {}     # Label map: label_idx/name -> instruction_index
        self.pc = 0          # current instruction index
        self._find_labels()

    # search for all labels
    def _find_labels(self):
        for i, line in enumerate(self.instructions):
            parts = line.split()
            if parts[0] == 'label':
                self.labels[parts[1]] = i

    def run(self):
        while self.pc < len(self.instructions):
            instr = self.instructions[self.pc]
            parts = instr.split()
            cmd = parts[0]
            
            # pushes value at the top of the stack
            if cmd == 'push':
                t = parts[1] # Type (I, F, B, S)
                val_str = " ".join(parts[2:]) # joins all the other parts together splitted by space
                if t == 'I': 
                    val = int(val_str)
                elif t == 'F': 
                    val = float(val_str)
                elif t == 'B': 
                    val = (val_str.lower() == 'true')
                elif t == 'S': 
                    val = val_str.strip('"')
                    val = val.encode('utf-8').decode('unicode_escape')
                self.stack.append(val)
            
            # gets one char fropm a string based on the index
            elif cmd == 'get_char':
                idx = self.stack.pop()
                string = self.stack.pop()
                if 0 <= idx < len(string):
                    self.stack.append(string[idx])
                else:
                    print(f"Chyba: Index {idx} je mimo rozsah stringu (delka {len(string)}).")
                    sys.exit(1)

            # opens a file
            elif cmd == 'fopen':
                file_name = self.stack.pop()
                f = open(file_name, "a+")
                self.stack.append(f)

            # appends text to a file 
            elif cmd == 'fappend':
                count = int(parts[1])
                vals = []
                for _ in range(count):
                    vals.append(self.stack.pop())

                f = vals[count-1]
                f.write("".join(map(str, reversed(vals[:-1]))))
                f.flush()

            elif cmd == '<<':
                count = int(parts[1])

                vals = []
                for _ in range(count):
                    vals.append(self.stack.pop())

                f = vals[count-1]
                f.write("".join(map(str, reversed(vals[:-1]))))
                f.flush()

            # reads the entire content of a file
            elif cmd == 'fread':
                f = self.stack.pop()
                f.seek(0)
                self.stack.append(f.read())

            # removes the value from the top of the stack
            elif cmd == 'pop':
                self.stack.pop()
            
            # loads value from the variable to the stack
            elif cmd == 'load':
                name = parts[1]
                self.stack.append(self.variables.get(name, 0))
            
            # saves value from top of the stack to the variable
            elif cmd == 'save':
                name = parts[1]
                self.variables[name] = self.stack.pop()

            elif cmd == 'createarray':
                size = int(parts[1])
                # Initialize array with default values based on context if needed
                # but for now, just 0s or empty. 
                # Since we don't know the type here, we can just use 0.
                self.stack.append([0] * size)

            elif cmd == 'arrayload':
                name = parts[1]
                idx = self.stack.pop()
                arr = self.variables[name]
                if 0 <= idx < len(arr):
                    self.stack.append(arr[idx])
                else:
                    print(f"Chyba: Index {idx} mimo rozsah pole {name} (velikost {len(arr)}).")
                    sys.exit(1)

            elif cmd == 'arraysave':
                name = parts[1]
                val = self.stack.pop() # hodnota
                idx = self.stack.pop() # index
                arr = self.variables[name]
                if 0 <= idx < len(arr):
                    arr[idx] = val
                    self.stack.append(val) # Necháme hodnotu na zásobníku pro případné další použití/pop
                else:
                    print(f"Chyba: Index {idx} mimo rozsah pole {name} (velikost {len(arr)}).")
                    sys.exit(1)
            
            # Binary operations (a + b, a - b, ...)
            elif cmd == 'add':
                r = self.stack.pop(); 
                l = self.stack.pop(); 
                self.stack.append(l + r)
            elif cmd == 'sub':
                r = self.stack.pop(); 
                l = self.stack.pop(); 
                self.stack.append(l - r)
            elif cmd == 'mul':
                r = self.stack.pop(); 
                l = self.stack.pop(); 
                self.stack.append(l * r)
            elif cmd == 'div':
                r = self.stack.pop(); l = self.stack.pop()
                if isinstance(l, int) and isinstance(r, int):
                    self.stack.append(l // r) # Int division
                else:
                    self.stack.append(l / r)  # float division
            elif cmd == 'mod':
                r = self.stack.pop(); 
                l = self.stack.pop(); 
                self.stack.append(l % r)
            
            # logicall operations
            elif cmd == 'and':
                r = self.stack.pop(); 
                l = self.stack.pop(); 
                self.stack.append(l and r)
            elif cmd == 'or':
                r = self.stack.pop(); 
                l = self.stack.pop(); 
                self.stack.append(l or r)
            
            # Unary ops (-5 , !true)
            elif cmd == 'uminus':
                val = self.stack.pop(); 
                self.stack.append(-val)
            elif cmd == 'not':
                val = self.stack.pop(); 
                self.stack.append(not val)
            
            # concat
            elif cmd == 'concat':
                r = self.stack.pop(); 
                l = self.stack.pop(); 
                self.stack.append(str(l) + str(r))

            # itof
            elif cmd == 'itof':
                val = self.stack.pop(); 
                self.stack.append(float(val))
            
            # Comparing
            elif cmd == 'gt':
                r = self.stack.pop(); 
                l = self.stack.pop(); 
                self.stack.append(l > r)
            elif cmd == 'lt':
                r = self.stack.pop(); 
                l = self.stack.pop(); 
                self.stack.append(l < r)
            elif cmd == 'eq':
                r = self.stack.pop(); 
                l = self.stack.pop(); 
                self.stack.append(l == r)
            
            # Jumps
            elif cmd == 'jmp':
                self.pc = self.labels[parts[1]]
                continue # have to skip program counter iteration at the end
            elif cmd == 'fjmp':
                cond = self.stack.pop()
                if not cond:
                    self.pc = self.labels[parts[1]]
                    continue
            
            # print
            elif cmd == 'print':
                n = int(parts[1])
                vals = []
                for _ in range(n):
                    vals.append(self.stack.pop())
                # gotta reverse bcs the values are backwards on the stack
                print("".join(map(str, reversed(vals))))
            
            # read
            elif cmd == 'read':
                t = parts[1]
                val_str = input().strip()
                if t == 'I': val = int(val_str)
                elif t == 'F': val = float(val_str)
                elif t == 'B': val = val_str.lower() in ['true', '1']
                elif t == 'S': val = val_str
                self.stack.append(val)
            
            # label - interpretr just skips
            elif cmd == 'label':
                pass
            
            self.pc += 1

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Použití: python3 Interpreter.py <soubor_s_kodem>")
        sys.exit(1)
    with open(sys.argv[1], 'r') as f:
        interp = Interpreter(f.readlines())
        interp.run()
