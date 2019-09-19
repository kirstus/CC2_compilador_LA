grammar la;

programa: declaracoes 'algoritmo' corpo 'fim_algoritmo';

declaracoes: decl_local_global declaracoes |;

decl_local_global: declaracao_local | declaracao_global;

declaracao_local: 'declare' variavel 
				| 'constante' IDENT ':' tipo_basico '=' valor_constante
				| 'tipo' IDENT ':' tipo;
variasDeclaracoesLocais: declaracao_local variasDeclaracoesLocais |;

variavel: identificador maisIdentificadoresVirgula ':' tipo;
variasVariaveis: variavel variasVariaveis |;

identificador: IDENT maisIdentificadores dimensao;
maisIdentificadores: '.' IDENT maisIdentificadores |;
maisIdentificadoresVirgula: ',' identificador maisIdentificadoresVirgula |;
dimensao: '[' exp_aritmetica ']' dimensao |;

tipo: registro | tipo_estendido;

tipo_basico: 'literal' | 'inteiro' | 'real' | 'logico';
tipo_basico_ident: tipo_basico | IDENT;

tipo_estendido: circunflexoOpcional tipo_basico_ident;

valor_constante: CADEIA | NUM_INT | NUM_REAL | 'verdadeiro' | 'falso';

registro: 'registro' variavel variasVariaveis 'fim_registro';

declaracao_global: 'procedimento' IDENT '(' (parametros)? ')' variasDeclaracoesLocais variosComandos 'fim_procedimento'
				 | 'funcao' IDENT '(' (parametros)? ')' ':' tipo_estendido variasDeclaracoesLocais variosComandos 'fim_funcao';

parametro: varOpcional identificador maisIdentificadoresVirgula ':' tipo_estendido;
parametros: parametro maisParametros;
maisParametros: ',' parametro maisParametros |;

corpo: variasDeclaracoesLocais (cmd)*;

variosComandos: cmd variosComandos |;
cmd: cmdLeia | cmdEscreva | cmdSe | cmdCaso | cmdPara | cmdEnquanto | cmdFaca | cmdAtribuicao | cmdChamada | cmdRetorne;
cmdLeia: 'leia' '(' circunflexoOpcional identificador cmdLeiaAtribuicao ')';
cmdLeiaAtribuicao: ',' circunflexoOpcional identificador cmdLeiaAtribuicao |;
cmdEscreva: 'escreva' '(' expressao (',' expressao)* ')';
cmdSe: 'se' expressao 'entao' variosComandos ('senao' variosComandos)? 'fim_se';
cmdCaso: 'caso' exp_aritmetica 'seja' selecao ('senao' variosComandos)? 'fim_caso';
cmdPara: 'para' IDENT '<-' exp_aritmetica 'ate' exp_aritmetica 'faca' variosComandos 'fim_para';
cmdEnquanto: 'enquanto' expressao 'faca' variosComandos 'fim_enquanto';
cmdFaca: 'faca' variosComandos 'ate' expressao;
cmdAtribuicao: circunflexoOpcional identificador '<-' expressao;
cmdChamada: IDENT '(' expressao (',' expressao)* ')';
cmdRetorne: 'retorne' expressao;

selecao: (item_selecao)+;
item_selecao: constantes ':' variosComandos;

constantes: numero_intervalo maisConstantes;
maisConstantes: ',' constantes |;

numero_intervalo: (op_unario)? NUM_INT ('..'(op_unario)? NUM_INT)?;

op_unario: '-';

exp_aritmetica: termo (op1 termo)*;
termo: fator (op2 fator)*;
fator: parcela (op3 parcela)*;
op1: '+' | '-';
op2: '*' | '/';
op3: '%';

parcela: (op_unario)? parcela_unario | parcela_nao_unario;

parcela_unario: circunflexoOpcional identificador
			  | IDENT '(' expressao (',' expressao)* ')'
			  | NUM_INT
			  | NUM_REAL
			  | '(' expressao ')';

parcela_nao_unario: '&' identificador | CADEIA;

exp_relacional: exp_aritmetica (op_relacional exp_aritmetica)?;

op_relacional: '=' | '<>' | '>=' | '<=' | '>' | '<';
			  
expressao: termo_logico (op_logico_1 fator_logico)*;
termo_logico: fator_logico (op_logico_2 fator_logico)*;
fator_logico: 'nao' parcela_logica | parcela_logica;
parcela_logica: ('verdadeiro' | 'falso')
				| exp_relacional;
op_logico_1: 'ou';
op_logico_2: 'e';

NUM_INT: [0-9]+;
NUM_REAL: [0-9]+'.'[0-9]+;

circunflexoOpcional: '^' |;
varOpcional: 'var' |;
IDENT: ([a-zA-Z] | '_')( [a-zA-Z] | [0-9] | '_')*;

CADEIA: '"' ~('"')* '"';

WHITE_SPACE:   ( '\t' | ' ' | '\r' | '\n' )+ -> skip;

COMMENTS: '{' ~('}')* '}' -> skip;

ErrorChar: .;