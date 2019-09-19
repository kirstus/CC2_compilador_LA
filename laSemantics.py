from antlr4 import *
from laListener import laListener
from laParser import laParser
from laVisitor import laVisitor

class laSemantics(laVisitor):
	errors = ""
	tabelaSimbolosVariaveis = {}
	tabelaSimbolosFuncoes = {}

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
			visitDeclaracao_global(ctx.declaracao_global())

	# Visit a parse tree produced by laParser#declaracao_local.
	def visitDeclaracao_local(self, ctx:laParser.Declaracao_localContext):
		if('declare' in ctx.getText()):
			self.visitVariavel(ctx.variavel())
		elif('constante' in ctx.getText()):
			if(ctx.IDENT().getText() not in tabelaSimbolosVariaveis.keys()):
				self.visitTipo_basico(ctx.tipo_basico())
				tabelaSimbolosVariaveis[ctx.IDENT().getText()] = ctx.tipo_basico().getText()
				self.visitValor_constante(ctx.valor_constante())
			else:
				self.errors += "Linha " + str(ctx.start.line) + ": identificador " + ctx.IDENT().getText() + " ja declarado anteriormente\n"
		elif('tipo' in ctx.getText()):
			if(ctx.IDENT().getText() not in tabelaSimbolosVariaveis.keys()):
				tabelaSimbolosVariaveis[ctx.IDENT().getText()] = "tipo"
				self.visitTipo(ctx.tipo())
			else:
				self.errors += "Linha " + str(ctx.start.line) + ": identificador " + ctx.IDENT().getText() + " ja declarado anteriormente\n"


	 # Visit a parse tree produced by laParser#variavel.
	def visitVariavel(self, ctx:laParser.VariavelContext):
		for i in range(0, len(ctx.identificador())):
			self.visitIdentificador(ctx.identificador(i))
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


	'''# Visit a parse tree produced by laParser#tipo.
	def visitTipo(self, ctx:laParser.TipoContext):
		return self.visitChildren(ctx)


	# Visit a parse tree produced by laParser#tipo_basico.
	def visitTipo_basico(self, ctx:laParser.Tipo_basicoContext):
		return self.visitChildren(ctx)


	# Visit a parse tree produced by laParser#tipo_basico_ident.
	def visitTipo_basico_ident(self, ctx:laParser.Tipo_basico_identContext):
		return self.visitChildren(ctx)


	# Visit a parse tree produced by laParser#tipo_estendido.
	def visitTipo_estendido(self, ctx:laParser.Tipo_estendidoContext):
		return self.visitChildren(ctx)


	# Visit a parse tree produced by laParser#valor_constante.
	def visitValor_constante(self, ctx:laParser.Valor_constanteContext):
		return self.visitChildren(ctx)


	# Visit a parse tree produced by laParser#registro.
	def visitRegistro(self, ctx:laParser.RegistroContext):
		return self.visitChildren(ctx)


	# Visit a parse tree produced by laParser#declaracao_global.
	def visitDeclaracao_global(self, ctx:laParser.Declaracao_globalContext):
		return self.visitChildren(ctx)


	# Visit a parse tree produced by laParser#parametro.
	def visitParametro(self, ctx:laParser.ParametroContext):
		return self.visitChildren(ctx)


	# Visit a parse tree produced by laParser#parametros.
	def visitParametros(self, ctx:laParser.ParametrosContext):
		return self.visitChildren(ctx)


	# Visit a parse tree produced by laParser#corpo.
	def visitCorpo(self, ctx:laParser.CorpoContext):
		return self.visitChildren(ctx)


	# Visit a parse tree produced by laParser#cmd.
	def visitCmd(self, ctx:laParser.CmdContext):
		return self.visitChildren(ctx)


	# Visit a parse tree produced by laParser#cmdLeia.
	def visitCmdLeia(self, ctx:laParser.CmdLeiaContext):
		return self.visitChildren(ctx)


	# Visit a parse tree produced by laParser#cmdEscreva.
	def visitCmdEscreva(self, ctx:laParser.CmdEscrevaContext):
		return self.visitChildren(ctx)


	# Visit a parse tree produced by laParser#cmdSe.
	def visitCmdSe(self, ctx:laParser.CmdSeContext):
		return self.visitChildren(ctx)


	# Visit a parse tree produced by laParser#cmdCaso.
	def visitCmdCaso(self, ctx:laParser.CmdCasoContext):
		return self.visitChildren(ctx)


	# Visit a parse tree produced by laParser#cmdPara.
	def visitCmdPara(self, ctx:laParser.CmdParaContext):
		return self.visitChildren(ctx)


	# Visit a parse tree produced by laParser#cmdEnquanto.
	def visitCmdEnquanto(self, ctx:laParser.CmdEnquantoContext):
		return self.visitChildren(ctx)


	# Visit a parse tree produced by laParser#cmdFaca.
	def visitCmdFaca(self, ctx:laParser.CmdFacaContext):
		return self.visitChildren(ctx)


	# Visit a parse tree produced by laParser#cmdAtribuicao.
	def visitCmdAtribuicao(self, ctx:laParser.CmdAtribuicaoContext):
		return self.visitChildren(ctx)


	# Visit a parse tree produced by laParser#cmdChamada.
	def visitCmdChamada(self, ctx:laParser.CmdChamadaContext):
		return self.visitChildren(ctx)


	# Visit a parse tree produced by laParser#cmdRetorne.
	def visitCmdRetorne(self, ctx:laParser.CmdRetorneContext):
		return self.visitChildren(ctx)


	# Visit a parse tree produced by laParser#selecao.
	def visitSelecao(self, ctx:laParser.SelecaoContext):
		return self.visitChildren(ctx)


	# Visit a parse tree produced by laParser#item_selecao.
	def visitItem_selecao(self, ctx:laParser.Item_selecaoContext):
		return self.visitChildren(ctx)


	# Visit a parse tree produced by laParser#constantes.
	def visitConstantes(self, ctx:laParser.ConstantesContext):
		return self.visitChildren(ctx)


	# Visit a parse tree produced by laParser#numero_intervalo.
	def visitNumero_intervalo(self, ctx:laParser.Numero_intervaloContext):
		return self.visitChildren(ctx)


	# Visit a parse tree produced by laParser#op_unario.
	def visitOp_unario(self, ctx:laParser.Op_unarioContext):
		return self.visitChildren(ctx)


	# Visit a parse tree produced by laParser#exp_aritmetica.
	def visitExp_aritmetica(self, ctx:laParser.Exp_aritmeticaContext):
		return self.visitChildren(ctx)


	# Visit a parse tree produced by laParser#termo.
	def visitTermo(self, ctx:laParser.TermoContext):
		return self.visitChildren(ctx)


	# Visit a parse tree produced by laParser#fator.
	def visitFator(self, ctx:laParser.FatorContext):
		return self.visitChildren(ctx)


	# Visit a parse tree produced by laParser#op1.
	def visitOp1(self, ctx:laParser.Op1Context):
		return self.visitChildren(ctx)


	# Visit a parse tree produced by laParser#op2.
	def visitOp2(self, ctx:laParser.Op2Context):
		return self.visitChildren(ctx)


	# Visit a parse tree produced by laParser#op3.
	def visitOp3(self, ctx:laParser.Op3Context):
		return self.visitChildren(ctx)


	# Visit a parse tree produced by laParser#parcela.
	def visitParcela(self, ctx:laParser.ParcelaContext):
		return self.visitChildren(ctx)


	# Visit a parse tree produced by laParser#parcela_unario.
	def visitParcela_unario(self, ctx:laParser.Parcela_unarioContext):
		return self.visitChildren(ctx)


	# Visit a parse tree produced by laParser#parcela_nao_unario.
	def visitParcela_nao_unario(self, ctx:laParser.Parcela_nao_unarioContext):
		return self.visitChildren(ctx)


	# Visit a parse tree produced by laParser#exp_relacional.
	def visitExp_relacional(self, ctx:laParser.Exp_relacionalContext):
		return self.visitChildren(ctx)


	# Visit a parse tree produced by laParser#op_relacional.
	def visitOp_relacional(self, ctx:laParser.Op_relacionalContext):
		return self.visitChildren(ctx)


	# Visit a parse tree produced by laParser#expressao.
	def visitExpressao(self, ctx:laParser.ExpressaoContext):
		return self.visitChildren(ctx)


	# Visit a parse tree produced by laParser#termo_logico.
	def visitTermo_logico(self, ctx:laParser.Termo_logicoContext):
		return self.visitChildren(ctx)


	# Visit a parse tree produced by laParser#fator_logico.
	def visitFator_logico(self, ctx:laParser.Fator_logicoContext):
		return self.visitChildren(ctx)


	# Visit a parse tree produced by laParser#parcela_logica.
	def visitParcela_logica(self, ctx:laParser.Parcela_logicaContext):
		return self.visitChildren(ctx)


	# Visit a parse tree produced by laParser#op_logico_1.
	def visitOp_logico_1(self, ctx:laParser.Op_logico_1Context):
		return self.visitChildren(ctx)


	# Visit a parse tree produced by laParser#op_logico_2.
	def visitOp_logico_2(self, ctx:laParser.Op_logico_2Context):
		return self.visitChildren(ctx)
'''