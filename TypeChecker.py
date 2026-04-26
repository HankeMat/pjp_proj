from PLC_ProjectVisitor import PLC_ProjectVisitor
from PLC_ProjectParser import PLC_ProjectParser

class TypeChecker(PLC_ProjectVisitor):
    def __init__(self):
        self.symbol_table = {}  # Symbol table: variable_name -> type (I, F, B, S)
        self.node_types = {}    # Table for result data types of each expression (for generator)
        self.errors = []       

    def report_error(self, ctx, message):
        line, column = 0, 0
        if hasattr(ctx, 'start') and hasattr(ctx.start, 'line'):
            line = ctx.start.line
            column = ctx.start.column
        elif hasattr(ctx, 'line'):
            line = ctx.line
            column = ctx.column
        self.errors.append(f"{line}:{column} - {message}")

    # Variable declaration: (int a, b;)
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

    # Variable check
    def visitIdentifierExpr(self, ctx):
        name = ctx.ID().getText()
        if name not in self.symbol_table:
            self.report_error(ctx.ID().getSymbol(), f"Proměnná '{name}' nebyla deklarována.")
            t = 'ERROR'
        else:
            t = self.symbol_table[name]
        self.node_types[ctx] = t
        return t

    # Literals check (numbers, true/false, strings)
    def visitLiteralExpr(self, ctx):
        lit = ctx.literal()
        if lit.INT(): t = 'I'
        elif lit.FLOAT(): t = 'F'
        elif lit.BOOL(): t = 'B'
        elif lit.STRING(): t = 'S'
        else: t = 'ERROR'
        self.node_types[ctx] = t
        return t

    # Parentehesis ckeck (just goes recursively inside and returns its result type)
    def visitParenthesisExpr(self, ctx):
        t = self.visit(ctx.expression())
        self.node_types[ctx] = t
        return t

    # Unary minus (works just for numbers ofc)
    def visitUnaryMinusExpr(self, ctx):
        t = self.visit(ctx.expression())
        if t not in ['I', 'F']:
            self.report_error(ctx, "Unární mínus vyžaduje 'int' nebo 'float'.")
            t = 'ERROR'
        self.node_types[ctx] = t
        return t

    # NOT
    def visitLogicalNotExpr(self, ctx):
        t = self.visit(ctx.expression())
        if t != 'B':
            self.report_error(ctx, "Logická negace vyžaduje 'bool'.")
            t = 'ERROR'
        self.node_types[ctx] = 'B'
        return 'B'

    # Helper for resolution data type of the binary operation (+, -, *, ==, ...) result
    def get_binary_type(self, left, right, op, ctx):
        if left == 'ERROR' or right == 'ERROR': 
            return 'ERROR'
        
        # If there is one float result is float
        if op in ['+', '-', '*', '/']:
            if left in ['I', 'F'] and right in ['I', 'F']:
                return 'F' if (left == 'F' or right == 'F') else 'I'
            
            self.report_error(ctx, f"Operátor '{op}' vyžaduje číselné typy.")
            return 'ERROR'
        
        # Modulo is for int only
        if op == '%':
            if left == 'I' and right == 'I': return 'I'
            self.report_error(ctx, "Modulo '%' vyžaduje 'int'.")
            return 'ERROR'
            
        # Concat
        if op == '.':
            if left == 'S' and right == 'S': return 'S'
            self.report_error(ctx, "Konkatenace '.' vyžaduje 'string'.")
            return 'ERROR'
            
        # Comparison
        if op in ['<', '>']:
            if left in ['I', 'F'] and right in ['I', 'F']: return 'B'
            self.report_error(ctx, f"Porovnání '{op}' vyžaduje číselné typy.")
            return 'ERROR'
            
        # Equality
        if op in ['==', '!=']:
            if left == right and left in ['I', 'F', 'S', 'B']: return 'B'
            if left in ['I', 'F'] and right in ['I', 'F']: return 'B'
            self.report_error(ctx, f"Porovnání '{op}' vyžaduje kompatibilní typy.")
            return 'ERROR'
            
        return 'ERROR'

    # * / %
    def visitMultiplicativeExpr(self, ctx):
        l = self.visit(ctx.expression(0))
        r = self.visit(ctx.expression(1))
        t = self.get_binary_type(l, r, ctx.op.text, ctx)
        self.node_types[ctx] = t
        return t
    
    # + - .
    def visitAdditiveExpr(self, ctx):
        l = self.visit(ctx.expression(0))
        r = self.visit(ctx.expression(1))
        t = self.get_binary_type(l, r, ctx.op.text, ctx)
        self.node_types[ctx] = t
        return t
    
    # < >
    def visitRelationalExpr(self, ctx):
        l = self.visit(ctx.expression(0))
        r = self.visit(ctx.expression(1))
        t = self.get_binary_type(l, r, ctx.op.text, ctx)
        self.node_types[ctx] = t
        return t
    
    # == !=
    def visitEqualityExpr(self, ctx):
        l = self.visit(ctx.expression(0))
        r = self.visit(ctx.expression(1))
        t = self.get_binary_type(l, r, ctx.op.text, ctx)
        self.node_types[ctx] = t
        return t
    
    # &&
    def visitLogicalAndExpr(self, ctx):
        l = self.visit(ctx.expression(0))
        r = self.visit(ctx.expression(1))
        if l == 'B' and r == 'B': t = 'B'
        else:
            self.report_error(ctx, "Logické AND vyžaduje 'bool'.")
            t = 'ERROR'
        self.node_types[ctx] = t
        return t
    
    # ||
    def visitLogicalOrExpr(self, ctx):
        l = self.visit(ctx.expression(0))
        r = self.visit(ctx.expression(1))
        if l == 'B' and r == 'B': t = 'B'
        else:
            self.report_error(ctx, "Logické OR vyžaduje 'bool'.")
            t = 'ERROR'
        self.node_types[ctx] = t
        return t

    # Assignment (a = 5;)
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
        
        # data type compatibility check
        if var_type == expr_type:
            self.node_types[ctx] = var_type
            return var_type
        if var_type == 'F' and expr_type == 'I':
            # Auto casting
            self.node_types[ctx] = 'F'
            return 'F'
        
        self.report_error(ctx, f"Nelze přiřadit typ '{expr_type}' do proměnné '{name}' typu '{var_type}'.")
        self.node_types[ctx] = 'ERROR'
        return 'ERROR'

    # if
    def visitIfStatement(self, ctx):
        cond_type = self.visit(ctx.expression())
        if cond_type != 'B':
            self.report_error(ctx.expression(), "Podmínka v 'if' musí být 'bool'.")
        self.visit(ctx.statement(0))
        if ctx.ELSE():
            self.visit(ctx.statement(1))
        return None

    # while
    def visitWhileStatement(self, ctx):
        cond_type = self.visit(ctx.expression())
        if cond_type != 'B':
            self.report_error(ctx.expression(), "Podmínka ve 'while' musí být 'bool'.")
        self.visit(ctx.statement())
        return None

    # read
    def visitReadStatement(self, ctx):
        for id_node in ctx.idList().ID():
            name = id_node.getText()
            if name not in self.symbol_table:
                self.report_error(id_node.getSymbol(), f"Proměnná '{name}' nebyla deklarována.")
        return None

    # write
    def visitWriteStatement(self, ctx):
        for expr in ctx.exprList().expression():
            self.visit(expr)
        return None
