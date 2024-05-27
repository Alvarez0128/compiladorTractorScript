import ply.yacc as yacc
from Analizador_Lexico import construir_analizador_lexico, obtener_errores_lexico, reiniciar_analizador_lexico, tokens
from SymbolTable import Symbol, SymbolTable
from Analizador_Sintactico import construir_analizador_sintactico, NodoPara

# Función para generar el código intermedio a partir del AST
def generar_codigo_intermedio(node):
    codigo_intermedio = []
    
    def recorrer_arbol(node, indent_level=0):
        indent = "    " * indent_level
        if isinstance(node, tuple):
            if node[0] == 'programa':
                recorrer_arbol(node[1], indent_level)
            elif node[0] == 'bloque_codigo':
                codigo_intermedio.append(indent + "{")
                for decl in node[1]:
                    recorrer_arbol(decl, indent_level + 1)
                codigo_intermedio.append(indent + "}")
            elif node[0] == 'declaracion':
                if len(node) == 4:
                    tipo, ident, valor = node[1], node[2], node[3]
                    codigo_intermedio.append(f"{indent}{tipo} {ident} = {valor};")
                else:
                    recorrer_arbol(node[1], indent_level)
            elif node[0] == 'si':
                condicion, bloque = node[1], node[2]
                codigo_intermedio.append(f"{indent}IF ({condicion})")
                recorrer_arbol(bloque, indent_level + 1)
            elif node[0] == 'si_no':
                condicion, bloque = node[1], node[2]
                codigo_intermedio.append(f"{indent}IF (NOT {condicion})")
                recorrer_arbol(bloque, indent_level + 1)
            elif node[0] == 'mientras':
                condicion, bloque = node[1], node[2]
                codigo_intermedio.append(f"{indent}WHILE ({condicion})")
                recorrer_arbol(bloque, indent_level + 1)
            elif node[0] == 'expresion':
                izq, op, der = node[1], node[2], node[3]
                codigo_intermedio.append(f"{indent}{izq} {op} {der}")
            elif node[0] == 'grupo':
                recorrer_arbol(node[1], indent_level)
            elif node[0] == 'mostrar_en_pantalla':
                expresion = node[1]
                codigo_intermedio.append(f"{indent}PRINT({expresion});")
            elif node[0] == 'obstaculo_detectado':
                codigo_intermedio.append(f"{indent}OBSTACLE_DETECTED();")
        elif isinstance(node, NodoPara):
            tipo, ident, inicio, condicion, incremento, bloque = node.tipo, node.identificador, node.inicio, node.condicion, node.incremento, node.bloque
            codigo_intermedio.append(f"{indent}FOR ({tipo} {ident} = {inicio}; {condicion}; {incremento})")
            recorrer_arbol(bloque, indent_level + 1)
    
    recorrer_arbol(node)
    return codigo_intermedio

# Función para exportar el código intermedio a una cadena de texto formateada
def exportar_codigo_a_texto(codigo_intermedio):
    return "\n".join(codigo_intermedio)

######################################################ZONA PARA PRUEBAS
# DESCOMENTA CON Ctrl+k+u TODAS LAS LINEAS DE ABAJO PARA PROBAR ESTE ARCHIVO DE MANERA AISLADA

# # Probar el código de ejemplo
# test_code = """
# COMENZAR{

# BOOL obstaculo_detectado = falso;
# DECIMAL distancia_objetivo = 500.0;

# MIENTRAS(distancia_recorrida < distancia_objetivo){
#     SI(obstaculo_detectado){
#         SI(CALCULAR_DISTANCIA_RESTANTE(distancia_objetivo) < 100){
#             DETENER_MOTOR();
#             SONAR_ALARMA();
#             ESPERAR(5); // Espera 5 segundos antes de reanudar
#             ACTIVAR_FRENO();
#             ESPERAR(2); // Espera 2 segundos con los frenos activados
#             obstaculo_detectado = Falso; // Reinicia la detección de obstáculos
#         }SINO{
#             AJUSTAR_VELOCIDAD(20); // Reducir la velocidad para evitar el obstáculo
#         }
#     }SINO{
#         SI(VERIFICAR_SENSOR_OBSTACULOS()){
#             obstaculo_detectado = Verdadero;
#         }SINO{
#             AJUSTAR_VELOCIDAD(50); // Mantener velocidad constante
#         }
#     }
#     // Simulación de movimiento del tractor
#     distancia_recorrida = distancia_recorrida + velocidad * tiempo_transcurrido;
# }

# }TERMINAR
# """

# # Construir los analizadores
# lexer = construir_analizador_lexico()
# parser = construir_analizador_sintactico()

# # Realizar el análisis léxico y sintáctico
# lexer.input(test_code)
# tokens_analisis = [token for token in lexer]
# reiniciar_analizador_lexico(lexer)

# # Obtener el AST
# ast = parser.parse(test_code)

# # Generar el código intermedio
# codigo_intermedio = generar_codigo_intermedio(ast)

# # Exportar el código intermedio a una cadena de texto formateada
# codigo_intermedio_texto = exportar_codigo_a_texto(codigo_intermedio)

# # Imprimir el código intermedio formateado
# print(codigo_intermedio_texto)
