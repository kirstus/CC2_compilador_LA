from antlr4 import *
from laListener import laListener
from laParser import laParser
from laVisitor import laVisitor
import re #Regular expressions

class laSemantics(laVisitor):
	# variável que vai armazenar todos os erros da etapa semântica
	errors = ""
	codigo = []
	tipos = {
  		"literal": "char",
  		"inteiro": "int",
  		"real": "float",
  		"logico": "bool",
  		"registro": "struct",
  		"tipo":	"typedef"
	}

	formatos = {
  		"literal": "%s",
  		"inteiro": "%d",
  		"real": "%f",
  		"logico": "%b"
	}

	tabelaSimbolosVariaveis = {}
	tabelaSimbolosFuncoes = {}
	# dicionário com simbolos já declarados
	tabelaSimbolosVariaveisFuncoes = {}
	tabelaSimbolosRetornoFuncoes = {}
	tabelaSimbolosProcedimentos = {}

	# Visit a parse tree produced by laParser#programa.
	# gramática = programa: declaracoes 'algoritmo' corpo 'fim_algoritmo';
	def visitPrograma(self, ctx:laParser.ProgramaContext):
		self.codigo.append("#include <stdio.h>\n")
		self.codigo.append("#include <stdlib.h>\n")
		self.codigo.append("\n")
		self.codigo.append("int main() {\n")
		self.visitDeclaracoes(ctx.declaracoes())
		self.visitCorpo(ctx.corpo())
		self.codigo.append("return 0;\n")
		self.codigo.append("}\n")


	# Visit a parse tree produced by laParser#declaracoes.
	# gramática = declaracoes: decl_local_global*;
	def visitDeclaracoes(self, ctx:laParser.DeclaracoesContext):
		for declLG in ctx.decl_local_global():
			self.visitDecl_local_global(declLG)


	# Visit a parse tree produced by laParser#decl_local_global.
	# gramática = decl_local_global: declaracao_local | declaracao_global;
	def visitDecl_local_global(self, ctx:laParser.Decl_local_globalContext):
		if(ctx.declaracao_local() != None):
			self.visitDeclaracao_local(ctx.declaracao_local())
		elif(ctx.declaracao_global() != None):
			self.visitDeclaracao_global(ctx.declaracao_global())

	''' Visit a parse tree produced by laParser#declaracao_local.
	declaracao_local: 'declare' variavel 
				| 'constante' IDENT ':' tipo_basico '=' valor_constante
				| 'tipo' IDENT ':' tipo;'''
	def visitDeclaracao_local(self, ctx:laParser.Declaracao_localContext, isFunction = None):
		if('declare' in ctx.getText()):
			self.visitVariavel(ctx.variavel(), isFunction)
		elif('constante' in ctx.getText()):
			if(isFunction != None): # Se for uma função
				# Se o identificador não tiver sido declarado ainda, adiciona ao dicionário de declarações dessa função
				if(ctx.IDENT().getText() not in self.tabelaSimbolosVariaveisFuncoes[isFunction].keys()):
					self.visitTipo_basico(ctx.tipo_basico())
					self.tabelaSimbolosVariaveisFuncoes.update({isFunction: {ctx.IDENT().getText() : ctx.tipo_basico().getText()}})
					self.visitValor_constante(ctx.valor_constante())
				else: #Se o identificador já tiver sido declarado, adiciona o erro à variável de erros
					self.errors += "Linha " + str(ctx.start.line) + ": identificador " + ctx.IDENT().getText() + " ja declarado anteriormente\n"
			else: # Se não for uma função
				# Se o identificador não tiver sido declarado ainda, adiciona ao dicionário de declarações
				if(ctx.IDENT().getText() not in self.tabelaSimbolosVariaveis.keys()):
					self.visitTipo_basico(ctx.tipo_basico())
					self.tabelaSimbolosVariaveis[ctx.IDENT().getText()] = ctx.tipo_basico().getText()
					self.visitValor_constante(ctx.valor_constante())
				else: #Se o identificador já tiver sido declarado, adiciona o erro à variável de erros
					self.errors += "Linha " + str(ctx.start.line) + ": identificador " + ctx.IDENT().getText() + " ja declarado anteriormente\n"
		elif('tipo' in ctx.getText()):
			if(isFunction != None):
				# Se o identificador não tiver sido declarado ainda, adiciona ao dicionário de declarações dessa função
				if(ctx.IDENT().getText() not in self.tabelaSimbolosVariaveisFuncoes[isFunction].keys()):
					self.tabelaSimbolosVariaveisFuncoes.update({isFunction: {ctx.IDENT().getText() : "tipo"}})
					self.visitTipo(ctx.tipo())
				else: #Se o identificador já tiver sido declarado, adiciona o erro à variável de erros
					self.errors += "Linha " + str(ctx.start.line) + ": identificador " + ctx.IDENT().getText() + " ja declarado anteriormente\n"
			else: # Se o identificador não tiver sido declarado ainda, adiciona ao dicionário de declarações
				if(ctx.IDENT().getText() not in self.tabelaSimbolosVariaveis.keys()):
					self.tabelaSimbolosVariaveis[ctx.IDENT().getText()] = "tipo"
					self.tipos[ctx.IDENT().getText()] = ctx.IDENT().getText()
					self.visitTipo(ctx.tipo())
				else: #Se o identificador já tiver sido declarado, adiciona o erro à variável de erros
					self.errors += "Linha " + str(ctx.start.line) + ": identificador " + ctx.IDENT().getText() + " ja declarado anteriormente\n"

	 # Visit a parse tree produced by laParser#variavel.
	 # variavel: primID=identificador (',' maisID+=identificador)* ':' tipo;
	def visitVariavel(self, ctx:laParser.VariavelContext, isFunction = None):
		v = ""
		for i in range(0, len(ctx.identificador())):
			identName = self.visitIdentificador(ctx.identificador(i))
			if(isFunction != None):
				# Se o identificador não tiver sido declarado ainda, adiciona ao dicionário de declarações dessa função
				if(identName not in self.tabelaSimbolosVariaveisFuncoes[isFunction].keys()):
					tabelaKeys = self.tabelaSimbolosVariaveisFuncoes[isFunction]
					tabelaKeys[identName] = ctx.tipo().getText()
					self.tabelaSimbolosVariaveisFuncoes[isFunction] = tabelaKeys
				else: #Se o identificador já tiver sido declarado, adiciona o erro à variável de erros
					self.errors += "Linha " + str(ctx.identificador(i).start.line) + ": identificador " + identName + " ja declarado anteriormente\n"
			else: # Se o identificador não tiver sido declarado ainda, adiciona ao dicionário de declarações
				if(identName not in self.tabelaSimbolosVariaveis.keys()):
					self.tabelaSimbolosVariaveis[identName] = ctx.tipo().getText()
					if(ctx.tipo().getText().find('registro')!=-1):
						v = self.tipos["registro"]+" "+identName+"{"
					else:
						v += "," + identName
						print(identName)
				else: #Se o identificador já tiver sido declarado, adiciona o erro à variável de erros
					self.errors += "Linha " + str(ctx.identificador(i).start.line) + ": identificador " + identName + " ja declarado anteriormente\n"
		if(v!=""):
			if(v[0]!=","):
				self.codigo.append(v+"\n")
			else:
				v.replace(",","",1)
				if(ctx.tipo().getText()=="literal"):
					self.codigo.append(self.tipos.get(ctx.tipo().getText().replace("^", ""),"")+" "+identName+"[100];\n")
				else:
					self.codigo.append(self.tipos.get(ctx.tipo().getText().replace("^", ""),"")+" "+identName+";\n")
		self.visitTipo(ctx.tipo())



	# Visit a parse tree produced by laParser#identificador.
	# gramática = identificador: primIDIdent=IDENT ('.' maisIDIdent+=IDENT)* dimensao;
	def visitIdentificador(self, ctx:laParser.IdentificadorContext):
		identString = str(ctx.IDENT(0))
		for i in range(1, len(ctx.IDENT())):
			identString = identString + '.' + str(ctx.IDENT(i))	
		self.visitDimensao(ctx.dimensao())
		return identString


	# Visit a parse tree produced by laParser#dimensao.
	# gramática = dimensao: ('[' exp_aritmetica ']')*;
	def visitDimensao(self, ctx:laParser.DimensaoContext):
		for expArit in ctx.exp_aritmetica():
			self.visitExp_aritmetica(expArit)


	# Visit a parse tree produced by laParser#tipo.
	# gramática = tipo: registro | tipo_estendido;
	def visitTipo(self, ctx:laParser.TipoContext):
		if (ctx.registro() != None):
			self.visitRegistro(ctx.registro())
		else:
			self.visitTipo_estendido(ctx.tipo_estendido())


	# Visit a parse tree produced by laParser#tipo_basico.
	# gramática = tipo_basico: 'literal' | 'inteiro' | 'real' | 'logico';
	def visitTipo_basico(self, ctx:laParser.Tipo_basicoContext):
		ctxText = ctx.getText()
		# os tipos podem ser literal, inteiro, real ou lógico
		if('literal' in ctxText or 'inteiro' in ctxText or 'real' in ctxText or 'logico' in ctxText):
			return ctx.getText()
		else: # se não for nenhum desses, adiciona o erro a variavel de erros
			self.errors += "Linha " + str(ctx.start.line) + ": tipo " + ctx.IDENT().getText() + " nao declarado\n"


	# Visit a parse tree produced by laParser#tipo_basico_ident.
	# gramática = tipo_basico_ident: tipo_basico | IDENT;
	def visitTipo_basico_ident(self, ctx:laParser.Tipo_basico_identContext):
		if(ctx.tipo_basico() != None):
			return ctx.tipo_basico().getText()
		else:
			if(ctx.IDENT().getText() not in self.tabelaSimbolosVariaveis.keys()):
				self.errors += "Linha " + str(ctx.start.line) + ": tipo " + ctx.IDENT().getText() + " nao declarado\n"
			return ctx.IDENT().getText()


	# Visit a parse tree produced by laParser#tipo_estendido.
	# gramática = tipo_estendido: ('^')? tipo_basico_ident;
	def visitTipo_estendido(self, ctx:laParser.Tipo_estendidoContext):
		# Remove o ^ da entrada e passa como parâmetro para o visitor de tipo basico
		return self.visitTipo_basico_ident(ctx.tipo_basico_ident()).replace('^', '')


	# Visit a parse tree produced by laParser#valor_constante.
	# gramática = valor_constante: CADEIA | NUM_INT | NUM_REAL | 'verdadeiro' | 'falso';
	def visitValor_constante(self, ctx:laParser.Valor_constanteContext):
		return ctx.getText()


	# Visit a parse tree produced by laParser#registro.
	# gramática = registro: 'registro' (variavel)* 'fim_registro';
	def visitRegistro(self, ctx:laParser.RegistroContext):
		for var in ctx.variavel():
			# Valida cada uma das variáveis do registro
			self.visitVariavel(var)
		self.codigo.append("};\n")


	''' Visit a parse tree produced by laParser#declaracao_global.
	declaracao_global: 'procedimento' IDENT '(' (parametros)? ')' (declaracao_local)* (cmd)* 'fim_procedimento'
				 | 'funcao' IDENT '(' (parametros)? ')' ':' tipo_estendido (declaracao_local)* (cmd)* 'fim_funcao';
	'''
	def visitDeclaracao_global(self, ctx:laParser.Declaracao_globalContext):
		if('procedimento' in ctx.getText()):
			# Verifica se o escopo é um procedimento e trata das declarações considerando isso
			functionParameters = ''
			if(ctx.parametros() != None):
				self.visitParametros(ctx.parametros(), ctx.IDENT().getText())
			if(ctx.IDENT().getText() not in self.tabelaSimbolosFuncoes.keys()):
				# Adiciona a declaraçao ao dicionário de declarações de procedimentos
				self.tabelaSimbolosProcedimentos[ctx.IDENT().getText()] = 'procedimento'
				self.tabelaSimbolosVariaveis[ctx.IDENT().getText()] = 'procedimento'
				self.tabelaSimbolosFuncoes[ctx.IDENT().getText()] = functionParameters
			for declL in ctx.declaracao_local():
				self.visitDeclaracao_local(declL, ctx.IDENT().getText())
			for command in ctx.cmd():
				self.visitCmd(command, ctx.IDENT().getText())
		else: # Se não é um procedimento, considera como função e trata das declarações considerando isso
			functionParameters = ''
			if(ctx.parametros() != None):
				functionParameters = self.visitParametros(ctx.parametros(), ctx.IDENT().getText())
			if(ctx.IDENT().getText() not in self.tabelaSimbolosFuncoes.keys()):
				# Adiciona a declaraçao ao dicionário de declarações de funções
				self.tabelaSimbolosFuncoes[ctx.IDENT().getText()] = functionParameters
				self.tabelaSimbolosVariaveis[ctx.IDENT().getText()] = 'funcao'
			self.visitTipo_estendido(ctx.tipo_estendido())
			self.tabelaSimbolosRetornoFuncoes[ctx.IDENT().getText()] = ctx.tipo_estendido().getText()
			for declL in ctx.declaracao_local():
				self.visitDeclaracao_local(declL, ctx.IDENT().getText())
			for command in ctx.cmd():
				self.visitCmd(command, ctx.IDENT().getText())

	
	# Visit a parse tree produced by laParser#parametro.
	# gramática = parametro: ('var')? primID=identificador (',' maisID+=identificador)* ':' tipo_estendido;
	def visitParametro(self, ctx:laParser.ParametroContext, isFunction = None):
		for identifier in ctx.identificador():
			self.visitIdentificador(identifier)
			if (isFunction != None):
				if(isFunction not in self.tabelaSimbolosVariaveisFuncoes.keys()):
					self.tabelaSimbolosVariaveisFuncoes.update({isFunction: {identifier.getText() : ctx.tipo_estendido().getText()}})
				else:
					tabelaSimFuncs = self.tabelaSimbolosVariaveisFuncoes[isFunction]
					tabelaSimFuncs[identifier.getText()] = ctx.tipo_estendido().getText()
					self.tabelaSimbolosVariaveisFuncoes[isFunction] = tabelaSimFuncs
		return self.visitTipo_estendido(ctx.tipo_estendido())


	# Visit a parse tree produced by laParser#parametros.
	# gramática =  parametros: param=parametro (',' maisParam+=parametro)*;
	def visitParametros(self, ctx:laParser.ParametrosContext, isFunction = None):
		parametersArray = []
		for parameter in ctx.parametro():
			parametersArray.append(self.visitParametro(parameter, isFunction))
		return parametersArray


	# Visit a parse tree produced by laParser#corpo.
	# gramática = corpo: (declaracao_local)* (cmd)*;
	def visitCorpo(self, ctx:laParser.CorpoContext):
		for declL in ctx.declaracao_local():
			self.visitDeclaracao_local(declL)
		for command in ctx.cmd():
			self.visitCmd(command)


	# Visit a parse tree produced by laParser#cmd.
	# gramática = cmd: cmdLeia | cmdEscreva | cmdSe | cmdCaso | cmdPara | cmdEnquanto | cmdFaca | cmdAtribuicao | cmdChamada | cmdRetorne;
	def visitCmd(self, ctx:laParser.CmdContext, isFunction = None):
		if(ctx.cmdLeia() != None):
			self.visitCmdLeia(ctx.cmdLeia(), isFunction)
		if(ctx.cmdEscreva() != None):
			self.visitCmdEscreva(ctx.cmdEscreva(), isFunction)
		if(ctx.cmdSe() != None):
			self.visitCmdSe(ctx.cmdSe(), isFunction)
		if(ctx.cmdCaso() != None):
			self.visitCmdCaso(ctx.cmdCaso())
		if(ctx.cmdPara() != None):
			self.visitCmdPara(ctx.cmdPara())
		if(ctx.cmdEnquanto() != None):
			self.visitCmdEnquanto(ctx.cmdEnquanto())
		if(ctx.cmdFaca() != None):
			self.visitCmdFaca(ctx.cmdFaca(), isFunction)
		if(ctx.cmdAtribuicao() != None):
			self.visitCmdAtribuicao(ctx.cmdAtribuicao(), isFunction)
		if(ctx.cmdChamada() != None):
			self.visitCmdChamada(ctx.cmdChamada())
		if(ctx.cmdRetorne() != None):
			self.visitCmdRetorne(ctx.cmdRetorne(), isFunction)


	# Visit a parse tree produced by laParser#cmdLeia.
	# gramática = cmdLeia: 'leia' '(' ('^')? primID=identificador (',' ('^')? maisID+=identificador)* ')';
	def visitCmdLeia(self, ctx:laParser.CmdLeiaContext, isFunction = None):
		stringFormatos = ""
		argumentos = ""
		for identifier in ctx.identificador():
			identificadores = identifier.getText().split('.')
			regex = re.compile(r'\[.*\]')
			args = ", "
			for element in identificadores:
				if(isFunction != None):
					identFunction = regex.sub('',element)
					if(identFunction not in self.tabelaSimbolosVariaveisFuncoes[isFunction].keys() and identFunction not in self.tabelaSimbolosVariaveis.keys()):
						self.errors += "Linha " + str(ctx.start.line) + ": identificador " + identifier.getText() + " nao declarado\n"
					else:						
						#stringFormatos += self.formatos.get(self.tabelaSimbolosVariaveisFuncoes[element.split("[")[0]],"") #erro aqui
						args += "." + element
				else:
					if(regex.sub('',element) not in self.tabelaSimbolosVariaveis.keys()):
						self.errors += "Linha " + str(ctx.start.line) + ": identificador " + identifier.getText() + " nao declarado\n"	
					else:
						stringFormatos += self.formatos.get(self.tabelaSimbolosVariaveis[element.split("[")[0]],"")
						args += "." + element
			self.visitIdentificador(identifier)
			args = args.replace(".", "&", 1)
			argumentos += args
		if(stringFormatos=="%s"):
			argumentos = argumentos.replace(", ", "", 1)
			self.codigo.append("gets("+argumentos+");\n")
		else:
			self.codigo.append("scanf(\""+stringFormatos+"\""+argumentos+");\n")
		print("scanf("+stringFormatos+argumentos+");")


	# Visit a parse tree produced by laParser#cmdEscreva.
	# gramática = cmdEscreva: 'escreva' '(' expr=expressao (',' naisExpr+=expressao)* ')';
	def visitCmdEscreva(self, ctx:laParser.CmdEscrevaContext, isFunction = None):
		stringFormatos = ""
		argumentos = ""
		for expression in ctx.expressao():
			self.visitExpressao(expression, isFunction)
			if(expression.getText()[0]=="\""):
				stringFormatos += "%s"
			else:
				identificadores = expression.getText().split('.')
				regex = re.compile(r'\[.*\]')
				for element in identificadores:
					if(isFunction != None):
						identFunction = regex.sub('',element)
						if(identFunction in self.tabelaSimbolosVariaveisFuncoes[isFunction].keys() or identFunction in self.tabelaSimbolosVariaveis.keys()):					
							a=0#stringFormatos += self.formatos.get(self.tabelaSimbolosVariaveis[element],"")
					else:
						if(regex.sub('',element) in self.tabelaSimbolosVariaveis.keys()):
							stringFormatos += self.formatos.get(self.tabelaSimbolosVariaveis[element],"")
			argumentos += ", " + expression.getText()
		self.codigo.append("printf(\""+stringFormatos+"\""+argumentos+");\n")


	# Visit a parse tree produced by laParser#cmdSe.
	# gramática =  cmdSe: 'se' expressao 'entao' (comandos+=cmd)* ('senao' (maisComandos+=cmd)*)? 'fim_se';
	def visitCmdSe(self, ctx:laParser.CmdSeContext, isFunction = None):
		
		self.visitExpressao(ctx.expressao(), isFunction)
		for command in ctx.cmd():
			self.visitCmd(command, isFunction)


	# Visit a parse tree produced by laParser#cmdCaso.
	# gramática = cmdCaso: 'caso' exp_aritmetica 'seja' selecao ('senao' (cmd)*)? 'fim_caso';
	def visitCmdCaso(self, ctx:laParser.CmdCasoContext):
		self.visitExp_aritmetica(ctx.exp_aritmetica())
		self.visitSelecao(ctx.selecao())
		for command in ctx.cmd():
			self.visitCmd(command)


	# Visit a parse tree produced by laParser#cmdPara.
	# gramática = cmdPara: 'para' IDENT '<-' exp_aritmetica 'ate' exp_aritmetica 'faca' (cmd)* 'fim_para';
	def visitCmdPara(self, ctx:laParser.CmdParaContext):
		self.visitExp_aritmetica(ctx.exp_aritmetica(0))
		self.visitExp_aritmetica(ctx.exp_aritmetica(1))
		for command in ctx.cmd():
			self.visitCmd(command)

	# Visit a parse tree produced by laParser#cmdEnquanto.
	# gramática = cmdEnquanto: 'enquanto' expressao 'faca' (cmd)* 'fim_enquanto';
	def visitCmdEnquanto(self, ctx:laParser.CmdEnquantoContext):
		self.visitExpressao(ctx.expressao())
		for command in ctx.cmd():
			self.visitCmd(command)


	# Visit a parse tree produced by laParser#cmdFaca.
	# gramática = cmdFaca: 'faca' (cmd)* 'ate' expressao;
	def visitCmdFaca(self, ctx:laParser.CmdFacaContext, isFunction = None):
		for command in ctx.cmd():
			self.visitCmd(command, isFunction)
		self.visitExpressao(ctx.expressao(), isFunction)


	# Visit a parse tree produced by laParser#cmdAtribuicao.
	# gramática = cmdAtribuicao: ('^')? identificador '<-' expressao;
	def visitCmdAtribuicao(self, ctx:laParser.CmdAtribuicaoContext, isFunction):
		self.visitIdentificador(ctx.identificador())
		regex = re.compile(r'\[.*\]')
		identifier = regex.sub('',ctx.identificador().getText().split('.')[-1])
		exprValue = self.visitExpressao(ctx.expressao(), isFunction)
		if(isFunction != None):
			identSplitted = identifier.split('.')
			isValidIdentifier = True
			for element in identSplitted:
				if(element not in self.tabelaSimbolosVariaveisFuncoes[isFunction].keys() and element not in self.tabelaSimbolosVariaveis.keys()):
					self.errors += "Linha " + str(ctx.start.line) + ": identificador " + element + ' nao declarado\n'
					isValidIdentifier = False
			if(isValidIdentifier):
				if(identifier in self.tabelaSimbolosVariaveisFuncoes[isFunction].keys()):
					tabelaValue = self.tabelaSimbolosVariaveisFuncoes[isFunction][identifier].replace('^', '')
				else:
					tabelaValue = self.tabelaSimbolosVariaveis[identifier].replace('^', '')
				if(exprValue == 'errorType' or (exprValue != tabelaValue)):
					if('^' in self.tabelaSimbolosVariaveisFuncoes[isFunction][identifier]):
						if(tabelaValue == 'real'):
							if(exprValue != 'inteiro' and exprValue != 'real'):
								self.errors += "Linha " + str(ctx.start.line) + ": atribuicao nao compativel para ^" + ctx.identificador().getText() + '\n'
						else:
							self.errors += "Linha " + str(ctx.start.line) + ": atribuicao nao compativel para ^" + ctx.identificador().getText() + '\n'
					else:
						if(tabelaValue == 'real'):
							if(exprValue != 'inteiro' and exprValue != 'real'):
								self.errors += "Linha " + str(ctx.start.line) + ": atribuicao nao compativel para " + ctx.identificador().getText() + '\n'
						else:
							self.errors += "Linha " + str(ctx.start.line) + ": atribuicao nao compativel para " + ctx.identificador().getText() + '\n'
		else:
			identSplitted = identifier.split('.')
			isValidIdentifier = True
			for element in identSplitted:
				if(element not in self.tabelaSimbolosVariaveis.keys()):
					self.errors += "Linha " + str(ctx.start.line) + ": identificador " + element + ' nao declarado\n'
					isValidIdentifier = False
			if(isValidIdentifier):
				tabelaValue = self.tabelaSimbolosVariaveis[identifier].replace('^', '')
				if(exprValue == 'errorType' or (exprValue != tabelaValue)):
					if('^' in self.tabelaSimbolosVariaveis[identifier]):
						if(tabelaValue == 'real'):
							if(exprValue != 'inteiro' and exprValue != 'real'):
								self.errors += "Linha " + str(ctx.start.line) + ": atribuicao nao compativel para ^" + ctx.identificador().getText() + '\n'
						else:
							self.errors += "Linha " + str(ctx.start.line) + ": atribuicao nao compativel para ^" + ctx.identificador().getText() + '\n'
					else:
						if(tabelaValue == 'real'):
							if(exprValue != 'inteiro' and exprValue != 'real'):
								self.errors += "Linha " + str(ctx.start.line) + ": atribuicao nao compativel para " + ctx.identificador().getText() + '\n'
						else:
							self.errors += "Linha " + str(ctx.start.line) + ": atribuicao nao compativel para " + ctx.identificador().getText() + '\n'

	# Visit a parse tree produced by laParser#cmdChamada.
	# gramática = cmdChamada: IDENT '(' expr=expressao (',' maisExpr+=expressao)* ')';
	def visitCmdChamada(self, ctx:laParser.CmdChamadaContext):
		for expression in ctx.expressao():
			self.visitExpressao(expression)


	# Visit a parse tree produced by laParser#cmdRetorne.
	# gramática = cmdRetorne: 'retorne' expressao;
	def visitCmdRetorne(self, ctx:laParser.CmdRetorneContext, isFunction = None):
		if(isFunction == None or isFunction in self.tabelaSimbolosProcedimentos):
			self.errors += "Linha " + str(ctx.start.line) + ": comando retorne nao permitido nesse escopo\n"
		self.visitExpressao(ctx.expressao(), isFunction)


	# Visit a parse tree produced by laParser#selecao.
	# gramática = selecao: (item_selecao)+;
	def visitSelecao(self, ctx:laParser.SelecaoContext):
		for selection in ctx.item_selecao():
			self.visitItem_selecao(selection)


	# Visit a parse tree produced by laParser#item_selecao.
	# gramática = item_selecao: constantes ':' (cmd)*;
	def visitItem_selecao(self, ctx:laParser.Item_selecaoContext):
		self.visitConstantes(ctx.constantes())
		for command in ctx.cmd():
			self.visitCmd(command)


	# Visit a parse tree produced by laParser#constantes.
	# gramática = constantes: ni=numero_intervalo (',' maisNI+=numero_intervalo)*;
	def visitConstantes(self, ctx:laParser.ConstantesContext):
		for numInterval in ctx.numero_intervalo():
			self.visitNumero_intervalo(numInterval)


	# Visit a parse tree produced by laParser#numero_intervalo.
	# gramática = numero_intervalo: (op_unario)? primNum=NUM_INT ('..'(op_unario)? segNum=NUM_INT)?;
	def visitNumero_intervalo(self, ctx:laParser.Numero_intervaloContext):
		for opUN in ctx.op_unario():
			self.visitOp_unario(opUN)


	# Visit a parse tree produced by laParser#op_unario.
	# gramática = op_unario: '-';
	def visitOp_unario(self, ctx:laParser.Op_unarioContext):
		if (type(ctx) != None):
			return ctx.getText()


	# Visit a parse tree produced by laParser#exp_aritmetica.
	# gramática = exp_aritmetica: primTermo=termo (op1 maisTermos+=termo)*;
	def visitExp_aritmetica(self, ctx:laParser.Exp_aritmeticaContext, isFunction = None):
		primTermoText = self.visitTermo(ctx.termo(0), isFunction)
		for i in range(0, len(ctx.op1())):
			self.visitOp1(ctx.op1(i))
			outroTermoText = self.visitTermo(ctx.termo(i+1), isFunction)
			if(primTermoText != outroTermoText):
				return 'errorType'
		return primTermoText


	# Visit a parse tree produced by laParser#termo.
	# gramática = termo: primFator=fator (op2 maisFatores+=fator)*;
	def visitTermo(self, ctx:laParser.TermoContext, isFunction = None):
		fatorText = ''
		fatorText = self.visitFator(ctx.fator(0), isFunction)
		for i in range(0, len(ctx.op2())):
			self.visitOp2(ctx.op2(i))
			fatorText2 = self.visitFator(ctx.fator(i+1), isFunction)
			if(fatorText2 != fatorText):
				if((fatorText == 'real' or fatorText == 'inteiro') and (fatorText2 == 'real' or fatorText2 == 'inteiro')):
					if(fatorText == 'real' or fatorText2 == 'real'):
						return 'real'
					else:
						return 'inteiro'
				fatorText = "errorType"
		return fatorText


	# Visit a parse tree produced by laParser#fator.
	# gramática = fator: primParcela=parcela (op3 maisParcelas+=parcela)*;
	def visitFator(self, ctx:laParser.FatorContext, isFunction = None):
		parcelasText = ''
		parcelaType = self.visitParcela(ctx.parcela(0), isFunction)
		if(parcelaType != None):
			parcelasText += parcelaType
		for i in range(0, len(ctx.op3())):
			self.visitOp3(ctx.op3(i))
			parcelasType2 = self.visitParcela(ctx.parcela(i+1), isFunction)
			if(parcelasType2 != parcelasText):
				if((parcelasText == 'real' or parcelasText == 'inteiro') and (parcelasText2 == 'real' or parcelasText2 == 'inteiro')):
					if(parcelasText == 'real' or parcelasText2 == 'real'):
						return 'real'
					else:
						return 'inteiro'
				parcelasText = "errorType"
		return parcelasText


	# Visit a parse tree produced by laParser#op1.
	# gramática = op1: '+' | '-';
	def visitOp1(self, ctx:laParser.Op1Context):
		return ctx.getText()


	# Visit a parse tree produced by laParser#op2.
	# gramática = op2: '*' | '/';
	def visitOp2(self, ctx:laParser.Op2Context):
		return ctx.getText()


	# Visit a parse tree produced by laParser#op3.
	# gramática = op3: '%';
	def visitOp3(self, ctx:laParser.Op3Context):
		return ctx.getText()


	# Visit a parse tree produced by laParser#parcela.
	# gramática = parcela: (op_unario)? parcela_unario | parcela_nao_unario;
	def visitParcela(self, ctx:laParser.ParcelaContext, isFunction = None):
		if(ctx.parcela_unario() != None):
			if(ctx.op_unario() != None):
				self.visitOp_unario(ctx.op_unario())
			return self.visitParcela_unario(ctx.parcela_unario(), isFunction)
		else:
			return self.visitParcela_nao_unario(ctx.parcela_nao_unario())


	''' Visit a parse tree produced by laParser#parcela_unario.
	parcela_unario: ('^')? identificador
			  | IDENT '(' expr=expressao (',' maisExpr+=expressao)* ')'
			  | NUM_INT
			  | NUM_REAL
			  | '(' outraExpr=expressao ')';
	'''
	def visitParcela_unario(self, ctx:laParser.Parcela_unarioContext, isFunction = None):
		if(ctx.identificador() != None):
			identNameBefore = self.visitIdentificador(ctx.identificador())
			identName = identNameBefore.split('.')
			isErrorType = False
			for element in identName:
				if(isFunction != None):
					if(element not in self.tabelaSimbolosVariaveisFuncoes[isFunction].keys() and element not in self.tabelaSimbolosVariaveis.keys()):
						self.errors += "Linha " + str(ctx.identificador().start.line) + ": identificador " + identNameBefore + " nao declarado\n"
						isErrorType = True
				else:
					if(element not in self.tabelaSimbolosVariaveis.keys()):
						self.errors += "Linha " + str(ctx.identificador().start.line) + ": identificador " + identNameBefore + " nao declarado\n"
						isErrorType = True
			if (isErrorType == True):
				return 'errorType'
			else:
				if(isFunction != None):
					if(identName[-1] in self.tabelaSimbolosVariaveisFuncoes[isFunction].keys()):
						return self.tabelaSimbolosVariaveisFuncoes[isFunction][identName[-1]]
					else:
						return self.tabelaSimbolosVariaveis[identName[-1]]
				else:
					return self.tabelaSimbolosVariaveis[identName[-1]]
		elif(ctx.expr != None):
			exprTypeArray = []
			funcTypeArray = self.tabelaSimbolosFuncoes[ctx.IDENT().getText()]
			for expression in ctx.expressao():
				exprTypeArray.append(self.visitExpressao(expression))
			if(exprTypeArray != funcTypeArray):
				self.errors += "Linha " + str(ctx.start.line) + ": incompatibilidade de parametros na chamada de " + ctx.IDENT().getText() + "\n"
			return self.tabelaSimbolosRetornoFuncoes[ctx.IDENT().getText()]
		elif(ctx.outraExpr != None):
			return self.visitExpressao(ctx.expressao(0))
		else:
			if('.' in ctx.getText()):
				return 'real'
			return 'inteiro'


	# Visit a parse tree produced by laParser#parcela_nao_unario.
	# gramática = parcela_nao_unario: '&' identificador | CADEIA;
	def visitParcela_nao_unario(self, ctx:laParser.Parcela_nao_unarioContext):
		if(ctx.identificador() != None):
			self.visitIdentificador(ctx.identificador())
			return self.tabelaSimbolosVariaveis[ctx.identificador().getText()]
		else:
			return 'literal'


	# Visit a parse tree produced by laParser#exp_relacional.
	# gramática = exp_relacional: exp_aritmetica (op_relacional exp_aritmetica)?;
	def visitExp_relacional(self, ctx:laParser.Exp_relacionalContext, isFunction = None):
		expArit1 = self.visitExp_aritmetica(ctx.exp_aritmetica(0), isFunction)
		if(ctx.op_relacional() != None):
			self.visitOp_relacional(ctx.op_relacional())
			expArit2 = self.visitExp_aritmetica(ctx.exp_aritmetica(1), isFunction)
			if(expArit1 != expArit2):
				return 'errorType'
			else:
				return 'logico'
		return expArit1


	# Visit a parse tree produced by laParser#op_relacional.
	# gramática = op_relacional: '=' | '<>' | '>=' | '<=' | '>' | '<';
	def visitOp_relacional(self, ctx:laParser.Op_relacionalContext):
		return ctx.getText()


	# Visit a parse tree produced by laParser#expressao.
	# gramática = expressao: termoLog=termo_logico (op_logico_1 maisTermoLog+=termo_logico)*;
	def visitExpressao(self, ctx:laParser.ExpressaoContext, isFunction = None):
		primTermLog = self.visitTermo_logico(ctx.termo_logico(0), isFunction)
		for i in range(0,len(ctx.op_logico_1())):
			self.visitOp_logico_1(ctx.op_logico_1(i))
			outroTermLog = self.visitTermo_logico(ctx.termo_logico(i+1), isFunction)
			if( primTermLog != outroTermLog ):
				return "errorType"
		return primTermLog


	# Visit a parse tree produced by laParser#termo_logico.
	# gramática = termo_logico: fatLog=fator_logico (op_logico_2 maisFatLog+=fator_logico)*;
	def visitTermo_logico(self, ctx:laParser.Termo_logicoContext, isFunction = None):
		primFatLog = self.visitFator_logico(ctx.fator_logico(0), isFunction)
		for i in range(0,len(ctx.op_logico_2())):
			self.visitOp_logico_2(ctx.op_logico_2(i))
			outroFatLog = self.visitFator_logico(ctx.fator_logico(i+1), isFunction)
			if( primFatLog != outroFatLog ):
				return "errorType"
		return primFatLog


	# Visit a parse tree produced by laParser#fator_logico.
	# gramática = fator_logico: ('nao')? parcela_logica;
	def visitFator_logico(self, ctx:laParser.Fator_logicoContext, isFunction = None):
		parLog = self.visitParcela_logica(ctx.parcela_logica(), isFunction)
		if(parLog != None):
			return parLog


	# Visit a parse tree produced by laParser#parcela_logica.
	# parcela_logica: ('verdadeiro' | 'falso') | exp_relacional;
	def visitParcela_logica(self, ctx:laParser.Parcela_logicaContext, isFunction = None):
		if(ctx.exp_relacional() != None):
			return self.visitExp_relacional(ctx.exp_relacional(), isFunction)
		else:
			if(ctx.getText() == 'verdadeiro' or ctx.getText() == 'falso'):
				return 'logico'
			return 'errorType'


	# Visit a parse tree produced by laParser#op_logico_1.
	# gramática = op_logico_1: 'ou';
	def visitOp_logico_1(self, ctx:laParser.Op_logico_1Context):
		return ctx.getText()


	# Visit a parse tree produced by laParser#op_logico_2.
	# gramática = op_logico_2: 'e';
	def visitOp_logico_2(self, ctx:laParser.Op_logico_2Context):
		return ctx.getText()
