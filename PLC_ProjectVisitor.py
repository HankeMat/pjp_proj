# Generated from PLC_Project.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .PLC_ProjectParser import PLC_ProjectParser
else:
    from PLC_ProjectParser import PLC_ProjectParser

# This class defines a complete generic visitor for a parse tree produced by PLC_ProjectParser.

class PLC_ProjectVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by PLC_ProjectParser#program.
    def visitProgram(self, ctx:PLC_ProjectParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PLC_ProjectParser#emptyStatement.
    def visitEmptyStatement(self, ctx:PLC_ProjectParser.EmptyStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PLC_ProjectParser#declarationStatement.
    def visitDeclarationStatement(self, ctx:PLC_ProjectParser.DeclarationStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PLC_ProjectParser#expressionStatement.
    def visitExpressionStatement(self, ctx:PLC_ProjectParser.ExpressionStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PLC_ProjectParser#readStatement.
    def visitReadStatement(self, ctx:PLC_ProjectParser.ReadStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PLC_ProjectParser#writeStatement.
    def visitWriteStatement(self, ctx:PLC_ProjectParser.WriteStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PLC_ProjectParser#blockStatement.
    def visitBlockStatement(self, ctx:PLC_ProjectParser.BlockStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PLC_ProjectParser#ifStatement.
    def visitIfStatement(self, ctx:PLC_ProjectParser.IfStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PLC_ProjectParser#whileStatement.
    def visitWhileStatement(self, ctx:PLC_ProjectParser.WhileStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PLC_ProjectParser#type.
    def visitType(self, ctx:PLC_ProjectParser.TypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PLC_ProjectParser#idList.
    def visitIdList(self, ctx:PLC_ProjectParser.IdListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PLC_ProjectParser#exprList.
    def visitExprList(self, ctx:PLC_ProjectParser.ExprListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PLC_ProjectParser#logicalNotExpr.
    def visitLogicalNotExpr(self, ctx:PLC_ProjectParser.LogicalNotExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PLC_ProjectParser#assignmentExpr.
    def visitAssignmentExpr(self, ctx:PLC_ProjectParser.AssignmentExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PLC_ProjectParser#logicalOrExpr.
    def visitLogicalOrExpr(self, ctx:PLC_ProjectParser.LogicalOrExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PLC_ProjectParser#unaryMinusExpr.
    def visitUnaryMinusExpr(self, ctx:PLC_ProjectParser.UnaryMinusExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PLC_ProjectParser#logicalAndExpr.
    def visitLogicalAndExpr(self, ctx:PLC_ProjectParser.LogicalAndExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PLC_ProjectParser#literalExpr.
    def visitLiteralExpr(self, ctx:PLC_ProjectParser.LiteralExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PLC_ProjectParser#additiveExpr.
    def visitAdditiveExpr(self, ctx:PLC_ProjectParser.AdditiveExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PLC_ProjectParser#relationalExpr.
    def visitRelationalExpr(self, ctx:PLC_ProjectParser.RelationalExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PLC_ProjectParser#parenthesisExpr.
    def visitParenthesisExpr(self, ctx:PLC_ProjectParser.ParenthesisExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PLC_ProjectParser#multiplicativeExpr.
    def visitMultiplicativeExpr(self, ctx:PLC_ProjectParser.MultiplicativeExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PLC_ProjectParser#equalityExpr.
    def visitEqualityExpr(self, ctx:PLC_ProjectParser.EqualityExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PLC_ProjectParser#identifierExpr.
    def visitIdentifierExpr(self, ctx:PLC_ProjectParser.IdentifierExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PLC_ProjectParser#literal.
    def visitLiteral(self, ctx:PLC_ProjectParser.LiteralContext):
        return self.visitChildren(ctx)



del PLC_ProjectParser