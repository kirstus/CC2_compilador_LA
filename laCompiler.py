from antlr4 import *
from laLexer import laLexer
from laListener import laListener
from laParser import laParser
from laVisitor import laVisitor
from laErrorHandler import laErrorHandler
import argparse

parser = argparse.ArgumentParser(description='Compiler for Python Machine Learning Models', add_help=True)
#parser.add_argument('-f','--file', dest='filepath', type=str, required=True)
parser.add_argument('sourcefile', type=str)
parser.add_argument('output', type=str)
args = parser.parse_args()

#abrir arquivo de saída
saida = open(args.output, "w+")

# Parsear texto
if(args.sourcefile != None):
	text = FileStream(args.sourcefile, encoding = 'UTF-8')

# Análise léxica
try:
    lexer = laLexer(text)
except ParseCancellationException as pce:
    msg = pce.get_message()

stream = CommonTokenStream(lexer)

# Análise sintática
parser = laParser(stream)
parser._listeners = [laErrorHandler(saida)]
tree = parser.programa()