import ply.yacc as yacc
from Analizador_Lexico import construir_analizador_lexico, obtener_errores_lexico, reiniciar_analizador_lexico, tokens
from SymbolTable import Symbol, SymbolTable
from Analizador_Sintactico import construir_analizador_sintactico, NodoPara

def generar_codigo_optimizado(node):
    triplos = []
    temp_counter = 0

    def nuevo_temporal():
        nonlocal temp_counter
        temp_name = f"t{temp_counter}"
        temp_counter += 1
        return temp_name

    def recorrer_arbol(node):
        if isinstance(node, tuple):
            if node[0] == 'programa':
                recorrer_arbol(node[1])
            elif node[0] == 'bloque_codigo':
                for decl in node[1]:
                    recorrer_arbol(decl)
            elif node[0] == 'declaracion':
                if len(node) == 4:
                    tipo, ident, valor = node[1], node[2], node[3]
                    temp = generar_expresion(valor)
                    triplos.append(('=', temp, ident))
            elif node[0] == 'si':
                condicion, bloque = node[1], node[2]
                temp = generar_expresion(condicion)
                etiqueta_si = nuevo_temporal()
                triplos.append(('IF', temp, etiqueta_si))
                recorrer_arbol(bloque)
                triplos.append((etiqueta_si, 'GOTO', ''))
            elif node[0] == 'sino':
                etiqueta_sino = nuevo_temporal()
                triplos.append(('ELSE', '', etiqueta_sino))
                recorrer_arbol(node[1])
                triplos.append((etiqueta_sino, 'GOTO', ''))
            elif node[0] == 'si_no':
                condicion, bloque = node[1], node[2]
                temp = generar_expresion(condicion)
                etiqueta_si_no = nuevo_temporal()
                triplos.append(('IF', temp, etiqueta_si_no))
                recorrer_arbol(bloque)
                triplos.append((etiqueta_si_no, 'GOTO', ''))
            elif node[0] == 'mientras':
                condicion, bloque = node[1], node[2]
                etiqueta_mientras = nuevo_temporal()
                triplos.append((etiqueta_mientras, 'WHILE', ''))
                temp = generar_expresion(condicion)
                triplos.append(('IF', temp, etiqueta_mientras))
                recorrer_arbol(bloque)
                triplos.append((etiqueta_mientras, 'GOTO', ''))
            elif node[0] == 'expresion':
                izq, op, der = node[1], node[2], node[3]
                temp1 = generar_expresion(izq)
                temp2 = generar_expresion(der)
                temp_result = nuevo_temporal()
                triplos.append((op, temp1, temp2, temp_result))
                return temp_result
            elif node[0] == 'grupo':
                return generar_expresion(node[1])
        elif isinstance(node, NodoPara):
            tipo, ident, inicio, condicion, incremento, bloque = node.tipo, node.identificador, node.inicio, node.condicion, node.incremento, node.bloque
            temp_inicio = generar_expresion(inicio)
            triplos.append(('=', temp_inicio, ident))
            etiqueta_para = nuevo_temporal()
            temp_cond = generar_expresion(condicion)
            triplos.append(('IF', temp_cond, etiqueta_para))
            recorrer_arbol(bloque)
            temp_incr = generar_expresion(incremento)
            triplos.append(('+', ident, temp_incr, ident))
            triplos.append((etiqueta_para, 'GOTO', ''))

    def generar_expresion(exp):
        if isinstance(exp, tuple):
            if exp[0] == 'expresion':
                izq, op, der = exp[1], exp[2], exp[3]
                temp1 = generar_expresion(izq)
                temp2 = generar_expresion(der)
                temp_result = nuevo_temporal()
                triplos.append((op, temp1, temp2, temp_result))
                return temp_result
            elif exp[0] == 'grupo':
                return generar_expresion(exp[1])
        return str(exp)

    recorrer_arbol(node)
    return triplos
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

# # Optimizar el código intermedio
# codigo_optimizado = optimizar_codigo_intermedio(codigo_intermedio)

# # Exportar el código optimizado a una cadena de texto formateada
# codigo_optimizado_texto = exportar_codigo_a_texto(codigo_optimizado)

# # Imprimir el código optimizado formateado
# print(codigo_optimizado_texto)
