# Generated from PLC_Project.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .PLC_ProjectParser import PLC_ProjectParser
else:
    from PLC_ProjectParser import PLC_ProjectParser

# This class defines a complete listener for a parse tree produced by PLC_ProjectParser.
class PLC_ProjectListener(ParseTreeListener):

    # Enter a parse tree produced by PLC_ProjectParser#program.
    def enterProgram(self, ctx:PLC_ProjectParser.ProgramContext):
        pass

    # Exit a parse tree produced by PLC_ProjectParser#program.
    def exitProgram(self, ctx:PLC_ProjectParser.ProgramContext):
        pass


    # Enter a parse tree produced by PLC_ProjectParser#emptyStatement.
    def enterEmptyStatement(self, ctx:PLC_ProjectParser.EmptyStatementContext):
        pass

    # Exit a parse tree produced by PLC_ProjectParser#emptyStatement.
    def exitEmptyStatement(self, ctx:PLC_ProjectParser.EmptyStatementContext):
        pass


    # Enter a parse tree produced by PLC_ProjectParser#declarationStatement.
    def enterDeclarationStatement(self, ctx:PLC_ProjectParser.DeclarationStatementContext):
        pass

    # Exit a parse tree produced by PLC_ProjectParser#declarationStatement.
    def exitDeclarationStatement(self, ctx:PLC_ProjectParser.DeclarationStatementContext):
        pass


    # Enter a parse tree produced by PLC_ProjectParser#expressionStatement.
    def enterExpressionStatement(self, ctx:PLC_ProjectParser.ExpressionStatementContext):
        pass

    # Exit a parse tree produced by PLC_ProjectParser#expressionStatement.
    def exitExpressionStatement(self, ctx:PLC_ProjectParser.ExpressionStatementContext):
        pass


    # Enter a parse tree produced by PLC_ProjectParser#readStatement.
    def enterReadStatement(self, ctx:PLC_ProjectParser.ReadStatementContext):
        pass

    # Exit a parse tree produced by PLC_ProjectParser#readStatement.
    def exitReadStatement(self, ctx:PLC_ProjectParser.ReadStatementContext):
        pass


    # Enter a parse tree produced by PLC_ProjectParser#writeStatement.
    def enterWriteStatement(self, ctx:PLC_ProjectParser.WriteStatementContext):
        pass

    # Exit a parse tree produced by PLC_ProjectParser#writeStatement.
    def exitWriteStatement(self, ctx:PLC_ProjectParser.WriteStatementContext):
        pass


    # Enter a parse tree produced by PLC_ProjectParser#blockStatement.
    def enterBlockStatement(self, ctx:PLC_ProjectParser.BlockStatementContext):
        pass

    # Exit a parse tree produced by PLC_ProjectParser#blockStatement.
    def exitBlockStatement(self, ctx:PLC_ProjectParser.BlockStatementContext):
        pass


    # Enter a parse tree produced by PLC_ProjectParser#ifStatement.
    def enterIfStatement(self, ctx:PLC_ProjectParser.IfStatementContext):
        pass

    # Exit a parse tree produced by PLC_ProjectParser#ifStatement.
    def exitIfStatement(self, ctx:PLC_ProjectParser.IfStatementContext):
        pass


    # Enter a parse tree produced by PLC_ProjectParser#whileStatement.
    def enterWhileStatement(self, ctx:PLC_ProjectParser.WhileStatementContext):
        pass

    # Exit a parse tree produced by PLC_ProjectParser#whileStatement.
    def exitWhileStatement(self, ctx:PLC_ProjectParser.WhileStatementContext):
        pass


    # Enter a parse tree produced by PLC_ProjectParser#forStatement.
    def enterForStatement(self, ctx:PLC_ProjectParser.ForStatementContext):
        pass

    # Exit a parse tree produced by PLC_ProjectParser#forStatement.
    def exitForStatement(self, ctx:PLC_ProjectParser.ForStatementContext):
        pass


    # Enter a parse tree produced by PLC_ProjectParser#type.
    def enterType(self, ctx:PLC_ProjectParser.TypeContext):
        pass

    # Exit a parse tree produced by PLC_ProjectParser#type.
    def exitType(self, ctx:PLC_ProjectParser.TypeContext):
        pass


    # Enter a parse tree produced by PLC_ProjectParser#idList.
    def enterIdList(self, ctx:PLC_ProjectParser.IdListContext):
        pass

    # Exit a parse tree produced by PLC_ProjectParser#idList.
    def exitIdList(self, ctx:PLC_ProjectParser.IdListContext):
        pass


    # Enter a parse tree produced by PLC_ProjectParser#exprList.
    def enterExprList(self, ctx:PLC_ProjectParser.ExprListContext):
        pass

    # Exit a parse tree produced by PLC_ProjectParser#exprList.
    def exitExprList(self, ctx:PLC_ProjectParser.ExprListContext):
        pass


    # Enter a parse tree produced by PLC_ProjectParser#logicalNotExpr.
    def enterLogicalNotExpr(self, ctx:PLC_ProjectParser.LogicalNotExprContext):
        pass

    # Exit a parse tree produced by PLC_ProjectParser#logicalNotExpr.
    def exitLogicalNotExpr(self, ctx:PLC_ProjectParser.LogicalNotExprContext):
        pass


    # Enter a parse tree produced by PLC_ProjectParser#assignmentExpr.
    def enterAssignmentExpr(self, ctx:PLC_ProjectParser.AssignmentExprContext):
        pass

    # Exit a parse tree produced by PLC_ProjectParser#assignmentExpr.
    def exitAssignmentExpr(self, ctx:PLC_ProjectParser.AssignmentExprContext):
        pass


    # Enter a parse tree produced by PLC_ProjectParser#logicalOrExpr.
    def enterLogicalOrExpr(self, ctx:PLC_ProjectParser.LogicalOrExprContext):
        pass

    # Exit a parse tree produced by PLC_ProjectParser#logicalOrExpr.
    def exitLogicalOrExpr(self, ctx:PLC_ProjectParser.LogicalOrExprContext):
        pass


    # Enter a parse tree produced by PLC_ProjectParser#unaryMinusExpr.
    def enterUnaryMinusExpr(self, ctx:PLC_ProjectParser.UnaryMinusExprContext):
        pass

    # Exit a parse tree produced by PLC_ProjectParser#unaryMinusExpr.
    def exitUnaryMinusExpr(self, ctx:PLC_ProjectParser.UnaryMinusExprContext):
        pass


    # Enter a parse tree produced by PLC_ProjectParser#logicalAndExpr.
    def enterLogicalAndExpr(self, ctx:PLC_ProjectParser.LogicalAndExprContext):
        pass

    # Exit a parse tree produced by PLC_ProjectParser#logicalAndExpr.
    def exitLogicalAndExpr(self, ctx:PLC_ProjectParser.LogicalAndExprContext):
        pass


    # Enter a parse tree produced by PLC_ProjectParser#literalExpr.
    def enterLiteralExpr(self, ctx:PLC_ProjectParser.LiteralExprContext):
        pass

    # Exit a parse tree produced by PLC_ProjectParser#literalExpr.
    def exitLiteralExpr(self, ctx:PLC_ProjectParser.LiteralExprContext):
        pass


    # Enter a parse tree produced by PLC_ProjectParser#additiveExpr.
    def enterAdditiveExpr(self, ctx:PLC_ProjectParser.AdditiveExprContext):
        pass

    # Exit a parse tree produced by PLC_ProjectParser#additiveExpr.
    def exitAdditiveExpr(self, ctx:PLC_ProjectParser.AdditiveExprContext):
        pass


    # Enter a parse tree produced by PLC_ProjectParser#relationalExpr.
    def enterRelationalExpr(self, ctx:PLC_ProjectParser.RelationalExprContext):
        pass

    # Exit a parse tree produced by PLC_ProjectParser#relationalExpr.
    def exitRelationalExpr(self, ctx:PLC_ProjectParser.RelationalExprContext):
        pass


    # Enter a parse tree produced by PLC_ProjectParser#parenthesisExpr.
    def enterParenthesisExpr(self, ctx:PLC_ProjectParser.ParenthesisExprContext):
        pass

    # Exit a parse tree produced by PLC_ProjectParser#parenthesisExpr.
    def exitParenthesisExpr(self, ctx:PLC_ProjectParser.ParenthesisExprContext):
        pass


    # Enter a parse tree produced by PLC_ProjectParser#multiplicativeExpr.
    def enterMultiplicativeExpr(self, ctx:PLC_ProjectParser.MultiplicativeExprContext):
        pass

    # Exit a parse tree produced by PLC_ProjectParser#multiplicativeExpr.
    def exitMultiplicativeExpr(self, ctx:PLC_ProjectParser.MultiplicativeExprContext):
        pass


    # Enter a parse tree produced by PLC_ProjectParser#equalityExpr.
    def enterEqualityExpr(self, ctx:PLC_ProjectParser.EqualityExprContext):
        pass

    # Exit a parse tree produced by PLC_ProjectParser#equalityExpr.
    def exitEqualityExpr(self, ctx:PLC_ProjectParser.EqualityExprContext):
        pass


    # Enter a parse tree produced by PLC_ProjectParser#identifierExpr.
    def enterIdentifierExpr(self, ctx:PLC_ProjectParser.IdentifierExprContext):
        pass

    # Exit a parse tree produced by PLC_ProjectParser#identifierExpr.
    def exitIdentifierExpr(self, ctx:PLC_ProjectParser.IdentifierExprContext):
        pass


    # Enter a parse tree produced by PLC_ProjectParser#literal.
    def enterLiteral(self, ctx:PLC_ProjectParser.LiteralContext):
        pass

    # Exit a parse tree produced by PLC_ProjectParser#literal.
    def exitLiteral(self, ctx:PLC_ProjectParser.LiteralContext):
        pass



del PLC_ProjectParser