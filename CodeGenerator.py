from PLC_ProjectVisitor import PLC_ProjectVisitor
from PLC_ProjectParser import PLC_ProjectParser

# Generátor kódu - vytváří instrukce pro zásobníkový stroj (VM)
class CodeGenerator(PLC_ProjectVisitor):
    def __init__(self, symbol_table, node_types):
        self.symbol_table = symbol_table # Tabulka symbolů z TypeCheckeru
        self.node_types = node_types     # Typy uzlů z TypeCheckeru
        self.instructions = []           # Seznam vygenerovaných instrukcí
        self.label_count = 0             # Počítadlo pro unikátní návěstí

    def new_label(self):
        self.label_count += 1
        return self.label_count

    def add_instr(self, instr):
        self.instructions.append(instr)

    def visitProgram(self, ctx):
        # Inicializace proměnných na výchozí hodnoty (podle zadání: 0, 0.0, "", false)
        for name, var_type in self.symbol_table.items():
            if var_type == 'I': self.add_instr("push I 0")
            elif var_type == 'F': self.add_instr("push F 0.0")
            elif var_type == 'B': self.add_instr("push B false")
            elif var_type == 'S': self.add_instr('push S ""')
            self.add_instr(f"save {name}")
        
        for stmt in ctx.statement():
            self.visit(stmt)
        return None

    # Příkaz výraz: např. a = 5; (hodnota výrazu se na konci zahodí pomocí pop)
    def visitExpressionStatement(self, ctx):
        self.visit(ctx.expression())
        self.add_instr("pop")
        return None

    def visitLiteralExpr(self, ctx):
        t = self.node_types[ctx]
        val = ctx.literal().getText()
        self.add_instr(f"push {t} {val}")
        return t

    def visitIdentifierExpr(self, ctx):
        name = ctx.ID().getText()
        self.add_instr(f"load {name}")
        return self.node_types[ctx]

    def visitParenthesisExpr(self, ctx):
        return self.visit(ctx.expression())

    def visitUnaryMinusExpr(self, ctx):
        t = self.visit(ctx.expression())
        self.add_instr(f"uminus {t}")
        return t

    def visitLogicalNotExpr(self, ctx):
        self.visit(ctx.expression())
        self.add_instr("not")
        return 'B'

    # Pomocná metoda pro návštěvu výrazu a případné přetypování na požadovaný typ
    def visit_and_cast(self, expr_ctx, target_type):
        actual_type = self.visit(expr_ctx)
        if target_type == 'F' and actual_type == 'I':
            self.add_instr("itof") # Převede int na float na vrcholu zásobníku
        return target_type

    def visitMultiplicativeExpr(self, ctx):
        res_type = self.node_types[ctx]
        op = ctx.op.text
        self.visit_and_cast(ctx.expression(0), res_type)
        self.visit_and_cast(ctx.expression(1), res_type)
        if op == '*': self.add_instr(f"mul {res_type}")
        elif op == '/': self.add_instr(f"div {res_type}")
        elif op == '%': self.add_instr("mod")
        return res_type

    def visitAdditiveExpr(self, ctx):
        res_type = self.node_types[ctx]
        op = ctx.op.text
        if op == '.':
            self.visit(ctx.expression(0))
            self.visit(ctx.expression(1))
            self.add_instr("concat")
            return 'S'
        self.visit_and_cast(ctx.expression(0), res_type)
        self.visit_and_cast(ctx.expression(1), res_type)
        if op == '+': self.add_instr(f"add {res_type}")
        elif op == '-': self.add_instr(f"sub {res_type}")
        return res_type

    def visitRelationalExpr(self, ctx):
        op = ctx.op.text
        # Pro porovnání určíme společný typ (pokud je jeden float, oba budou float)
        l_type = self.node_types[ctx.expression(0)]
        r_type = self.node_types[ctx.expression(1)]
        common_type = 'F' if (l_type == 'F' or r_type == 'F') else 'I'
        self.visit_and_cast(ctx.expression(0), common_type)
        self.visit_and_cast(ctx.expression(1), common_type)
        if op == '>': self.add_instr(f"gt {common_type}")
        elif op == '<': self.add_instr(f"lt {common_type}")
        return 'B'

    def visitEqualityExpr(self, ctx):
        op = ctx.op.text
        l_type = self.node_types[ctx.expression(0)]
        r_type = self.node_types[ctx.expression(1)]
        if l_type in ['I', 'F'] and r_type in ['I', 'F']:
            common_type = 'F' if (l_type == 'F' or r_type == 'F') else 'I'
        else:
            common_type = l_type
        
        self.visit_and_cast(ctx.expression(0), common_type)
        self.visit_and_cast(ctx.expression(1), common_type)
        self.add_instr(f"eq {common_type}")
        if op == '!=': self.add_instr("not")
        return 'B'

    def visitLogicalAndExpr(self, ctx):
        self.visit(ctx.expression(0))
        self.visit(ctx.expression(1))
        self.add_instr("and")
        return 'B'

    def visitLogicalOrExpr(self, ctx):
        self.visit(ctx.expression(0))
        self.visit(ctx.expression(1))
        self.add_instr("or")
        return 'B'

    def visitAssignmentExpr(self, ctx):
        name = ctx.ID().getText()
        var_type = self.symbol_table[name]
        self.visit_and_cast(ctx.expression(), var_type)
        self.add_instr(f"save {name}") # Uloží hodnotu do proměnné
        self.add_instr(f"load {name}") # Přiřazení vrací hodnotu (pro a = b = 5)
        return var_type

    def visitWriteStatement(self, ctx):
        exprs = ctx.exprList().expression()
        for expr in exprs:
            self.visit(expr)
        self.add_instr(f"print {len(exprs)}")
        return None

    def visitReadStatement(self, ctx):
        for id_node in ctx.idList().ID():
            name = id_node.getText()
            var_type = self.symbol_table[name]
            self.add_instr(f"read {var_type}")
            self.add_instr(f"save {name}")
        return None

    def visitBlockStatement(self, ctx):
        for stmt in ctx.statement():
            self.visit(stmt)
        return None

    def visitIfStatement(self, ctx):
        l_else = self.new_label()
        l_end = self.new_label()
        
        self.visit(ctx.expression())
        self.add_instr(f"fjmp {l_else}") # Skoč na else, pokud je podmínka false
        self.visit(ctx.statement(0))
        self.add_instr(f"jmp {l_end}")
        self.add_instr(f"label {l_else}")
        if ctx.ELSE():
            self.visit(ctx.statement(1))
        self.add_instr(f"label {l_end}")
        return None

    def visitWhileStatement(self, ctx):
        l_start = self.new_label()
        l_end = self.new_label()
        
        self.add_instr(f"label {l_start}")
        self.visit(ctx.expression())
        self.add_instr(f"fjmp {l_end}") # Skoč na konec, pokud je podmínka false
        self.visit(ctx.statement())
        self.add_instr(f"jmp {l_start}")
        self.add_instr(f"label {l_end}")
        return None
