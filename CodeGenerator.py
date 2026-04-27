from PLC_ProjectVisitor import PLC_ProjectVisitor
from PLC_ProjectParser import PLC_ProjectParser

class CodeGenerator(PLC_ProjectVisitor):
    def __init__(self, symbol_table, node_types):
        self.symbol_table = symbol_table # Symbol table from typechecker: variable_name -> type (I, F, B, S)
        self.node_types = node_types     # Data types of each expression
        self.instructions = []           # Instructions
        self.label_count = 0             # Counter for label (so ewach is unique)

    def new_label(self):
        self.label_count += 1
        return self.label_count

    def add_instr(self, instr):
        self.instructions.append(instr)

    def visitProgram(self, ctx):
        # Init of variables to defaults (0, 0.0, "", false)
        for name, var_type in self.symbol_table.items():
            if var_type == 'I': self.add_instr("push I 0")
            elif var_type == 'F': self.add_instr("push F 0.0")
            elif var_type == 'B': self.add_instr("push B false")
            elif var_type == 'S': self.add_instr('push S ""')
            elif var_type == 'FI': self.add_instr('push FI 0')
            self.add_instr(f"save {name}")
        
        for stmt in ctx.statement():
            self.visit(stmt)
        return None

    # lonely expression :D (a = 5;) (value gets poped from stack at the end we dont need that)
    def visitExpressionStatement(self, ctx):
        self.visit(ctx.expression())
        self.add_instr("pop")
        return None

    # Literal expression means we have to push that onto stack
    def visitLiteralExpr(self, ctx):
        t = self.node_types[ctx]
        val = ctx.literal().getText()
        self.add_instr(f"push {t} {val}")
        return t

    # Calling identifier has to load value from that variable to the stack 
    def visitIdentifierExpr(self, ctx):
        name = ctx.ID().getText()
        self.add_instr(f"load {name}")
        return self.node_types[ctx]

    # Parenthesis .. just go inside
    def visitParenthesisExpr(self, ctx):
        return self.visit(ctx.expression())

    # Unary minus negetes value
    def visitUnaryMinusExpr(self, ctx):
        t = self.visit(ctx.expression())
        self.add_instr(f"uminus {t}")
        return t

    # NOT
    def visitLogicalNotExpr(self, ctx):
        self.visit(ctx.expression())
        self.add_instr("not")
        return 'B'

    # Auto cast
    def visit_and_cast(self, expr_ctx, target_type):
        actual_type = self.visit(expr_ctx)
        if target_type == 'F' and actual_type == 'I':
            self.add_instr("itof") # Converts int at the top of the stack to float
        return target_type

    # * / %
    def visitMultiplicativeExpr(self, ctx):
        res_type = self.node_types[ctx]
        op = ctx.op.text
        self.visit_and_cast(ctx.expression(0), res_type)
        self.visit_and_cast(ctx.expression(1), res_type)
        if op == '*': 
            self.add_instr(f"mul {res_type}")
        elif op == '/': 
            self.add_instr(f"div {res_type}")
        elif op == '%': 
            self.add_instr("mod")
        return res_type

    # + - .
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
        if op == '+': 
            self.add_instr(f"add {res_type}")
        elif op == '-': 
            self.add_instr(f"sub {res_type}")
        return res_type

    # < >
    def visitRelationalExpr(self, ctx):
        op = ctx.op.text
        # Common type is F if either of them is F
        l_type = self.node_types[ctx.expression(0)]
        r_type = self.node_types[ctx.expression(1)]
        common_type = 'F' if (l_type == 'F' or r_type == 'F') else 'I'
        self.visit_and_cast(ctx.expression(0), common_type)
        self.visit_and_cast(ctx.expression(1), common_type)
        if op == '>': 
            self.add_instr(f"gt {common_type}")
        elif op == '<': 
            self.add_instr(f"lt {common_type}")
        return 'B'

    # == !=
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
        if op == '!=': 
            self.add_instr("not")   # I just negate the equality result 
        return 'B'

    # AND
    def visitLogicalAndExpr(self, ctx):
        self.visit(ctx.expression(0))
        self.visit(ctx.expression(1))
        self.add_instr("and")
        return 'B'

    # OR
    def visitLogicalOrExpr(self, ctx):
        self.visit(ctx.expression(0))
        self.visit(ctx.expression(1))
        self.add_instr("or")
        return 'B'

    # = 
    def visitAssignmentExpr(self, ctx):
        name = ctx.ID().getText()
        var_type = self.symbol_table[name]
        self.visit_and_cast(ctx.expression(), var_type)
        self.add_instr(f"save {name}") # Saves value to the variable from top of the stack
        self.add_instr(f"load {name}") # I have to load that value back to the stack in case of a = b = 5
        return var_type

    # write
    def visitWriteStatement(self, ctx):
        exprs = ctx.exprList().expression()
        for expr in exprs:
            self.visit(expr)
        self.add_instr(f"print {len(exprs)}")
        return None

    # read
    def visitReadStatement(self, ctx):
        for id_node in ctx.idList().ID():
            name = id_node.getText()
            var_type = self.symbol_table[name]
            self.add_instr(f"read {var_type}")  # reads input of specified type
            self.add_instr(f"save {name}")      # saves it into the variable 
        return None

    # just statement parenthesis, we go inside
    def visitBlockStatement(self, ctx):
        for stmt in ctx.statement():
            self.visit(stmt)
        return None

    # if
    def visitIfStatement(self, ctx):
        l_else = self.new_label()
        l_end = self.new_label()
        
        self.visit(ctx.expression())
        self.add_instr(f"fjmp {l_else}") # Jump to else if condition is false
        self.visit(ctx.statement(0))
        self.add_instr(f"jmp {l_end}")
        self.add_instr(f"label {l_else}")
        if ctx.ELSE():
            self.visit(ctx.statement(1))
        self.add_instr(f"label {l_end}")
        return None
    
    def visitTernaryExpr(self, ctx):
        res_type = self.node_types[ctx]
        l_else = self.new_label()
        l_end = self.new_label()
        
        self.visit(ctx.expression(0))
        self.add_instr(f"fjmp {l_else}")    # Jump to else if condition is false
        
        self.visit_and_cast(ctx.expression(1),res_type)
        self.add_instr(f"jmp {l_end}")      # Jump to end

        self.add_instr(f"label {l_else}")   # else
        self.visit_and_cast(ctx.expression(2), res_type)
        self.add_instr(f"label {l_end}")    # End
        return res_type

    def visitWhileStatement(self, ctx):
        l_start = self.new_label()
        l_end = self.new_label()
        
        self.add_instr(f"label {l_start}")  # Start
        self.visit(ctx.expression())
        self.add_instr(f"fjmp {l_end}")     # Jump to the end if condition is false
        self.visit(ctx.statement())
        self.add_instr(f"jmp {l_start}")
        self.add_instr(f"label {l_end}")    # End
        return None 
    
    def visitForStatement(self, ctx):
        l_start = self.new_label()
        l_end = self.new_label()
        
        self.visit(ctx.expression(0))       # Inicialization
        self.add_instr("pop")               # Pop the result of the expression(0) - dont need it :)

        self.add_instr(f"label {l_start}")  # Start
        self.visit(ctx.expression(1))       # Condition
        self.add_instr(f"fjmp {l_end}")     # Jump to the end if condition is false
        self.visit(ctx.statement())         # Body

        self.visit(ctx.expression(2))       # Iteration
        self.add_instr("pop")               # Pop the result of the expression(2) - dont need it :)
        
        self.add_instr(f"jmp {l_start}")    # Jump to the start again
        self.add_instr(f"label {l_end}")    # End
        return None
    
    def visitIndexingExpr(self, ctx):
        self.visit(ctx.expression(0))
        self.visit(ctx.expression(1))
        self.add_instr("get_char")
        return 'S'

    def visitFopenStatement(self, ctx):
        self.visit(ctx.expression(1))
        self.add_instr("fopen")
        var_name = ctx.expression(0).getText()
        self.add_instr(f"save {var_name}")
        return None
    
    def visitFappendStatement(self, ctx):
        # load that FILE variable
        self.visit(ctx.expression())
        
        # all vars push onto the stack
        exprs = ctx.exprList().expression()
        for expr in exprs:
            self.visit(expr)
            
        # fappend number_of_pops (1 for the file + rest for variables/text)
        self.add_instr(f"fappend {len(exprs) + 1}")
        return None
    
    # read
    def visitFreadStatement(self, ctx):
        self.visit(ctx.expression())

        name = ctx.ID().getText()
        self.add_instr(f"fread")
        self.add_instr(f"save {name}")

        return None
    
    def visitArrowsStatement(self, ctx):
        # load the FILE variable onto stack
        self.visit(ctx.expression())

        # all vars push onto the stack
        exprs = ctx.inputList().expression()
        for expr in exprs:
            self.visit(expr)

        self.add_instr(f"<< {len(exprs) + 1}")
        return None