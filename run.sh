#!/bin/bash

# Cesta k ANTLR jaru
ANTLR_JAR="./antlr-4.13.2-complete.jar"

# 1. Vygenerování parseru (pokud se změní .g4 soubor)
echo "Generuji parser z gramatiky..."
java -jar $ANTLR_JAR -Dlanguage=Python3 -visitor PLC_Project.g4

# 2. Spuštění kompilátoru (Type Checker + Code Generator)
echo "Překládám test_program.txt..."
./venv/bin/python3 main.py test_program.txt

# 3. Spuštění výsledného kódu v interpretu (VM)
if [ -f generated_code.txt ]; then
    echo "Spouštím interpret..."
    ./venv/bin/python3 Interpreter.py generated_code.txt
else
    echo "Chyba: Kód nebyl vygenerován."
fi
