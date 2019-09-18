from antlr4 import *
from laListener import laListener
from laParser import laParser
from laVisitor import laVisitor

class laSemantics(laVisitor):
	errors = ""
	tabelaSimbolosVariaveis = {}
	tabelaSimbolosFuncoes = {}

	def visitPrograma(self, ctx:laParser.ProgramaContext):
		self.visitDeclaracoes(ctx.declaracoes())
		self.visitCorpo(ctx.corpo())

	# Visit a parse tree produced by laParser#declaracoes.
	def visitDeclaracoes(self, ctx:laParser.DeclaracoesContext):
		for i in range(0, len(ctx.decl_local_global())):
			self.visitDecl_local_global(ctx.decl_local_global(i))

	# Visit a parse tree produced by laParser#decl_local_global.
	def visitDecl_local_global(self, ctx:laParser.Decl_local_globalContext):
		self.visitDeclaracao_local(ctx.declaracao_local())
		self.VvisitDeclaracao_global(ctx.declaracao_global())

	# Visit a parse tree produced by laParser#declaracao_local.
	def visitDeclaracao_local(self, ctx:laParser.Declaracao_localContext):
		if('declare' in ctx.getText()):
			self.visitVariavel(ctx.variavel())
		elif('constante' in ctx.getText()):
			if(ctx.IDENT() not in tabelaSimbolosVariaveis.keys()):
				self.visitTipo_basico(ctx.tipo_basico())
				tabelaSimbolosVariaveis[ctx.IDENT().getText()] = ctx.tipo_basico().getText()
				self.visitValor_constante(ctx.valor_constante())
			else:
				self.errors += "Linha " + str(ctx.start.line) + ": identificador " + str(ctx.IDENT().getText()) + " ja declarado anteriormente\n"
		elif('tipo' in ctx.getText()):
			self.visitTipo(ctx.TipoContext())

	# Visit a parse tree produced by laParser#variavel.
	def visitVariavel(self, ctx:laParser.VariavelContext):
		print(ctx.getText())
		for i in range(0, len(ctx.identificador())):
			self.visitIdentificador(ctx.identificador(i))
		self.visitTipo(ctx.tipo())

	# Visit a parse tree produced by laParser#identificador.
	def visitIdentificador(self, ctx:laParser.IdentificadorContext):
		self.visitDimensao(ctx.dimensao())

	# Visit a parse tree produced by laParser#dimensao.
	def visitDimensao(self, ctx:laParser.DimensaoContext):
		if(ctx.dimensao() != None):
			self.visitExp_aritmetica(ctx.exp_aritmetica())
			self.visitDimensao(ctx.dimensao())

	# Visit a parse tree produced by laParser#tipo.
	def visitTipo(self, ctx:laParser.TipoContext):
		if(ctx.registro() != None):
			self.visitRegistro(ctx.registro())
		elif(ctx.tipo_estendido() != None):
			self.visitTipo_estendido(ctx.tipo_estendido())

	# Visit a parse tree produced by laParser#tipo_basico.
	def visitTipo_basico(self, ctx:laParser.Tipo_basicoContext):
		print("Nada")

	# Visit a parse tree produced by laParser#tipo_basico_ident.
	def visitTipo_basico_ident(self, ctx:laParser.Tipo_basico_identContext):
		if(ctx.tipo_basico() != None):
			self.visitTipo_basico(ctx.tipo_basico())

	# Visit a parse tree produced by laParser#tipo_estendido.
	def visitTipo_estendido(self, ctx:laParser.Tipo_estendidoContext):
		self.visitTipo_basico_ident(ctx.tipo_basico_ident())

	# Visit a parse tree produced by laParser#valor_constante.
	def visitValor_constante(self, ctx:laParser.Valor_constanteContext):
		print("Nada")

	# Visit a parse tree produced by laParser#registro.
	def visitRegistro(self, ctx:laParser.RegistroContext):
		for i in range(0, len(ctx.variavel())):
			self.visitVariavel(ctx.variavel(i))

	# Visit a parse tree produced by laParser#declaracao_global.
	def visitDeclaracao_global(self, ctx:laParser.Declaracao_globalContext):
		if(ctx.parametro() != None):
			self.visitParametro(ctx.parametro())

		if('fim_funcao' in ctx.getText()):
			self.visitTipo_estendido(ctx.tipo_estendido())

		for i in range(0, len(ctx.declaracao_local())):
			self.visitDeclaracao_local(ctx.declaracao_local(i))

		for i in range(0, len(ctx.cmd())):
			self.visitCmd(ctx.cmd(i))


	# Visit a parse tree produced by laParser#parametro.
	def visitParametro(self, ctx:laParser.ParametroContext):
		for i in range(0, len(ctx.identificador())):
			self.visitIdentificador(ctx.identificador(i))
		self.visitTipo_estendido(ctx.tipo_estendido())

	# Visit a parse tree produced by laParser#parametros.
	def visitParametros(self, ctx:laParser.ParametrosContext):
		for i in range(0, len(ctx.parametro())):
			self.visitParametro(ctx.parametro(i))

	# Visit a parse tree produced by laParser#corpo.
	def visitCorpo(self, ctx:laParser.CorpoContext):
		for i in range(0, len(ctx.declaracao_local())):
			self.visitDeclaracao_local(ctx.declaracao_local(i))
		for i in range(0, len(ctx.cmd())):
			self.visitCmd(ctx.cmd(i))


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
			self.cmdEnquanto(ctx.cmdEnquanto())
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
		for i in range(0, len(ctx.identificador())):
			self.visitIdentificador(ctx.identificador(i))

	# Visit a parse tree produced by laParser#cmdEscreva.
	def visitCmdEscreva(self, ctx:laParser.CmdEscrevaContext):
		for i in range(0, len(ctx.expressao())):
			self.visitExpressao(ctx.expressao(i))

	# Visit a parse tree produced by laParser#cmdSe.
	def visitCmdSe(self, ctx:laParser.CmdSeContext):
		self.visitExpressao(ctx.expressao())
		for i in range(0, len(ctx.cmd())):
			self.visitCmd(ctx.cmd(i))

	# Visit a parse tree produced by laParser#cmdCaso.
	def visitCmdCaso(self, ctx:laParser.CmdCasoContext):
		self.visitExp_aritmetica(ctx.exp_aritmetica())
		self.visitSelecao(ctx.selecao())
		for i in range(0, len(ctx.cmd())):
			self.visitCmd(ctx.cmd(i))

	# Visit a parse tree produced by laParser#cmdPara.
	def visitCmdPara(self, ctx:laParser.CmdParaContext):
		self.visitExp_aritmetica(ctx.exp_aritmetica())
		self.visitExp_aritmetica(ctx.exp_aritmetica())
		for i in range(0, len(ctx.cmd())):
			self.visitCmd(ctx.cmd(i))
			
	# Visit a parse tree produced by laParser#cmdEnquanto.
	def visitCmdEnquanto(self, ctx:laParser.CmdEnquantoContext):
		self.visitExpressao(ctx.expressao())
		for i in range(0, len(ctx.cmd())):
			self.visitCmd(ctx.cmd(i))

	# Visit a parse tree produced by laParser#cmdFaca.
	def visitCmdFaca(self, ctx:laParser.CmdFacaContext):
		for i in range(0, len(ctx.cmd())):
			self.visitCmd(ctx.cmd(i))
		self.visitExpressao(ctx.expressao())

	# Visit a parse tree produced by laParser#cmdAtribuicao.
	def visitCmdAtribuicao(self, ctx:laParser.CmdAtribuicaoContext):
		self.visitIdentificador(ctx.identificador())
		self.visitExpressao(ctx.expressao())

	# Visit a parse tree produced by laParser#cmdChamada.
	def visitCmdChamada(self, ctx:laParser.CmdChamadaContext):
		self.visitExpressao(ctx.expressao(0))
		for i in range(1, len(ctx.expressao())):
			self.visitExpressao(ctx.expressao(i))

	# Visit a parse tree produced by laParser#cmdRetorne.
	def visitCmdRetorne(self, ctx:laParser.CmdRetorneContext):
		self.visitExpressao(ctx.expressao())

	# Visit a parse tree produced by laParser#selecao.
	def visitSelecao(self, ctx:laParser.SelecaoContext):
		for i in range(0, len(ctx.item_selecao())):
			self.visitItem_selecao(ctx.item_selecao(i))

	# Visit a parse tree produced by laParser#item_selecao.
	def visitItem_selecao(self, ctx:laParser.Item_selecaoContext):
		self.visitConstantes(ctx.constantes())
		for i in range(0, len(ctx.cmd())):
			self.visitCmd(ctx.cmd(i))

	# Visit a parse tree produced by laParser#constantes.
	def visitConstantes(self, ctx:laParser.ConstantesContext):
		self.visitNumero_intervalo(ctx.numero_intervalo(0))
		for i in range(1, len(ctx.numero_intervalo())):
			self.visitNumero_intervalo(ctx.numero_intervalo(i))

	# Visit a parse tree produced by laParser#numero_intervalo.
	def visitNumero_intervalo(self, ctx:laParser.Numero_intervaloContext):
		if(ctx.op_unario() != None):
			self.visitOp_unario(ctx.op_unario())
		if(len(ctx.numero_intervalo())) > 1:
			self.visitOp_unario(ctx.op_unario())

	# Visit a parse tree produced by laParser#op_unario.
	def visitOp_unario(self, ctx:laParser.Op_unarioContext):
		 return ctx.getText()

	# Visit a parse tree produced by laParser#exp_aritmetica.
	def visitExp_aritmetica(self, ctx:laParser.Exp_aritmeticaContext):
		self.visitTermo(ctx.termo())
		self.visitMaisTermos(ctx.maisTermos())

	# Visit a parse tree produced by laParser#termo.
	def visitTermo(self, ctx:laParser.TermoContext):
		self.visitFator(ctx.fator(0))
		for i in range(0, len(ctx.op2())):
			self.visitOp2(ctx.op2(i))
			self.visitFator(ctx.fator(i+1))

	# Visit a parse tree produced by laParser#maisTermos.
	def visitMaisTermos(self, ctx:laParser.MaisTermosContext):
		if(ctx.op1() != None):
			self.visitOp1(ctx.op1())
			self.visitTermo(ctx.termo())
			self.visitMaisTermos(ctx.maisTermos())

	# Visit a parse tree produced by laParser#fator.
	def visitFator(self, ctx:laParser.FatorContext):
		self.visitParcela(ctx.parcela(0))
		for i in range(0, len(ctx.op3())):
			self.visitOp3(ctx.op3(i))
			self.visitParcela(ctx.parcela(i+1))

	'''
	# Visit a parse tree produced by laParser#op1.
	def visitOp1(self, ctx:laParser.Op1Context):


	# Visit a parse tree produced by laParser#op2.
	def visitOp2(self, ctx:laParser.Op2Context):


	# Visit a parse tree produced by laParser#op3.
	def visitOp3(self, ctx:laParser.Op3Context):

	'''
	# Visit a parse tree produced by laParser#parcela.
	def visitParcela(self, ctx:laParser.ParcelaContext):
		if(ctx.op_unario() != None):
			self.visitOp_unario(ctx.op_unario())
			self.visitParcela_unario(ctx.parcela_unario())
		else:
			self.visitParcela_nao_unario(ctx.parcela_nao_unario())

	# Visit a parse tree produced by laParser#parcela_unario.
	def visitParcela_unario(self, ctx:laParser.Parcela_unarioContext):
		if(ctx.identificador() != None):
			self.visitIdentificador(ctx.identificador())
		if(ctx.expressao() != None):
			for i in range(0, len(ctx.expressao())):
				self.visitExpressao(ctx.expressao(i))

	# Visit a parse tree produced by laParser#parcela_nao_unario.
	def visitParcela_nao_unario(self, ctx:laParser.Parcela_nao_unarioContext):
		if(ctx != None):
			self.visitIdentificador(ctx.identificador())
	
	# Visit a parse tree produced by laParser#exp_relacional.
	def visitExp_relacional(self, ctx:laParser.Exp_relacionalContext):
		self.visitExp_aritmetica(ctx.exp_aritmetica(0))
		if(ctx.op_relacional() != None):
			self.visitOp_relacional(ctx.op_relacional())
			self.visitExp_aritmetica(ctx.exp_aritmetica(1))
	'''
	# Visit a parse tree produced by laParser#op_relacional.
	def visitOp_relacional(self, ctx:laParser.Op_relacionalContext):

	'''
	# Visit a parse tree produced by laParser#expressao.
	def visitExpressao(self, ctx:laParser.ExpressaoContext):
		self.visitTermo_logico(ctx.termo_logico())
		for i in range(0, len(ctx.op_logico_1())):
			self.visitOp_logico_1(ctx.op_logico_1(i))
			self.visitFator_logico(ctx.fator_logico(i))
			
	# Visit a parse tree produced by laParser#termo_logico.
	def visitTermo_logico(self, ctx:laParser.Termo_logicoContext):
		self.visitFator_logico(ctx.fator_logico(0))
		for i in range(0, len(ctx.op_logico_2())):
			self.visitOp_logico_2(ctx.op_logico_2(i))
			self.visitFator_logico(ctx.fator_logico(i+1))
		
	# Visit a parse tree produced by laParser#fator_logico.
	def visitFator_logico(self, ctx:laParser.Fator_logicoContext):
		self.visitParcela_logica(ctx.parcela_logica())
	
	# Visit a parse tree produced by laParser#parcela_logica.
	def visitParcela_logica(self, ctx:laParser.Parcela_logicaContext):
		if(ctx.exp_relacional() != None):
			self.visitExp_relacional(ctx.exp_relacional())
	'''
	# Visit a parse tree produced by laParser#op_logico_1.
	def visitOp_logico_1(self, ctx:laParser.Op_logico_1Context):


	# Visit a parse tree produced by laParser#op_logico_2.
	def visitOp_logico_2(self, ctx:laParser.Op_logico_2Context):'''