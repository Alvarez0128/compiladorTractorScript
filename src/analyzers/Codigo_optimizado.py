import ply.yacc as yacc
from Analizador_Lexico import construir_analizador_lexico, obtener_errores_lexico, reiniciar_analizador_lexico, tokens
from SymbolTable import Symbol, SymbolTable
from Analizador_Sintactico import construir_analizador_sintactico, NodoPara
from Codigo_intermedio import generar_codigo_intermedio, exportar_codigo_a_texto

def optimizar_codigo_intermedio(codigo_intermedio):
    codigo_optimizado = []
    
    def optimizar_linea(linea):
        # Eliminación de instrucciones redundantes
        if linea in codigo_optimizado:
            return None
        # Simplificación de expresiones constantes
        if " = " in linea and ";" in linea:
            partes = linea.split(" = ")
            if len(partes) == 2:
                izq = partes[0].strip()
                der = partes[1].strip().rstrip(';')
                try:
                    valor = eval(der)
                    linea = f"{izq} = {valor};"
                except:
                    pass
        return linea

    for linea in codigo_intermedio:
        linea_optimizada = optimizar_linea(linea)
        if linea_optimizada:
            codigo_optimizado.append(linea_optimizada)

    return codigo_optimizado

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
