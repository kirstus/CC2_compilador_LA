grammar la;

programa: declaracoes 'algoritmo' corpo 'fim_algoritmo';

declaracoes: decl_local_global*;

decl_local_global: declaracao_local | declaracao_global;

declaracao_local: 'declare' variavel 
				| 'constante' IDENT ':' tipo_basico '=' valor_constante
				| 'tipo' IDENT ':' tipo
				;

variavel: primID=identificador (',' maisID+=identificador)* ':' tipo;
identificador: primID=IDENT ('.' maisID+=IDENT)* dimensao;
dimensao: ('[' exp_aritmetica ']')*;

tipo: registro | tipo_estendido;

tipo_basico: 'literal' | 'inteiro' | 'real' | 'logico';
tipo_basico_ident: tipo_basico | IDENT;

tipo_estendido: ('^')? tipo_basico_ident;

valor_constante: CADEIA | NUM_INT | NUM_REAL | 'verdadeiro' | 'falso';

registro: 'registro' (variavel)* 'fim_registro';

declaracao_global: 'procedimento' IDENT '(' (parametros)? ')' (declaracao_local)* (cmd)* 'fim_procedimento'
				 | 'funcao' IDENT '(' (parametros)? ')' ':' tipo_estendido (declaracao_local)* (cmd)* 'fim_funcao';

parametro: ('var')? primID=identificador (',' maisID+=identificador)* ':' tipo_estendido;
parametros: param=parametro (',' maisParam+=parametro)*;

corpo: (declaracao_local)* (cmd)*;

cmd: cmdLeia | cmdEscreva | cmdSe | cmdCaso | cmdPara | cmdEnquanto | cmdFaca | cmdAtribuicao | cmdChamada | cmdRetorne;
cmdLeia: 'leia' '(' ('^')? primID=identificador (',' ('^')? maisID+=identificador)* ')';
cmdEscreva: 'escreva' '(' expr=expressao (',' naisExpr+=expressao)* ')';
cmdSe: 'se' expressao 'entao' (comandos+=cmd)* ('senao' (maisComandos+=cmd)*)? 'fim_se';
cmdCaso: 'caso' exp_aritmetica 'seja' selecao ('senao' (cmd)*)? 'fim_caso';
cmdPara: 'para' IDENT '<-' exp_aritmetica 'ate' exp_aritmetica 'faca' (cmd)* 'fim_para';
cmdEnquanto: 'enquanto' expressao 'faca' (cmd)* 'fim_enquanto';
cmdFaca: 'faca' (cmd)* 'ate' expressao;
cmdAtribuicao: ('^')? identificador '<-' expressao;
cmdChamada: IDENT '(' expr=expressao (',' maisExpr+=expressao)* ')';
cmdRetorne: 'retorne' expressao;

selecao: (item_selecao)+;
item_selecao: constantes ':' (cmd)*;

constantes: ni=numero_intervalo (',' maisNI+=numero_intervalo)*;

numero_intervalo: (op_unario)? primNum=NUM_INT ('..'(op_unario)? segNum=NUM_INT)?;

op_unario: '-';

exp_aritmetica: primTermo=termo (op1 maisTermos+=termo)*;
termo: primFator=fator (op2 maisFatores+=fator)*;
fator: primParcela=parcela (op3 maisParcelas+=parcela)*;
op1: '+' | '-';
op2: '*' | '/';
op3: '%';

parcela: (op_unario)? parcela_unario | parcela_nao_unario;

parcela_unario: ('^')? identificador
			  | IDENT '(' expr=expressao (',' maisExpr+=expressao)* ')'
			  | NUM_INT
			  | NUM_REAL
			  | '(' outraExpr=expressao ')';

parcela_nao_unario: '&' identificador | CADEIA;

exp_relacional: exp_aritmetica (op_relacional exp_aritmetica)?;

op_relacional: '=' | '<>' | '>=' | '<=' | '>' | '<';
			  
expressao: termoLog=termo_logico (op_logico_1 maisTermoLog+=fator_logico)*;
termo_logico: fatLog=fator_logico (op_logico_2 maisFatLog+=fator_logico)*;
fator_logico: ('nao')? parcela_logica;
parcela_logica: ('verdadeiro' | 'falso')
				| exp_relacional;
op_logico_1: 'ou';
op_logico_2: 'e';

NUM_INT: [0-9]+;
NUM_REAL: [0-9]+'.'[0-9]+;

IDENT: ([a-zA-Z] | '_')( [a-zA-Z] | [0-9] | '_')*;

CADEIA: '"' ~('"')* '"';

WHITE_SPACE:   ( '\t' | ' ' | '\r' | '\n' )+ -> skip;

COMMENTS: '{' ~('}')* '}' -> skip;

ErrorChar: .;