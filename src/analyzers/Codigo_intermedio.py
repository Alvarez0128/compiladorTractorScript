# Importar los analizadores y la tabla de símbolos
from Analizador_Lexico import construir_analizador_lexico, reiniciar_analizador_lexico
from Analizador_Sintactico import construir_analizador_sintactico, NodoPara
from SymbolTable import SymbolTable, Symbol
import Analizador_Semantico as sem

def analizar_codigo(input_code):
    # Construir analizadores léxico y sintáctico
    lexer = construir_analizador_lexico()
    parser = construir_analizador_sintactico()
    
    # Reiniciar analizadores
    reiniciar_analizador_lexico(lexer)
    
    # Realizar el análisis léxico
    lexer.input(input_code)
    tokens = list(lexer)
    
    # Realizar el análisis sintáctico
    ast = parser.parse(input_code, lexer=lexer)
    
    return tokens, ast

def verificar_semantica(ast, symbol_table):
    try:
        # Aquí se realizarían las verificaciones semánticas necesarias
        # Por ejemplo, verificar asignaciones, expresiones, estructuras de control, etc.
        sem.check_expression(symbol_table, ast)
    except Exception as e:
        print(f"Error semántico: {e}")

def generar_codigo_intermedio(ast, symbol_table):
    codigo_intermedio = []

    def recorrer_ast(node):
        if isinstance(node, tuple):
            if node[0] == 'declaracion':
                # Procesar una declaración
                tipo, identificador, valor = node[1], node[2], node[3]
                simbolo = Symbol(name=identificador, category='variable', symbol_type=tipo, attributes={'value': valor})
                symbol_table.add(simbolo)
                codigo_intermedio.append(f"{tipo} {identificador} = {valor};")
            elif node[0] == 'mostrar_en_pantalla':
                # Procesar una instrucción de mostrar en pantalla
                valor = node[1]
                codigo_intermedio.append(f"Serial.println({valor});")
            elif node[0] == 'si':
                # Procesar una estructura condicional
                condicion, bloque = node[1], node[2]
                codigo_intermedio.append(f"if ({condicion}) {{")
                recorrer_ast(bloque)
                codigo_intermedio.append("}")
            elif node[0] == 'mientras':
                # Procesar un bucle mientras
                condicion, bloque = node[1], node[2]
                codigo_intermedio.append(f"while ({condicion}) {{")
                recorrer_ast(bloque)
                codigo_intermedio.append("}")
            else:
                # Procesar otros nodos
                for child in node:
                    recorrer_ast(child)
        elif isinstance(node, NodoPara):
            # Procesar un bucle para
            codigo_intermedio.append(f"for ({node.tipo} {node.identificador} = {node.inicio}; {node.condicion}; {node.incremento}) {{")
            recorrer_ast(node.bloque)
            codigo_intermedio.append("}")
        elif isinstance(node, list):
            # Procesar una lista de nodos
            for item in node:
                recorrer_ast(item)
    
    recorrer_ast(ast)
    return codigo_intermedio

def generar_codigo_arduino(codigo_intermedio):
    codigo_arduino = []
    # Código de inicialización (setup)
    setup_code = ["void setup() {", "Serial.begin(9600);", "}"]
    # Código principal del loop
    loop_code = ["void loop() {"]

    for linea in codigo_intermedio:
        loop_code.append(f"  {linea}")

    loop_code.append("}")

    # Combinar el código de setup y loop
    codigo_arduino.extend(setup_code)
    codigo_arduino.extend(loop_code)
    return codigo_arduino

def compilar_codigo(input_code):
    symbol_table = SymbolTable()
    tokens, ast = analizar_codigo(input_code)
    verificar_semantica(ast, symbol_table)
    codigo_intermedio = generar_codigo_intermedio(ast, symbol_table)
    codigo_arduino = generar_codigo_arduino(codigo_intermedio)
    return codigo_arduino

if __name__ == "__main__":
    # Ejemplo de código fuente
    codigo_fuente = """
    COMENZAR{
        ENTERO x = 0;
        MOSTRAR_EN_PANTALLA(x);
    }TERMINAR
    """
    
    # Compilar el código fuente a código Arduino
    codigo_arduino = compilar_codigo(codigo_fuente)
    # Imprimir el código Arduino generado
    print("\n".join(codigo_arduino))
