grammar la;

programa: declaracoes 'algoritmo' corpo 'fim_algoritmo';

declaracoes: decl_local_global declaracoes |;

decl_local_global: declaracao_local | declaracao_global;

declaracao_local: 'declare' variavel 
				| 'constante' IDENT ':' tipo_basico '=' valor_constante
				| 'tipo' IDENT ':' tipo;
variasDeclaracoesLocais: declaracao_local variasDeclaracoesLocais |;

variavel: IDENT dimensao maisVariaveis ':' tipo;
maisVariaveis: ',' IDENT dimensao maisVariaveis |;

identificador: circunflexoOpcional IDENT dimensao maisIdentificadores;
maisIdentificadores: '.' identificador |;
maisIdentificadoresVirgula: ',' identificador maisIdentificadoresVirgula |;

dimensao: '[' exp_aritmetica ']' dimensao |;

tipo: registro | tipo_estendido;

tipo_basico: 'literal' | 'inteiro' | 'real' | 'logico';
tipo_basico_ident: tipo_basico | IDENT;

tipo_estendido: circunflexoOpcional tipo_basico_ident;

valor_constante: CADEIA | NUM_INT | NUM_REAL | 'verdadeiro' | 'falso';

registro: 'registro' variavel maisVariaveis 'fim_registro';

declaracao_global: 'procedimento' IDENT '(' parametroOpcional ')' variasDeclaracoesLocais variosComandos 'fim_procedimento'
				 | 'funcao' IDENT '(' parametroOpcional ')' ':' tipo_estendido variasDeclaracoesLocais variosComandos 'fim_funcao';

parametro: varOpcional identificador maisIdentificadoresVirgula ':' tipo_estendido maisParametros;
parametroOpcional: parametro |;
maisParametros: ',' parametro |;

corpo: variasDeclaracoesLocais variosComandos;

variosComandos: cmd variosComandos |;
cmd: cmdLeia | cmdEscreva | cmdSe | cmdCaso | cmdPara | cmdEnquanto | cmdFaca | cmdAtribuicao | cmdChamada | cmdRetorne;
cmdLeia: 'leia' '(' lerComando ')';
lerComando: circunflexoOpcional identificador lerMaisComandos;
lerMaisComandos: ',' lerComando |;
cmdEscreva: 'escreva' '(' expressao maisExpressoes ')';
cmdSe: 'se' expressao 'entao' variosComandos senaoComandosOpcional 'fim_se';
cmdCaso: 'caso' exp_aritmetica 'seja' selecao senaoComandosOpcional 'fim_caso';
cmdPara: 'para' IDENT '<-' exp_aritmetica 'ate' exp_aritmetica 'faca' variosComandos 'fim_para';
cmdEnquanto: 'enquanto' expressao 'faca' variosComandos 'fim_enquanto';
cmdFaca: 'faca' variosComandos 'ate' expressao;
cmdAtribuicao: circunflexoOpcional identificador '<-' expressao;
cmdChamada: IDENT '(' expressao maisExpressoes ')';
cmdRetorne: 'retorne' expressao;

selecao: constantes ':' variosComandos maisSelecoes;
maisSelecoes: selecao |;

constantes: numero_intervalo maisConstantes;
maisConstantes: ',' constantes |;

numero_intervalo: op_unario NUM_INT intervaloNumericoOpcional;
intervaloNumericoOpcional: '..' op_unario NUM_INT |;

op_unario: '-' |;

exp_aritmetica: termo maisTermos;

termo: fator maisFatores;
maisTermos: op1 termo maisTermos |;

fator: parcela maisParcelas;
maisFatores: op2 fator maisFatores |;

parcela: op_unario parcela_unario | parcela_nao_unario;
maisParcelas: op3 parcela maisParcelas |;

parcela_unario: '^' IDENT maisIdentificadores dimensao
			  | IDENT '(' expressao maisExpressoes ')'
			  | NUM_INT
			  | NUM_REAL
			  | '(' expressao ')';

parcela_nao_unario: '&' IDENT maisIdentificadores dimensao | CADEIA;

op1: '+' | '-';
op2: '*' | '/';
op3: '%';

exp_relacional: exp_aritmetica exp_opcional;
exp_opcional: op_relacional exp_aritmetica |;

op_relacional: '=' | '<>' | '>=' | '<=' | '>' | '<';
			  
expressao: termo_logico maisTermosLogicos;
maisExpressoes: ',' expressao maisExpressoes|;

termo_logico: fator_logico maisFatoresLogicos;
maisTermosLogicos: op_logico_1 termo_logico maisTermosLogicos |;

fator_logico: naoOpcional parcela_logica;
maisFatoresLogicos: op_logico_2 fator_logico maisFatoresLogicos |;

parcela_logica: ('verdadeiro' | 'falso')
				| exp_relacional;
op_logico_1: 'ou';
op_logico_2: 'e';

NUM_INT: [0-9]+;
NUM_REAL: [0-9]+'.'[0-9]+;

circunflexoOpcional: '^' circunflexoOpcional |;
varOpcional: 'var' |;
senaoComandosOpcional: 'senao' variosComandos |;
naoOpcional: 'nao' |;
IDENT: ([a-zA-Z] | '_')( [a-zA-Z] | [0-9] | '_')*;

CADEIA: '"' ~('"')* '"';

WHITE_SPACE:   ( '\t' | ' ' | '\r' | '\n' )+ -> skip;

COMMENTS: '{' ~('}')* '}' -> skip;

ErrorChar: .;