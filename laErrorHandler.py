
from antlr4.error.ErrorListener import ErrorListener
from antlr4 import *
import math


class laErrorHandler(ErrorListener):
	def __init__(self, output):
		self.output = output
	#tratamento dos erros sintaticos
	def syntaxError(self, recognizer, o, line, column, msg, e):
		#condição ou caracter que gerou o erro sintático
		value = o.text
		#mapeia o tipo de erro sintático ou lexico que aparece
		message = msg
		extraneousSymbols = '"@!|'
		if(message[0:20] == "mismatched input '{'"):
			#print("Linha " + str(line+1) + ": comentario nao fechado")
			self.output.write("Linha " + str(line+1) + ": comentario nao fechado\n")
		elif(message[0:10] == "extraneous" and value in extraneousSymbols):
			#print("Linha " + str(line) + ": " + value + " - simbolo nao identificado")
			self.output.write("Linha " + str(line) + ": " + value + " - simbolo nao identificado\n")
		else:
			#print("Linha " + str(line) + ": erro sintatico proximo a " + value)
			if(value == "<EOF>"):
				value = "EOF"
			self.output.write("Linha " + str(line) + ": erro sintatico proximo a " + value + "\n")

		self.output.write("Fim da compilacao\n")
		#print("Fim da compilacao")
		exit()	