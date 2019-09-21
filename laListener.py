# Generated from la.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .laParser import laParser
else:
    from laParser import laParser

# This class defines a complete listener for a parse tree produced by laParser.
class laListener(ParseTreeListener):

    # Enter a parse tree produced by laParser#programa.
    def enterPrograma(self, ctx:laParser.ProgramaContext):
        pass

    # Exit a parse tree produced by laParser#programa.
    def exitPrograma(self, ctx:laParser.ProgramaContext):
        pass


    # Enter a parse tree produced by laParser#declaracoes.
    def enterDeclaracoes(self, ctx:laParser.DeclaracoesContext):
        pass

    # Exit a parse tree produced by laParser#declaracoes.
    def exitDeclaracoes(self, ctx:laParser.DeclaracoesContext):
        pass


    # Enter a parse tree produced by laParser#decl_local_global.
    def enterDecl_local_global(self, ctx:laParser.Decl_local_globalContext):
        pass

    # Exit a parse tree produced by laParser#decl_local_global.
    def exitDecl_local_global(self, ctx:laParser.Decl_local_globalContext):
        pass


    # Enter a parse tree produced by laParser#declaracao_local.
    def enterDeclaracao_local(self, ctx:laParser.Declaracao_localContext):
        pass

    # Exit a parse tree produced by laParser#declaracao_local.
    def exitDeclaracao_local(self, ctx:laParser.Declaracao_localContext):
        pass


    # Enter a parse tree produced by laParser#variavel.
    def enterVariavel(self, ctx:laParser.VariavelContext):
        pass

    # Exit a parse tree produced by laParser#variavel.
    def exitVariavel(self, ctx:laParser.VariavelContext):
        pass


    # Enter a parse tree produced by laParser#identificador.
    def enterIdentificador(self, ctx:laParser.IdentificadorContext):
        pass

    # Exit a parse tree produced by laParser#identificador.
    def exitIdentificador(self, ctx:laParser.IdentificadorContext):
        pass


    # Enter a parse tree produced by laParser#dimensao.
    def enterDimensao(self, ctx:laParser.DimensaoContext):
        pass

    # Exit a parse tree produced by laParser#dimensao.
    def exitDimensao(self, ctx:laParser.DimensaoContext):
        pass


    # Enter a parse tree produced by laParser#tipo.
    def enterTipo(self, ctx:laParser.TipoContext):
        pass

    # Exit a parse tree produced by laParser#tipo.
    def exitTipo(self, ctx:laParser.TipoContext):
        pass


    # Enter a parse tree produced by laParser#tipo_basico.
    def enterTipo_basico(self, ctx:laParser.Tipo_basicoContext):
        pass

    # Exit a parse tree produced by laParser#tipo_basico.
    def exitTipo_basico(self, ctx:laParser.Tipo_basicoContext):
        pass


    # Enter a parse tree produced by laParser#tipo_basico_ident.
    def enterTipo_basico_ident(self, ctx:laParser.Tipo_basico_identContext):
        pass

    # Exit a parse tree produced by laParser#tipo_basico_ident.
    def exitTipo_basico_ident(self, ctx:laParser.Tipo_basico_identContext):
        pass


    # Enter a parse tree produced by laParser#tipo_estendido.
    def enterTipo_estendido(self, ctx:laParser.Tipo_estendidoContext):
        pass

    # Exit a parse tree produced by laParser#tipo_estendido.
    def exitTipo_estendido(self, ctx:laParser.Tipo_estendidoContext):
        pass


    # Enter a parse tree produced by laParser#valor_constante.
    def enterValor_constante(self, ctx:laParser.Valor_constanteContext):
        pass

    # Exit a parse tree produced by laParser#valor_constante.
    def exitValor_constante(self, ctx:laParser.Valor_constanteContext):
        pass


    # Enter a parse tree produced by laParser#registro.
    def enterRegistro(self, ctx:laParser.RegistroContext):
        pass

    # Exit a parse tree produced by laParser#registro.
    def exitRegistro(self, ctx:laParser.RegistroContext):
        pass


    # Enter a parse tree produced by laParser#declaracao_global.
    def enterDeclaracao_global(self, ctx:laParser.Declaracao_globalContext):
        pass

    # Exit a parse tree produced by laParser#declaracao_global.
    def exitDeclaracao_global(self, ctx:laParser.Declaracao_globalContext):
        pass


    # Enter a parse tree produced by laParser#parametro.
    def enterParametro(self, ctx:laParser.ParametroContext):
        pass

    # Exit a parse tree produced by laParser#parametro.
    def exitParametro(self, ctx:laParser.ParametroContext):
        pass


    # Enter a parse tree produced by laParser#parametros.
    def enterParametros(self, ctx:laParser.ParametrosContext):
        pass

    # Exit a parse tree produced by laParser#parametros.
    def exitParametros(self, ctx:laParser.ParametrosContext):
        pass


    # Enter a parse tree produced by laParser#corpo.
    def enterCorpo(self, ctx:laParser.CorpoContext):
        pass

    # Exit a parse tree produced by laParser#corpo.
    def exitCorpo(self, ctx:laParser.CorpoContext):
        pass


    # Enter a parse tree produced by laParser#cmd.
    def enterCmd(self, ctx:laParser.CmdContext):
        pass

    # Exit a parse tree produced by laParser#cmd.
    def exitCmd(self, ctx:laParser.CmdContext):
        pass


    # Enter a parse tree produced by laParser#cmdLeia.
    def enterCmdLeia(self, ctx:laParser.CmdLeiaContext):
        pass

    # Exit a parse tree produced by laParser#cmdLeia.
    def exitCmdLeia(self, ctx:laParser.CmdLeiaContext):
        pass


    # Enter a parse tree produced by laParser#cmdEscreva.
    def enterCmdEscreva(self, ctx:laParser.CmdEscrevaContext):
        pass

    # Exit a parse tree produced by laParser#cmdEscreva.
    def exitCmdEscreva(self, ctx:laParser.CmdEscrevaContext):
        pass


    # Enter a parse tree produced by laParser#cmdSe.
    def enterCmdSe(self, ctx:laParser.CmdSeContext):
        pass

    # Exit a parse tree produced by laParser#cmdSe.
    def exitCmdSe(self, ctx:laParser.CmdSeContext):
        pass


    # Enter a parse tree produced by laParser#cmdCaso.
    def enterCmdCaso(self, ctx:laParser.CmdCasoContext):
        pass

    # Exit a parse tree produced by laParser#cmdCaso.
    def exitCmdCaso(self, ctx:laParser.CmdCasoContext):
        pass


    # Enter a parse tree produced by laParser#cmdPara.
    def enterCmdPara(self, ctx:laParser.CmdParaContext):
        pass

    # Exit a parse tree produced by laParser#cmdPara.
    def exitCmdPara(self, ctx:laParser.CmdParaContext):
        pass


    # Enter a parse tree produced by laParser#cmdEnquanto.
    def enterCmdEnquanto(self, ctx:laParser.CmdEnquantoContext):
        pass

    # Exit a parse tree produced by laParser#cmdEnquanto.
    def exitCmdEnquanto(self, ctx:laParser.CmdEnquantoContext):
        pass


    # Enter a parse tree produced by laParser#cmdFaca.
    def enterCmdFaca(self, ctx:laParser.CmdFacaContext):
        pass

    # Exit a parse tree produced by laParser#cmdFaca.
    def exitCmdFaca(self, ctx:laParser.CmdFacaContext):
        pass


    # Enter a parse tree produced by laParser#cmdAtribuicao.
    def enterCmdAtribuicao(self, ctx:laParser.CmdAtribuicaoContext):
        pass

    # Exit a parse tree produced by laParser#cmdAtribuicao.
    def exitCmdAtribuicao(self, ctx:laParser.CmdAtribuicaoContext):
        pass


    # Enter a parse tree produced by laParser#cmdChamada.
    def enterCmdChamada(self, ctx:laParser.CmdChamadaContext):
        pass

    # Exit a parse tree produced by laParser#cmdChamada.
    def exitCmdChamada(self, ctx:laParser.CmdChamadaContext):
        pass


    # Enter a parse tree produced by laParser#cmdRetorne.
    def enterCmdRetorne(self, ctx:laParser.CmdRetorneContext):
        pass

    # Exit a parse tree produced by laParser#cmdRetorne.
    def exitCmdRetorne(self, ctx:laParser.CmdRetorneContext):
        pass


    # Enter a parse tree produced by laParser#selecao.
    def enterSelecao(self, ctx:laParser.SelecaoContext):
        pass

    # Exit a parse tree produced by laParser#selecao.
    def exitSelecao(self, ctx:laParser.SelecaoContext):
        pass


    # Enter a parse tree produced by laParser#item_selecao.
    def enterItem_selecao(self, ctx:laParser.Item_selecaoContext):
        pass

    # Exit a parse tree produced by laParser#item_selecao.
    def exitItem_selecao(self, ctx:laParser.Item_selecaoContext):
        pass


    # Enter a parse tree produced by laParser#constantes.
    def enterConstantes(self, ctx:laParser.ConstantesContext):
        pass

    # Exit a parse tree produced by laParser#constantes.
    def exitConstantes(self, ctx:laParser.ConstantesContext):
        pass


    # Enter a parse tree produced by laParser#numero_intervalo.
    def enterNumero_intervalo(self, ctx:laParser.Numero_intervaloContext):
        pass

    # Exit a parse tree produced by laParser#numero_intervalo.
    def exitNumero_intervalo(self, ctx:laParser.Numero_intervaloContext):
        pass


    # Enter a parse tree produced by laParser#op_unario.
    def enterOp_unario(self, ctx:laParser.Op_unarioContext):
        pass

    # Exit a parse tree produced by laParser#op_unario.
    def exitOp_unario(self, ctx:laParser.Op_unarioContext):
        pass


    # Enter a parse tree produced by laParser#exp_aritmetica.
    def enterExp_aritmetica(self, ctx:laParser.Exp_aritmeticaContext):
        pass

    # Exit a parse tree produced by laParser#exp_aritmetica.
    def exitExp_aritmetica(self, ctx:laParser.Exp_aritmeticaContext):
        pass


    # Enter a parse tree produced by laParser#termo.
    def enterTermo(self, ctx:laParser.TermoContext):
        pass

    # Exit a parse tree produced by laParser#termo.
    def exitTermo(self, ctx:laParser.TermoContext):
        pass


    # Enter a parse tree produced by laParser#fator.
    def enterFator(self, ctx:laParser.FatorContext):
        pass

    # Exit a parse tree produced by laParser#fator.
    def exitFator(self, ctx:laParser.FatorContext):
        pass


    # Enter a parse tree produced by laParser#op1.
    def enterOp1(self, ctx:laParser.Op1Context):
        pass

    # Exit a parse tree produced by laParser#op1.
    def exitOp1(self, ctx:laParser.Op1Context):
        pass


    # Enter a parse tree produced by laParser#op2.
    def enterOp2(self, ctx:laParser.Op2Context):
        pass

    # Exit a parse tree produced by laParser#op2.
    def exitOp2(self, ctx:laParser.Op2Context):
        pass


    # Enter a parse tree produced by laParser#op3.
    def enterOp3(self, ctx:laParser.Op3Context):
        pass

    # Exit a parse tree produced by laParser#op3.
    def exitOp3(self, ctx:laParser.Op3Context):
        pass


    # Enter a parse tree produced by laParser#parcela.
    def enterParcela(self, ctx:laParser.ParcelaContext):
        pass

    # Exit a parse tree produced by laParser#parcela.
    def exitParcela(self, ctx:laParser.ParcelaContext):
        pass


    # Enter a parse tree produced by laParser#parcela_unario.
    def enterParcela_unario(self, ctx:laParser.Parcela_unarioContext):
        pass

    # Exit a parse tree produced by laParser#parcela_unario.
    def exitParcela_unario(self, ctx:laParser.Parcela_unarioContext):
        pass


    # Enter a parse tree produced by laParser#parcela_nao_unario.
    def enterParcela_nao_unario(self, ctx:laParser.Parcela_nao_unarioContext):
        pass

    # Exit a parse tree produced by laParser#parcela_nao_unario.
    def exitParcela_nao_unario(self, ctx:laParser.Parcela_nao_unarioContext):
        pass


    # Enter a parse tree produced by laParser#exp_relacional.
    def enterExp_relacional(self, ctx:laParser.Exp_relacionalContext):
        pass

    # Exit a parse tree produced by laParser#exp_relacional.
    def exitExp_relacional(self, ctx:laParser.Exp_relacionalContext):
        pass


    # Enter a parse tree produced by laParser#op_relacional.
    def enterOp_relacional(self, ctx:laParser.Op_relacionalContext):
        pass

    # Exit a parse tree produced by laParser#op_relacional.
    def exitOp_relacional(self, ctx:laParser.Op_relacionalContext):
        pass


    # Enter a parse tree produced by laParser#expressao.
    def enterExpressao(self, ctx:laParser.ExpressaoContext):
        pass

    # Exit a parse tree produced by laParser#expressao.
    def exitExpressao(self, ctx:laParser.ExpressaoContext):
        pass


    # Enter a parse tree produced by laParser#termo_logico.
    def enterTermo_logico(self, ctx:laParser.Termo_logicoContext):
        pass

    # Exit a parse tree produced by laParser#termo_logico.
    def exitTermo_logico(self, ctx:laParser.Termo_logicoContext):
        pass


    # Enter a parse tree produced by laParser#fator_logico.
    def enterFator_logico(self, ctx:laParser.Fator_logicoContext):
        pass

    # Exit a parse tree produced by laParser#fator_logico.
    def exitFator_logico(self, ctx:laParser.Fator_logicoContext):
        pass


    # Enter a parse tree produced by laParser#parcela_logica.
    def enterParcela_logica(self, ctx:laParser.Parcela_logicaContext):
        pass

    # Exit a parse tree produced by laParser#parcela_logica.
    def exitParcela_logica(self, ctx:laParser.Parcela_logicaContext):
        pass


    # Enter a parse tree produced by laParser#op_logico_1.
    def enterOp_logico_1(self, ctx:laParser.Op_logico_1Context):
        pass

    # Exit a parse tree produced by laParser#op_logico_1.
    def exitOp_logico_1(self, ctx:laParser.Op_logico_1Context):
        pass


    # Enter a parse tree produced by laParser#op_logico_2.
    def enterOp_logico_2(self, ctx:laParser.Op_logico_2Context):
        pass

    # Exit a parse tree produced by laParser#op_logico_2.
    def exitOp_logico_2(self, ctx:laParser.Op_logico_2Context):
        pass


