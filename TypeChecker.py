from PLC_ProjectVisitor import PLC_ProjectVisitor
from PLC_ProjectParser import PLC_ProjectParser

class TypeChecker(PLC_ProjectVisitor):
    def __init__(self):
        self.symbol_table = {} # Symbol table: variable_name -> type (I, F, B, S)
        self.node_types = {}   # Pomocná tabulka pro uložení výsledného typu každého výrazu (pro generátor)
        self.errors = []

    def report_error(self, ctx, message):
        line = ctx.start.line
        column = ctx.start.column
        self.errors.append(f"{line}:{column} - {message}")

    # Variable declaration: e.g. int a, b;
    def visitDeclarationStatement(self, ctx):
        var_type_str = ctx.type_().getText()
        type_map = {'int': 'I', 'float': 'F', 'bool': 'B', 'string': 'S'}
        var_type = type_map.get(var_type_str)
        for id_node in ctx.idList().ID():
            name = id_node.getText()
            if name in self.symbol_table:
                self.report_error(id_node.getSymbol(), f"Proměnná '{name}' již byla deklarována.")
            else:
                self.symbol_table[name] = var_type
        return None

    # Použití proměnné ve výrazu
    def visitIdentifierExpr(self, ctx):
        name = ctx.ID().getText()
        if name not in self.symbol_table:
            self.report_error(ctx.ID().getSymbol(), f"Proměnná '{name}' nebyla deklarována.")
            t = 'ERROR'
        else:
            t = self.symbol_table[name]
        self.node_types[ctx] = t
        return t

    # Literály (čísla, true/false, řetězce)
    def visitLiteralExpr(self, ctx):
        lit = ctx.literal()
        if lit.INT(): t = 'I'
        elif lit.FLOAT(): t = 'F'
        elif lit.BOOL(): t = 'B'
        elif lit.STRING(): t = 'S'
        else: t = 'ERROR'
        self.node_types[ctx] = t
        return t

    def visitParenthesisExpr(self, ctx):
        t = self.visit(ctx.expression())
        self.node_types[ctx] = t
        return t

    def visitUnaryMinusExpr(self, ctx):
        t = self.visit(ctx.expression())
        if t not in ['I', 'F']:
            self.report_error(ctx, "Unární mínus vyžaduje 'int' nebo 'float'.")
            t = 'ERROR'
        self.node_types[ctx] = t
        return t

    def visitLogicalNotExpr(self, ctx):
        t = self.visit(ctx.expression())
        if t != 'B':
            self.report_error(ctx, "Logická negace vyžaduje 'bool'.")
            t = 'ERROR'
        self.node_types[ctx] = 'B'
        return 'B'

    # Pomocná funkce pro určení typu výsledku binární operace
    def get_binary_type(self, left, right, op, ctx):
        if left == 'ERROR' or right == 'ERROR': return 'ERROR'
        
        # Aritmetika: pokud je jeden float, výsledek je float
        if op in ['+', '-', '*', '/']:
            if left in ['I', 'F'] and right in ['I', 'F']:
                return 'F' if (left == 'F' or right == 'F') else 'I'
            self.report_error(ctx, f"Operátor '{op}' vyžaduje číselné typy.")
            return 'ERROR'
        
        # Modulo pouze pro int
        if op == '%':
            if left == 'I' and right == 'I': return 'I'
            self.report_error(ctx, "Modulo '%' vyžaduje 'int'.")
            return 'ERROR'
            
        # Spojování řetězců
        if op == '.':
            if left == 'S' and right == 'S': return 'S'
            self.report_error(ctx, "Konkatenace '.' vyžaduje 'string'.")
            return 'ERROR'
            
        # Relace (<, >)
        if op in ['<', '>']:
            if left in ['I', 'F'] and right in ['I', 'F']: return 'B'
            self.report_error(ctx, f"Porovnání '{op}' vyžaduje číselné typy.")
            return 'ERROR'
            
        # Rovnost (==, !=)
        if op in ['==', '!=']:
            if left == right and left in ['I', 'F', 'S', 'B']: return 'B'
            if left in ['I', 'F'] and right in ['I', 'F']: return 'B' # Porovnání int a float je ok
            self.report_error(ctx, f"Porovnání '{op}' vyžaduje kompatibilní typy.")
            return 'ERROR'
            
        return 'ERROR'

    def visitMultiplicativeExpr(self, ctx):
        l = self.visit(ctx.expression(0))
        r = self.visit(ctx.expression(1))
        t = self.get_binary_type(l, r, ctx.op.text, ctx)
        self.node_types[ctx] = t
        return t

    def visitAdditiveExpr(self, ctx):
        l = self.visit(ctx.expression(0))
        r = self.visit(ctx.expression(1))
        t = self.get_binary_type(l, r, ctx.op.text, ctx)
        self.node_types[ctx] = t
        return t

    def visitRelationalExpr(self, ctx):
        l = self.visit(ctx.expression(0))
        r = self.visit(ctx.expression(1))
        t = self.get_binary_type(l, r, ctx.op.text, ctx)
        self.node_types[ctx] = t
        return t

    def visitEqualityExpr(self, ctx):
        l = self.visit(ctx.expression(0))
        r = self.visit(ctx.expression(1))
        t = self.get_binary_type(l, r, ctx.op.text, ctx)
        self.node_types[ctx] = t
        return t

    def visitLogicalAndExpr(self, ctx):
        l = self.visit(ctx.expression(0))
        r = self.visit(ctx.expression(1))
        if l == 'B' and r == 'B': t = 'B'
        else:
            self.report_error(ctx, "Logické AND vyžaduje 'bool'.")
            t = 'ERROR'
        self.node_types[ctx] = t
        return t

    def visitLogicalOrExpr(self, ctx):
        l = self.visit(ctx.expression(0))
        r = self.visit(ctx.expression(1))
        if l == 'B' and r == 'B': t = 'B'
        else:
            self.report_error(ctx, "Logické OR vyžaduje 'bool'.")
            t = 'ERROR'
        self.node_types[ctx] = t
        return t

    # Přiřazení: a = výraz
    def visitAssignmentExpr(self, ctx):
        name = ctx.ID().getText()
        if name not in self.symbol_table:
            self.report_error(ctx.ID().getSymbol(), f"Proměnná '{name}' nebyla deklarována.")
            var_type = 'ERROR'
        else:
            var_type = self.symbol_table[name]
        
        expr_type = self.visit(ctx.expression())
        
        if var_type == 'ERROR' or expr_type == 'ERROR':
            self.node_types[ctx] = 'ERROR'
            return 'ERROR'
        
        # Kontrola kompatibility typů při přiřazení
        if var_type == expr_type:
            self.node_types[ctx] = var_type
            return var_type
        if var_type == 'F' and expr_type == 'I':
            # Automatické přetypování int -> float je povoleno
            self.node_types[ctx] = 'F'
            return 'F'
        
        self.report_error(ctx, f"Nelze přiřadit typ '{expr_type}' do proměnné '{name}' typu '{var_type}'.")
        self.node_types[ctx] = 'ERROR'
        return 'ERROR'

    def visitIfStatement(self, ctx):
        cond_type = self.visit(ctx.expression())
        if cond_type != 'B':
            self.report_error(ctx.expression(), "Podmínka v 'if' musí být 'bool'.")
        self.visit(ctx.statement(0))
        if ctx.ELSE():
            self.visit(ctx.statement(1))
        return None
    
    def visitTernaryExpr(self, ctx):
        cond_type = self.visit(ctx.expression(0))
        if cond_type != 'B':
            self.report_error(ctx.expression(0), "Podmínka musí být 'bool'.")

        t1 = self.visit(ctx.expression(1))
        t2 = self.visit(ctx.expression(2))

        if t1 == t2:
            self.node_types[ctx] = t1
            return t1
        elif (t1 == 'I' and t2 == 'F') or (t1 == 'F' and t2 == 'I'):
            self.node_types[ctx] = 'F'
            return 'F'
        else:
            self.report_error(ctx, "Větve ternárního operátoru mají nekompatibilní typy.")
            return 'ERROR'

    def visitWhileStatement(self, ctx):
        cond_type = self.visit(ctx.expression())
        if cond_type != 'B':
            self.report_error(ctx.expression(), "Podmínka ve 'while' musí být 'bool'.")
        self.visit(ctx.statement())
        return None
    
    def visitForStatement(self, ctx):
        self.visit(ctx.expression(0))
        cond_type = self.visit(ctx.expression(1))
        self.visit(ctx.expression(2))
        if cond_type != 'B':
            self.report_error(ctx.expression(1), "Podmínka ve 'for' musí být 'bool'.")
        self.visit(ctx.statement())
        return None

    def visitReadStatement(self, ctx):
        for id_node in ctx.idList().ID():
            name = id_node.getText()
            if name not in self.symbol_table:
                self.report_error(id_node.getSymbol(), f"Proměnná '{name}' nebyla deklarována.")
        return None

    def visitWriteStatement(self, ctx):
        for expr in ctx.exprList().expression():
            self.visit(expr)
        return None

    def visitIndexingExpr(self, ctx):
        if self.visit(ctx.expression(0)) != 'S':
            self.report_error(ctx, "Indexoval lze pouze STRING.")
            return 'ERROR'
        
        if self.visit(ctx.expression(1)) != 'I':
            self.report_error(ctx, "Index musí být typu INT.")
            return 'ERROR'
        
        self.node_types[ctx] = 'S'
        return 'S'