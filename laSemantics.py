from antlr4 import *
from laListener import laListener
from laParser import laParser
from laVisitor import laVisitor

class laSemantics(laVisitor):
	errors = ""

	def visitPrograma(self, ctx:laParser.ProgramaContext):


	# Visit a parse tree produced by laParser#declaracoes.
	def visitDeclaracoes(self, ctx:laParser.DeclaracoesContext):


	# Visit a parse tree produced by laParser#decl_local_global.
	def visitDecl_local_global(self, ctx:laParser.Decl_local_globalContext):


	# Visit a parse tree produced by laParser#declaracao_local.
	def visitDeclaracao_local(self, ctx:laParser.Declaracao_localContext):


	# Visit a parse tree produced by laParser#variavel.
	def visitVariavel(self, ctx:laParser.VariavelContext):


	# Visit a parse tree produced by laParser#identificador.
	def visitIdentificador(self, ctx:laParser.IdentificadorContext):


	# Visit a parse tree produced by laParser#dimensao.
	def visitDimensao(self, ctx:laParser.DimensaoContext):


	# Visit a parse tree produced by laParser#tipo.
	def visitTipo(self, ctx:laParser.TipoContext):


	# Visit a parse tree produced by laParser#tipo_basico.
	def visitTipo_basico(self, ctx:laParser.Tipo_basicoContext):


	# Visit a parse tree produced by laParser#tipo_basico_ident.
	def visitTipo_basico_ident(self, ctx:laParser.Tipo_basico_identContext):


	# Visit a parse tree produced by laParser#tipo_estendido.
	def visitTipo_estendido(self, ctx:laParser.Tipo_estendidoContext):


	# Visit a parse tree produced by laParser#valor_constante.
	def visitValor_constante(self, ctx:laParser.Valor_constanteContext):


	# Visit a parse tree produced by laParser#registro.
	def visitRegistro(self, ctx:laParser.RegistroContext):


	# Visit a parse tree produced by laParser#declaracao_global.
	def visitDeclaracao_global(self, ctx:laParser.Declaracao_globalContext):


	# Visit a parse tree produced by laParser#parametro.
	def visitParametro(self, ctx:laParser.ParametroContext):


	# Visit a parse tree produced by laParser#parametros.
	def visitParametros(self, ctx:laParser.ParametrosContext):


	# Visit a parse tree produced by laParser#corpo.
	def visitCorpo(self, ctx:laParser.CorpoContext):


	# Visit a parse tree produced by laParser#cmd.
	def visitCmd(self, ctx:laParser.CmdContext):


	# Visit a parse tree produced by laParser#cmdLeia.
	def visitCmdLeia(self, ctx:laParser.CmdLeiaContext):


	# Visit a parse tree produced by laParser#cmdEscreva.
	def visitCmdEscreva(self, ctx:laParser.CmdEscrevaContext):


	# Visit a parse tree produced by laParser#cmdSe.
	def visitCmdSe(self, ctx:laParser.CmdSeContext):


	# Visit a parse tree produced by laParser#cmdCaso.
	def visitCmdCaso(self, ctx:laParser.CmdCasoContext):


	# Visit a parse tree produced by laParser#cmdPara.
	def visitCmdPara(self, ctx:laParser.CmdParaContext):


	# Visit a parse tree produced by laParser#cmdEnquanto.
	def visitCmdEnquanto(self, ctx:laParser.CmdEnquantoContext):


	# Visit a parse tree produced by laParser#cmdFaca.
	def visitCmdFaca(self, ctx:laParser.CmdFacaContext):


	# Visit a parse tree produced by laParser#cmdAtribuicao.
	def visitCmdAtribuicao(self, ctx:laParser.CmdAtribuicaoContext):


	# Visit a parse tree produced by laParser#cmdChamada.
	def visitCmdChamada(self, ctx:laParser.CmdChamadaContext):


	# Visit a parse tree produced by laParser#cmdRetorne.
	def visitCmdRetorne(self, ctx:laParser.CmdRetorneContext):


	# Visit a parse tree produced by laParser#selecao.
	def visitSelecao(self, ctx:laParser.SelecaoContext):


	# Visit a parse tree produced by laParser#item_selecao.
	def visitItem_selecao(self, ctx:laParser.Item_selecaoContext):


	# Visit a parse tree produced by laParser#constantes.
	def visitConstantes(self, ctx:laParser.ConstantesContext):


	# Visit a parse tree produced by laParser#numero_intervalo.
	def visitNumero_intervalo(self, ctx:laParser.Numero_intervaloContext):


	# Visit a parse tree produced by laParser#op_unario.
	def visitOp_unario(self, ctx:laParser.Op_unarioContext):


	# Visit a parse tree produced by laParser#exp_aritmetica.
	def visitExp_aritmetica(self, ctx:laParser.Exp_aritmeticaContext):


	# Visit a parse tree produced by laParser#termo.
	def visitTermo(self, ctx:laParser.TermoContext):


	# Visit a parse tree produced by laParser#fator.
	def visitFator(self, ctx:laParser.FatorContext):


	# Visit a parse tree produced by laParser#op1.
	def visitOp1(self, ctx:laParser.Op1Context):


	# Visit a parse tree produced by laParser#op2.
	def visitOp2(self, ctx:laParser.Op2Context):


	# Visit a parse tree produced by laParser#op3.
	def visitOp3(self, ctx:laParser.Op3Context):


	# Visit a parse tree produced by laParser#parcela.
	def visitParcela(self, ctx:laParser.ParcelaContext):


	# Visit a parse tree produced by laParser#parcela_unario.
	def visitParcela_unario(self, ctx:laParser.Parcela_unarioContext):


	# Visit a parse tree produced by laParser#parcela_nao_unario.
	def visitParcela_nao_unario(self, ctx:laParser.Parcela_nao_unarioContext):


	# Visit a parse tree produced by laParser#exp_relacional.
	def visitExp_relacional(self, ctx:laParser.Exp_relacionalContext):


	# Visit a parse tree produced by laParser#op_relacional.
	def visitOp_relacional(self, ctx:laParser.Op_relacionalContext):


	# Visit a parse tree produced by laParser#expressao.
	def visitExpressao(self, ctx:laParser.ExpressaoContext):


	# Visit a parse tree produced by laParser#termo_logico.
	def visitTermo_logico(self, ctx:laParser.Termo_logicoContext):


	# Visit a parse tree produced by laParser#fator_logico.
	def visitFator_logico(self, ctx:laParser.Fator_logicoContext):


	# Visit a parse tree produced by laParser#parcela_logica.
	def visitParcela_logica(self, ctx:laParser.Parcela_logicaContext):


	# Visit a parse tree produced by laParser#op_logico_1.
	def visitOp_logico_1(self, ctx:laParser.Op_logico_1Context):


	# Visit a parse tree produced by laParser#op_logico_2.
	def visitOp_logico_2(self, ctx:laParser.Op_logico_2Context):