import ply.yacc as yacc
from Analizador_Lexico import construir_analizador_lexico, obtener_errores_lexico, reiniciar_analizador_lexico, tokens
from SymbolTable import Symbol, SymbolTable
from Analizador_Sintactico import construir_analizador_sintactico, NodoPara

# Función para generar el código intermedio a partir del AST
def generar_codigo_intermedio(node):
    codigo_intermedio = []
    
    def recorrer_arbol(node):
        if isinstance(node, tuple):
            if node[0] == 'programa':
                recorrer_arbol(node[1])
            elif node[0] == 'bloque_codigo':
                codigo_intermedio.append("{")
                for decl in node[1]:
                    recorrer_arbol(decl)
                codigo_intermedio.append("}")
            elif node[0] == 'declaracion':
                if len(node) == 4:
                    tipo, ident, valor = node[1], node[2], node[3]
                    codigo_intermedio.append(f"{tipo} {ident} = {valor};")
                else:
                    recorrer_arbol(node[1])
            elif node[0] == 'si':
                condicion, bloque = node[1], node[2]
                codigo_intermedio.append(f"IF ({condicion})")
                recorrer_arbol(bloque)
            elif node[0] == 'si_no':
                condicion, bloque = node[1], node[2]
                codigo_intermedio.append(f"IF (NOT {condicion})")
                recorrer_arbol(bloque)
            elif node[0] == 'mientras':
                condicion, bloque = node[1], node[2]
                codigo_intermedio.append(f"WHILE ({condicion})")
                recorrer_arbol(bloque)
            elif node[0] == 'expresion':
                izq, op, der = node[1], node[2], node[3]
                codigo_intermedio.append(f"{izq} {op} {der}")
            elif node[0] == 'grupo':
                recorrer_arbol(node[1])
            elif node[0] == 'mostrar_en_pantalla':
                expresion = node[1]
                codigo_intermedio.append(f"PRINT({expresion});")
            elif node[0] == 'obstaculo_detectado':
                codigo_intermedio.append("OBSTACLE_DETECTED();")
        elif isinstance(node, NodoPara):
            tipo, ident, inicio, condicion, incremento, bloque = node.tipo, node.identificador, node.inicio, node.condicion, node.incremento, node.bloque
            codigo_intermedio.append(f"FOR ({tipo} {ident} = {inicio}; {condicion}; {incremento})")
            recorrer_arbol(bloque)
    
    recorrer_arbol(node)
    return codigo_intermedio

# Probar el código de ejemplo
test_code = """
COMENZAR{

BOOL obstaculo_detectado = falso;
DECIMAL distancia_objetivo = 500.0;

MIENTRAS(distancia_recorrida < distancia_objetivo){
    SI(obstaculo_detectado){
        SI(CALCULAR_DISTANCIA_RESTANTE(distancia_objetivo) < 100){
            DETENER_MOTOR();
            SONAR_ALARMA();
            ESPERAR(5); // Espera 5 segundos antes de reanudar
            ACTIVAR_FRENO();
            ESPERAR(2); // Espera 2 segundos con los frenos activados
            obstaculo_detectado = Falso; // Reinicia la detección de obstáculos
        }SINO{
            AJUSTAR_VELOCIDAD(20); // Reducir la velocidad para evitar el obstáculo
        }
    }SINO{
        SI(VERIFICAR_SENSOR_OBSTACULOS()){
            obstaculo_detectado = Verdadero;
        }SINO{
            AJUSTAR_VELOCIDAD(50); // Mantener velocidad constante
        }
    }
    // Simulación de movimiento del tractor
    distancia_recorrida = distancia_recorrida + velocidad * tiempo_transcurrido;
}

}TERMINAR
"""

# Construir los analizadores
lexer = construir_analizador_lexico()
parser = construir_analizador_sintactico()

# Realizar el análisis léxico y sintáctico
lexer.input(test_code)
tokens_analisis = [token for token in lexer]
reiniciar_analizador_lexico(lexer)

# Obtener el AST
ast = parser.parse(test_code)

# Generar el código intermedio
codigo_intermedio = generar_codigo_intermedio(ast)

# Imprimir el código intermedio
for linea in codigo_intermedio:
    print(linea)
