from antlr4 import *
from laLexer import laLexer
from laListener import laListener
from laParser import laParser
from laVisitor import laVisitor
from laErrorHandler import laErrorHandler
import argparse

parser = argparse.ArgumentParser(description='Compiler for Python Machine Learning Models', add_help=True)
parser.add_argument('-f','--file', dest='filepath', type=str, required=True)
args = parser.parse_args()

# Parsear texto
if(args.filepath != None):
	text = FileStream(args.filepath, encoding = 'UTF-8')

# Análise léxica
try:
    lexer = laLexer(text)
except ParseCancellationException as pce:
    msg = pce.get_message()

stream = CommonTokenStream(lexer)

# Análise sintática
parser = laParser(stream)
parser._listeners = [laErrorHandler()]
tree = parser.programa()