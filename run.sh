#!/bin/bash

# Cesta k ANTLR jaru
ANTLR_JAR="./antlr-4.13.2-complete.jar"

# 1. Vygenerovani parseru (pokud se změní .g4 soubor jinak ne)
echo "Generuji parser z gramatiky..."
java -jar $ANTLR_JAR -Dlanguage=Python3 -visitor PLC_Project.g4

# 2. Spusteni kompilatoru (Type Checker + Code Generator)
INPUT_FILE=${1:-test_program.txt}
echo "Prekladam $INPUT_FILE..."
if ./.venv/bin/python3 main.py "$INPUT_FILE"; then
    # 3. Spusteni kodu v interpretru
    if [ -f generated_code.txt ]; then
        echo "Spoustim interpretr..."
        ./.venv/bin/python3 Interpreter.py generated_code.txt
    else
        echo "Chyba: Kod nebyl vygenerovan."
    fi
else
    echo "Preklad selhal (Type error nebo Syntax error). Interpret se nespusti."
    exit 1
fi
