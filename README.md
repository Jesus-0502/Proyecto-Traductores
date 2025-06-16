# Proyecto Traductores
#### Elaborado por: Jesus Gutierrez 20-10332 | Mauricio Fragachan 20-10265
El siguiente proyecto tiene como objetivo construir un traductor para un lenguaje imperativo definido en `proyecto.pdf`. Para ello, se dividió el proceso en cuatro etapas que se explican a continuacion: 

## Etapa 1
Esta entrega consiste en la implementación de un analizador lexicográfico para el lenguaje imperativo definido en el enunciado del proyecto. Dicho analizador está implementado en `lexer.py` utilizando la libreria `PLY` de Python.

##### Ejecución:
```bash
python3 lexer.py <archivo.imperat>
```


## Etapa 2
Esta entrega consiste en diseñar una gramática libre de contexto para el lenguaje imperativo y utilizarla para implementar un reconocedor sintáctico. Dicho reconocedor construye el árbol
sintáctico abstracto del programa reconocido e imprimirlo de forma legible por la pantalla.
La gramática está detallada en `gramatica.txt` y el reconocedor en `parser.py`.

##### Ejecución:
```bash
 python3 parser.py <archivo.imperat>
 ```