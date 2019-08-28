from antlr4.error.ErrorListener import ErrorListener
from antlr4 import *
import math


class laErrorHandler(ErrorListener):
	def __init__(self,output):
		self.output = output
	def syntaxError(self, recognizer, o, line, column, msg, e):
		value = o.text
		message = msg
		symbols = []

		'''print(o)
		print(line)
		print(msg)
		print(value)'''
		#self.output.write("erorhandler\n")

		if(message[0:10] == "mismatched"):
			self.output.write("Linha " + str(line+1) + ": comentario nao fechado\n")
			#print("Linha " + str(line+1) + ": comentario nao fechado")
		elif(message[0:9] == "no viable"):
			self.output.write("Linha " + str(line) + ": " + value + " - simbolo nao identificado\n")
			#print("Linha " + str(line) + ": " + value + " - simbolo nao identificado")
		else:
			self.output.write("Linha " + str(line) + ": erro sintatico proximo a " + value + "\n")
			#print("Linha " + str(line) + ": erro sintatico proximo a " + value)
		self.output.write("Fim da compilacao\n")
		#print("Fim da compilacao")
		exit()
		'''print("Line " + str(line) + ": ", end="")
		if(value == "<EOF>" and message[0:10] == "mismatched"):
			print("Job parameter has to be either 'class' or 'regression'\n")
		elif(value == "[" and message[0:10] == "mismatched"):
			print("features/classes range or training data size missing\n")
		elif(message[0:10] == "extraneous"):
			print("Erroneous value '" + value + "' found")
		elif(message[-5:] == "IDENT" and message[0:10] == "mismatched" and value.isdigit()):
			print("Dataset name is missing")
		elif(message[0:7] == "missing"):
			split = message.split("'")[1]
			print("Expected '" + split + "' next to '" + value + "'\n")
		elif(message[-3:] == "NUM" and message[0:10] == "mismatched"):
			print("Number is expected instead of '" + value + "'\n")
		elif(message[-5:] == "IDENT" and message[0:10] == "mismatched"):
			print("Name expected next to '" + value + "'\n")
		else:
			print("Syntax Error\n")
		exit()'''