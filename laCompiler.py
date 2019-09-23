from antlr4 import *
from laLexer import laLexer
from laListener import laListener
from laParser import laParser
from laVisitor import laVisitor
from laErrorHandler import laErrorHandler
from laSemantics import laSemantics
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
#tratamento de erros sintáticos (implementado em laErrorHandler)
parser._listeners = [laErrorHandler(saida)]
tree = parser.programa()

# Análise semântica
semantic = laSemantics()
semantic.visit(tree)

#abrir arquivo de saída semântica
saida_semantic = open(args.output, "w+")

#tratamento de erros semanticos (implementado em laSemantics)
if(semantic.errors):
	saida_semantic.write(semantic.errors)
	saida_semantic.write("Fim da compilacao\n")
	print(semantic.errors)
	exit()
else:
	for linha in semantic.codigo:
		saida.write(linha)
		print(linha)
	exit()