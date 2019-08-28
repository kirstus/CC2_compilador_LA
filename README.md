#Compilador linguagem LA

Instalar o ANTLR4 (https://www.antlr.org/)
Em particular para linux:
$ cd /usr/local/lib
$ wget https://www.antlr.org/download/antlr-4.7.2-complete.jar
$ export CLASSPATH=".:/usr/local/lib/antlr-4.7.2-complete.jar:$CLASSPATH"
$ alias antlr4='java -jar /usr/local/lib/antlr-4.7.2-complete.jar'
$ alias grun='java org.antlr.v4.gui.TestRig'

Para gerar os arquivos necessários a partir da gramática:
$ antlr4 -Dlanguage=Python3 -visitor

Para rodar um caso de teste:
$ python laCompiler.py caminho_do_teste caminho_da_saida

Para rodar o corretor automático:
$ java -jar CorretorTrabalho1.jar "python /home/matt/ufscar/CC2/T1/compilador_LA/laCompiler.py" "gcc" /tmp/ccc/ /home/matt/ufscar/CC2/T1/casosDeTesteT1/ "RAs" sintatico

