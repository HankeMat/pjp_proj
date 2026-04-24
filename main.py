import sys
from antlr4 import *
from PLC_ProjectLexer import PLC_ProjectLexer
from PLC_ProjectParser import PLC_ProjectParser
from TypeChecker import TypeChecker
from CodeGenerator import CodeGenerator

def main():
    if len(sys.argv) < 2:
        input_text = """
        int a, b;
        a = 5;
        b = a + 10 * 2;
        if (b > 20) {
            write "Greater than 20: ", b;
        } else {
            write "Less or equal 20: ", b;
        }
        """
    else:
        with open(sys.argv[1], 'r') as f:
            input_text = f.read()

    input_stream = InputStream(input_text)
    lexer = PLC_ProjectLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = PLC_ProjectParser(stream)
    
    tree = parser.program()
    
    if parser.getNumberOfSyntaxErrors() > 0:
        sys.exit(1)
    
    checker = TypeChecker()
    checker.visit(tree)
    
    if checker.errors:
        for err in checker.errors:
            print(err)
        sys.exit(1)
    
    generator = CodeGenerator(checker.symbol_table, checker.node_types)
    generator.visit(tree)
    
    output_file = "generated_code.txt"
    with open(output_file, 'w') as f:
        for instr in generator.instructions:
            f.write(instr + "\n")
    
    print(f"Code generated successfully in {output_file}!")

if __name__ == '__main__':
    main()
