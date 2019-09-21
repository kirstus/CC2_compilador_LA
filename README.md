# Compilador linguagem LA

Instalar o [ANTLR4](https://www.antlr.org/)

Em particular para linux:
```
$ cd /usr/local/lib
$ wget https://www.antlr.org/download/antlr-4.7.2-complete.jar
$ export CLASSPATH=".:/usr/local/lib/antlr-4.7.2-complete.jar:$CLASSPATH"
$ alias antlr4='java -jar /usr/local/lib/antlr-4.7.2-complete.jar'
$ alias grun='java org.antlr.v4.gui.TestRig'
```
Para usar o ANTLR4 com python3:
`pip install antlr4-python3-runtime`

Para gerar os arquivos necessários a partir da gramática:
`$ antlr4 -Dlanguage=Python3 -visitor la`

Para rodar um caso de teste:
`$ python laCompiler.py caminho_do_teste caminho_da_saida`

Para rodar o corretor automático:

`$ java -jar CorretorTrabalho1.jar "python /caminho/do/compilador_LA/laCompiler.py" "gcc" /caminho/da/pasta/de/saida/ /caminho/dos/casosDeTesteT1/ "RAs" tudo`

