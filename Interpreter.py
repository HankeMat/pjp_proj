import sys

# Interpret zásobníkového kódu
class Interpreter:
    def __init__(self, instructions):
        # Očistíme instrukce od prázdných řádků
        self.instructions = [line.strip() for line in instructions if line.strip()]
        self.stack = []      # Zásobník pro výpočty
        self.variables = {}  # Paměť pro proměnné
        self.labels = {}     # Mapa návěstí: název_návěstí -> index_instrukce
        self.pc = 0          # Program Counter - index aktuální instrukce
        self._find_labels()

    # První průchod: najdeme všechna návěstí (label), abychom věděli kam skákat
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
            
            # PUSH: vloží hodnotu na zásobník
            if cmd == 'push':
                t = parts[1] # Typ (I, F, B, S)
                val_str = " ".join(parts[2:]) # Hodnota (může obsahovat mezery v řetězcích)
                if t == 'I': val = int(val_str)
                elif t == 'F': val = float(val_str)
                elif t == 'B': val = (val_str.lower() == 'true')
                elif t == 'S': val = val_str.strip('"')
                self.stack.append(val)
            
            # POP: odstraní hodnotu z vrcholu zásobníku
            elif cmd == 'pop':
                self.stack.pop()
            
            # LOAD: načte hodnotu proměnné na zásobník
            elif cmd == 'load':
                name = parts[1]
                self.stack.append(self.variables.get(name, 0))
            
            # SAVE: uloží hodnotu z vrcholu zásobníku do proměnné
            elif cmd == 'save':
                name = parts[1]
                self.variables[name] = self.stack.pop()
            
            # Binární operace
            elif cmd == 'add':
                r = self.stack.pop(); l = self.stack.pop(); self.stack.append(l + r)
            elif cmd == 'sub':
                r = self.stack.pop(); l = self.stack.pop(); self.stack.append(l - r)
            elif cmd == 'mul':
                r = self.stack.pop(); l = self.stack.pop(); self.stack.append(l * r)
            elif cmd == 'div':
                r = self.stack.pop(); l = self.stack.pop()
                if isinstance(l, int) and isinstance(r, int):
                    self.stack.append(l // r) # Celočíselné dělení
                else:
                    self.stack.append(l / r)
            elif cmd == 'mod':
                r = self.stack.pop(); l = self.stack.pop(); self.stack.append(l % r)
            
            # Logické operace
            elif cmd == 'and':
                r = self.stack.pop(); l = self.stack.pop(); self.stack.append(l and r)
            elif cmd == 'or':
                r = self.stack.pop(); l = self.stack.pop(); self.stack.append(l or r)
            
            # Unární operace
            elif cmd == 'uminus':
                val = self.stack.pop(); self.stack.append(-val)
            elif cmd == 'not':
                val = self.stack.pop(); self.stack.append(not val)
            
            # Speciální operace
            elif cmd == 'concat':
                r = self.stack.pop(); l = self.stack.pop(); self.stack.append(str(l) + str(r))
            elif cmd == 'itof':
                val = self.stack.pop(); self.stack.append(float(val))
            
            # Porovnávání
            elif cmd == 'gt':
                r = self.stack.pop(); l = self.stack.pop(); self.stack.append(l > r)
            elif cmd == 'lt':
                r = self.stack.pop(); l = self.stack.pop(); self.stack.append(l < r)
            elif cmd == 'eq':
                r = self.stack.pop(); l = self.stack.pop(); self.stack.append(l == r)
            
            # Skoky
            elif cmd == 'jmp':
                self.pc = self.labels[parts[1]]
                continue # Přeskočíme standardní pc += 1 na konci cyklu
            elif cmd == 'fjmp':
                cond = self.stack.pop()
                if not cond:
                    self.pc = self.labels[parts[1]]
                    continue
            
            # Výstup
            elif cmd == 'print':
                n = int(parts[1])
                vals = []
                for _ in range(n):
                    vals.append(self.stack.pop())
                # Hodnoty na zásobníku jsou v obráceném pořadí
                print("".join(map(str, reversed(vals))))
            
            # Vstup
            elif cmd == 'read':
                t = parts[1]
                val_str = input().strip()
                if t == 'I': val = int(val_str)
                elif t == 'F': val = float(val_str)
                elif t == 'B': val = val_str.lower() in ['true', '1']
                elif t == 'S': val = val_str
                self.stack.append(val)
            
            # Návěstí (label) - interpret ho jen přeskočí
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
