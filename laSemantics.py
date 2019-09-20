from antlr4 import *
from laListener import laListener
from laParser import laParser
from laVisitor import laVisitor

class laSemantics(laVisitor):
	errors = ""
	tabelaSimbolosVariaveis = {}
	tabelaSimbolosFuncoes = {}
	tabelaSimbolosVariaveisFuncoes = {}

	# Visit a parse tree produced by laParser#programa.
	def visitPrograma(self, ctx:laParser.ProgramaContext):
		self.visitDeclaracoes(ctx.declaracoes())
		self.visitCorpo(ctx.corpo())


	# Visit a parse tree produced by laParser#declaracoes.
	def visitDeclaracoes(self, ctx:laParser.DeclaracoesContext):
		for declLG in ctx.decl_local_global():
			self.visitDecl_local_global(declLG)


	# Visit a parse tree produced by laParser#decl_local_global.
	def visitDecl_local_global(self, ctx:laParser.Decl_local_globalContext):
		if(ctx.declaracao_local() != None):
			self.visitDeclaracao_local(ctx.declaracao_local())
		elif(ctx.declaracao_global() != None):
			self.visitDeclaracao_global(ctx.declaracao_global())

	# Visit a parse tree produced by laParser#declaracao_local.
	def visitDeclaracao_local(self, ctx:laParser.Declaracao_localContext, isFunction = None):
		if('declare' in ctx.getText()):
			self.visitVariavel(ctx.variavel())
		elif('constante' in ctx.getText()):
			if(ctx.IDENT().getText() not in self.tabelaSimbolosVariaveis.keys()):
				self.visitTipo_basico(ctx.tipo_basico())
				self.tabelaSimbolosVariaveis[ctx.IDENT().getText()] = ctx.tipo_basico().getText()
				self.visitValor_constante(ctx.valor_constante())
			else:
				self.errors += "Linha " + str(ctx.start.line) + ": identificador " + ctx.IDENT().getText() + " ja declarado anteriormente\n"
		elif('tipo' in ctx.getText()):
			if(ctx.IDENT().getText() not in self.tabelaSimbolosVariaveis.keys()):
				self.tabelaSimbolosVariaveis[ctx.IDENT().getText()] = "tipo"
				self.visitTipo(ctx.tipo())
			else:
				self.errors += "Linha " + str(ctx.start.line) + ": identificador " + ctx.IDENT().getText() + " ja declarado anteriormente\n"

	 # Visit a parse tree produced by laParser#variavel.
	def visitVariavel(self, ctx:laParser.VariavelContext):
		for i in range(0, len(ctx.identificador())):
			identName = self.visitIdentificador(ctx.identificador(i))
			if(identName not in self.tabelaSimbolosVariaveis.keys()):
				self.tabelaSimbolosVariaveis[identName] = ctx.tipo().getText()
			else:
				self.errors += "Linha " + str(ctx.identificador(i).start.line) + ": identificador " + identName + " ja declarado anteriormente\n"
		self.visitTipo(ctx.tipo())



	# Visit a parse tree produced by laParser#identificador.
	def visitIdentificador(self, ctx:laParser.IdentificadorContext):
		identString = str(ctx.IDENT(0))
		for i in range(1, len(ctx.IDENT())):
			identString = identString + '.' + str(ctx.IDENT(i))	
		self.visitDimensao(ctx.dimensao())
		return identString


	# Visit a parse tree produced by laParser#dimensao.
	def visitDimensao(self, ctx:laParser.DimensaoContext):
		for expArit in ctx.exp_aritmetica():
			self.visitExp_aritmetica(expArit)


	# Visit a parse tree produced by laParser#tipo.
	def visitTipo(self, ctx:laParser.TipoContext):
		if (ctx.registro() != None):
			self.visitRegistro(ctx.registro())
		else:
			self.visitTipo_estendido(ctx.tipo_estendido())


	# Visit a parse tree produced by laParser#tipo_basico.
	def visitTipo_basico(self, ctx:laParser.Tipo_basicoContext):
		ctxText = ctx.getText()
		if('literal' in ctxText or 'inteiro' in ctxText or 'real' in ctxText or 'logico' in ctxText):
			return ctx.getText()
		else:
			self.errors += "Linha " + str(ctx.start.line) + ": tipo " + ctx.IDENT().getText() + " nao declarado\n"


	# Visit a parse tree produced by laParser#tipo_basico_ident.
	def visitTipo_basico_ident(self, ctx:laParser.Tipo_basico_identContext):
		if(ctx.tipo_basico() != None):
			return ctx.tipo_basico().getText()
		else:
			if(ctx.IDENT().getText() not in self.tabelaSimbolosVariaveis.keys()):
				self.errors += "Linha " + str(ctx.start.line) + ": tipo " + ctx.IDENT().getText() + " nao declarado\n"
			return ctx.IDENT().getText()


	# Visit a parse tree produced by laParser#tipo_estendido.
	def visitTipo_estendido(self, ctx:laParser.Tipo_estendidoContext):
		return self.visitTipo_basico_ident(ctx.tipo_basico_ident()).replace('^', '')


	# Visit a parse tree produced by laParser#valor_constante.
	def visitValor_constante(self, ctx:laParser.Valor_constanteContext):
		return ctx.getText()


	# Visit a parse tree produced by laParser#registro.
	def visitRegistro(self, ctx:laParser.RegistroContext):
		for var in ctx.variavel():
			self.visitVariavel(var)


	# Visit a parse tree produced by laParser#declaracao_global.
	def visitDeclaracao_global(self, ctx:laParser.Declaracao_globalContext):
		if('procedimento' in ctx.getText()):
			if(ctx.IDENT().getText() not in self.tabelaSimbolosFuncoes.keys()):
				self.tabelaSimbolosFuncoes[ctx.IDENT().getText()] = 'procedimento'
			if(ctx.parametros() != None):
				self.visitParametros(ctx.parametros())
			for declL in ctx.declaracao_local():
				self.visitDeclaracao_local(declL)
			for command in ctx.cmd():
				self.visitCmd(command)
		else:
			functionParameters = ''
			if(ctx.parametros() != None):
				functionParameters = self.visitParametros(ctx.parametros())
			if(ctx.IDENT().getText() not in self.tabelaSimbolosFuncoes.keys()):
				print(functionParameters)
				self.tabelaSimbolosFuncoes[ctx.IDENT().getText()] = 'functionParameters'
			self.visitTipo_estendido(ctx.tipo_estendido())
			for declL in ctx.declaracao_local():
				self.visitDeclaracao_local(declL)
			for command in ctx.cmd():
				self.visitCmd(command)

	# Visit a parse tree produced by laParser#parametro.
	def visitParametro(self, ctx:laParser.ParametroContext):
		for identifier in ctx.identificador():
			self.visitIdentificador(identifier)
		return self.visitTipo_estendido(ctx.tipo_estendido())


	# Visit a parse tree produced by laParser#parametros.
	def visitParametros(self, ctx:laParser.ParametrosContext):
		parametersString = ''
		for parameter in ctx.parametro():
			parametersString += self.visitParametro(parameter) + ' '
		return parametersString


	# Visit a parse tree produced by laParser#corpo.
	def visitCorpo(self, ctx:laParser.CorpoContext):
		for declL in ctx.declaracao_local():
			self.visitDeclaracao_local(declL)
		for command in ctx.cmd():
			self.visitCmd(command)


	# Visit a parse tree produced by laParser#cmd.
	def visitCmd(self, ctx:laParser.CmdContext):
		if(ctx.cmdLeia() != None):
			self.visitCmdLeia(ctx.cmdLeia())
		if(ctx.cmdEscreva() != None):
			self.visitCmdEscreva(ctx.cmdEscreva())
		if(ctx.cmdSe() != None):
			self.visitCmdSe(ctx.cmdSe())
		if(ctx.cmdCaso() != None):
			self.visitCmdCaso(ctx.cmdCaso())
		if(ctx.cmdPara() != None):
			self.visitCmdPara(ctx.cmdPara())
		if(ctx.cmdEnquanto() != None):
			self.visitCmdEnquanto(ctx.cmdEnquanto())
		if(ctx.cmdFaca() != None):
			self.visitCmdFaca(ctx.cmdFaca())
		if(ctx.cmdAtribuicao() != None):
			self.visitCmdAtribuicao(ctx.cmdAtribuicao())
		if(ctx.cmdChamada() != None):
			self.visitCmdChamada(ctx.cmdChamada())
		if(ctx.cmdRetorne() != None):
			self.visitCmdRetorne(ctx.cmdRetorne())


	# Visit a parse tree produced by laParser#cmdLeia.
	def visitCmdLeia(self, ctx:laParser.CmdLeiaContext):
		for identifier in ctx.identificador():
			identificadores = identifier.getText().split('.')
			for element in identificadores:
				if(element not in self.tabelaSimbolosVariaveis.keys()):
					self.errors += "Linha " + str(ctx.start.line) + ": identificador " + identifier.getText() + " nao declarado\n"	
			self.visitIdentificador(identifier)


	# Visit a parse tree produced by laParser#cmdEscreva.
	def visitCmdEscreva(self, ctx:laParser.CmdEscrevaContext):
		for expression in ctx.expressao():
			self.visitExpressao(expression)


	# Visit a parse tree produced by laParser#cmdSe.
	def visitCmdSe(self, ctx:laParser.CmdSeContext):
		self.visitExpressao(ctx.expressao())
		for command in ctx.cmd():
			self.visitCmd(command)


	# Visit a parse tree produced by laParser#cmdCaso.
	def visitCmdCaso(self, ctx:laParser.CmdCasoContext):
		self.visitExp_aritmetica(ctx.exp_aritmetica())
		self.visitSelecao(ctx.selecao())
		for command in ctx.cmd():
			self.visitCmd(command)


	# Visit a parse tree produced by laParser#cmdPara.
	def visitCmdPara(self, ctx:laParser.CmdParaContext):
		self.visitExp_aritmetica(ctx.exp_aritmetica(0))
		self.visitExp_aritmetica(ctx.exp_aritmetica(1))
		for command in ctx.cmd():
			self.visitCmd(command)

	# Visit a parse tree produced by laParser#cmdEnquanto.
	def visitCmdEnquanto(self, ctx:laParser.CmdEnquantoContext):
		self.visitExpressao(ctx.expressao())
		for command in ctx.cmd():
			self.visitCmd(command)


	# Visit a parse tree produced by laParser#cmdFaca.
	def visitCmdFaca(self, ctx:laParser.CmdFacaContext):
		for command in ctx.cmd():
			self.visitCmd(command)
		self.visitExpressao(ctx.expressao())


	# Visit a parse tree produced by laParser#cmdAtribuicao.
	def visitCmdAtribuicao(self, ctx:laParser.CmdAtribuicaoContext):
		self.visitIdentificador(ctx.identificador())
		identifier = ctx.identificador().getText().split('.')[-1]
		exprValue = self.visitExpressao(ctx.expressao())
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
	def visitCmdChamada(self, ctx:laParser.CmdChamadaContext):
		for expression in ctx.expressao():
			self.visitExpressao(expression)


	# Visit a parse tree produced by laParser#cmdRetorne.
	def visitCmdRetorne(self, ctx:laParser.CmdRetorneContext):
		self.visitExpressao(ctx.expressao())


	# Visit a parse tree produced by laParser#selecao.
	def visitSelecao(self, ctx:laParser.SelecaoContext):
		for selection in ctx.item_selecao():
			self.visitItem_selecao(selection)


	# Visit a parse tree produced by laParser#item_selecao.
	def visitItem_selecao(self, ctx:laParser.Item_selecaoContext):
		self.visitConstantes(ctx.constantes())
		for command in ctx.cmd():
			self.visitCmd(command)


	# Visit a parse tree produced by laParser#constantes.
	def visitConstantes(self, ctx:laParser.ConstantesContext):
		for numInterval in ctx.numero_intervalo():
			self.visitNumero_intervalo(numInterval)


	# Visit a parse tree produced by laParser#numero_intervalo.
	def visitNumero_intervalo(self, ctx:laParser.Numero_intervaloContext):
		for opUN in ctx.op_unario():
			self.visitOp_unario(opUN)


	# Visit a parse tree produced by laParser#op_unario.
	def visitOp_unario(self, ctx:laParser.Op_unarioContext):
		if (type(ctx) != None):
			return ctx.getText()


	# Visit a parse tree produced by laParser#exp_aritmetica.
	def visitExp_aritmetica(self, ctx:laParser.Exp_aritmeticaContext):
		primTermoText = self.visitTermo(ctx.termo(0))
		for i in range(0, len(ctx.op1())):
			self.visitOp1(ctx.op1(i))
			outroTermoText = self.visitTermo(ctx.termo(i+1))
			if(primTermoText != outroTermoText):
				return 'errorType'
		return primTermoText


	# Visit a parse tree produced by laParser#termo.
	def visitTermo(self, ctx:laParser.TermoContext):
		fatorText = ''
		fatorText = self.visitFator(ctx.fator(0))
		for i in range(0, len(ctx.op2())):
			self.visitOp2(ctx.op2(i))
			fatorText2 = self.visitFator(ctx.fator(i+1))
			if(fatorText2 != fatorText):
				if((fatorText == 'real' or fatorText == 'inteiro') and (fatorText2 == 'real' or fatorText2 == 'inteiro')):
					if(fatorText == 'real' or fatorText2 == 'real'):
						return 'real'
					else:
						return 'inteiro'
				fatorText = "errorType"
		return fatorText


	# Visit a parse tree produced by laParser#fator.
	def visitFator(self, ctx:laParser.FatorContext):
		parcelasText = ''
		parcelaType = self.visitParcela(ctx.parcela(0))
		if(parcelaType != None):
			parcelasText += parcelaType
		for i in range(0, len(ctx.op3())):
			self.visitOp3(ctx.op3(i))
			parcelasType2 = self.visitParcela(ctx.parcela(i+1))
			if(parcelasType2 != parcelasText):
				if((parcelasText == 'real' or parcelasText == 'inteiro') and (parcelasText2 == 'real' or parcelasText2 == 'inteiro')):
					if(parcelasText == 'real' or parcelasText2 == 'real'):
						return 'real'
					else:
						return 'inteiro'
				parcelasText = "errorType"
		return parcelasText


	# Visit a parse tree produced by laParser#op1.
	def visitOp1(self, ctx:laParser.Op1Context):
		return ctx.getText()


	# Visit a parse tree produced by laParser#op2.
	def visitOp2(self, ctx:laParser.Op2Context):
		return ctx.getText()


	# Visit a parse tree produced by laParser#op3.
	def visitOp3(self, ctx:laParser.Op3Context):
		return ctx.getText()


	# Visit a parse tree produced by laParser#parcela.
	def visitParcela(self, ctx:laParser.ParcelaContext):
		if(ctx.parcela_unario() != None):
			if(ctx.op_unario() != None):
				self.visitOp_unario(ctx.op_unario())
			return self.visitParcela_unario(ctx.parcela_unario())
		else:
			return self.visitParcela_nao_unario(ctx.parcela_nao_unario())


	# Visit a parse tree produced by laParser#parcela_unario.
	def visitParcela_unario(self, ctx:laParser.Parcela_unarioContext):
		if(ctx.identificador() != None):
			#print('unary identifier')
			#print(ctx.identificador().getText())
			identNameBefore = self.visitIdentificador(ctx.identificador())
			identName = identNameBefore.split('.')
			isErrorType = False
			for element in identName:
				if(element not in self.tabelaSimbolosVariaveis.keys()):
					self.errors += "Linha " + str(ctx.identificador().start.line) + ": identificador " + identNameBefore + " nao declarado\n"
					isErrorType = True
			if (isErrorType == True):
				return 'errorType'
			else:
				return self.tabelaSimbolosVariaveis[identName[-1]]
		elif(ctx.expr != None):
			#print('unary ident')
			#print(ctx.IDENT().getText())
			for expression in ctx.expressao():
				self.visitExpressao(expression)
		elif(ctx.outraExpr != None):
			return self.visitExpressao(ctx.expressao(0))
			#print(ctx.expressao(0).getText())
		else:
			if('.' in ctx.getText()):
				return 'real'
			return 'inteiro'


	# Visit a parse tree produced by laParser#parcela_nao_unario.
	def visitParcela_nao_unario(self, ctx:laParser.Parcela_nao_unarioContext):
		if(ctx.identificador() != None):
			#print('nãoUn')
			#print(ctx.identificador().getText())
			self.visitIdentificador(ctx.identificador())
			return self.tabelaSimbolosVariaveis[ctx.identificador().getText()]
		else:
			return 'literal'


	# Visit a parse tree produced by laParser#exp_relacional.
	def visitExp_relacional(self, ctx:laParser.Exp_relacionalContext):
		expArit1 = self.visitExp_aritmetica(ctx.exp_aritmetica(0))
		if(ctx.op_relacional() != None):
			self.visitOp_relacional(ctx.op_relacional())
			expArit2 = self.visitExp_aritmetica(ctx.exp_aritmetica(1))
			if(expArit1 != expArit2):
				return 'errorType'
			else:
				return 'logico'
		return expArit1


	# Visit a parse tree produced by laParser#op_relacional.
	def visitOp_relacional(self, ctx:laParser.Op_relacionalContext):
		return ctx.getText()


	# Visit a parse tree produced by laParser#expressao.
	def visitExpressao(self, ctx:laParser.ExpressaoContext):
		primTermLog = self.visitTermo_logico(ctx.termo_logico(0))
		for i in range(0,len(ctx.op_logico_1())):
			self.visitOp_logico_1(ctx.op_logico_1(i))
			outroTermLog = self.visitTermo_logico(ctx.termo_logico(i+1))
			if( primTermLog != outroTermLog ):
				return "errorType"
		return primTermLog


	# Visit a parse tree produced by laParser#termo_logico.
	def visitTermo_logico(self, ctx:laParser.Termo_logicoContext):
		primFatLog = self.visitFator_logico(ctx.fator_logico(0))
		for i in range(0,len(ctx.op_logico_2())):
			self.visitOp_logico_2(ctx.op_logico_2(i))
			outroFatLog = self.visitFator_logico(ctx.fator_logico(i+1))
			if( primFatLog != outroFatLog ):
				return "errorType"
		return primFatLog


	# Visit a parse tree produced by laParser#fator_logico.
	def visitFator_logico(self, ctx:laParser.Fator_logicoContext):
		parLog = self.visitParcela_logica(ctx.parcela_logica())
		if(parLog != None):
			return parLog


	# Visit a parse tree produced by laParser#parcela_logica.
	def visitParcela_logica(self, ctx:laParser.Parcela_logicaContext):
		if(ctx.exp_relacional() != None):
			return self.visitExp_relacional(ctx.exp_relacional())
		else:
			if(ctx.getText() == 'verdadeiro' or ctx.getText() == 'falso'):
				return 'logico'
			return 'errorType'


	# Visit a parse tree produced by laParser#op_logico_1.
	def visitOp_logico_1(self, ctx:laParser.Op_logico_1Context):
		return ctx.getText()


	# Visit a parse tree produced by laParser#op_logico_2.
	def visitOp_logico_2(self, ctx:laParser.Op_logico_2Context):
		return ctx.getText()