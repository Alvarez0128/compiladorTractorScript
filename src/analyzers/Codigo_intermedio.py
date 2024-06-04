from SymbolTable import Symbol, SymbolTable
from Analizador_Sintactico import construir_analizador_sintactico, NodoPara
from tripletas import GeneradorTripletas

generador_tripletas = GeneradorTripletas()

def generar_codigo_intermedio_triples(node):
    def nuevo_temp():
        return generador_tripletas.nueva_temporal()

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
                    generador_tripletas.agregar_tripleta('=', ident, valor)
                else:
                    recorrer_arbol(node[1])
            elif node[0] == 'si':
                condicion, bloque_si = node[1], node[2]
                temp_cond = recorrer_arbol(condicion)
                label_si = f"L{len(generador_tripletas.obtener_tripletas())+2}"
                label_end = f"L{len(generador_tripletas.obtener_tripletas())+3}"
                generador_tripletas.agregar_tripleta('IF', temp_cond, label_si)
                generador_tripletas.agregar_tripleta('GOTO', label_end, '')
                generador_tripletas.agregar_tripleta('LABEL', label_si, '')
                recorrer_arbol(bloque_si)
                generador_tripletas.agregar_tripleta('LABEL', label_end, '')
            elif node[0] == 'si_no':
                condicion, bloque_si, bloque_no = node[1], node[2], node[3]
                temp_cond = recorrer_arbol(condicion)
                label_si = f"L{len(generador_tripletas.obtener_tripletas())+2}"
                label_no = f"L{len(generador_tripletas.obtener_tripletas())+3}"
                label_end = f"L{len(generador_tripletas.obtener_tripletas())+4}"
                generador_tripletas.agregar_tripleta('IF', temp_cond, label_si)
                generador_tripletas.agregar_tripleta('GOTO', label_no, '')
                generador_tripletas.agregar_tripleta('LABEL', label_si, '')
                recorrer_arbol(bloque_si)
                generador_tripletas.agregar_tripleta('GOTO', label_end, '')
                generador_tripletas.agregar_tripleta('LABEL', label_no, '')
                recorrer_arbol(bloque_no)
                generador_tripletas.agregar_tripleta('LABEL', label_end, '')
            elif node[0] == 'mientras':
                condicion, bloque = node[1], node[2]
                start_label = f"L{len(generador_tripletas.obtener_tripletas())}"
                generador_tripletas.agregar_tripleta('LABEL', start_label, '')
                temp_cond = recorrer_arbol(condicion)
                end_label = f"L{len(generador_tripletas.obtener_tripletas())+2}"
                generador_tripletas.agregar_tripleta('WHILE', temp_cond, end_label)
                recorrer_arbol(bloque)
                generador_tripletas.agregar_tripleta('GOTO', start_label, '')
                generador_tripletas.agregar_tripleta('LABEL', end_label, '')
            elif node[0] == 'expresion':
                izq, op, der = node[1], node[2], node[3]
                temp_izq = recorrer_arbol(izq)
                temp_der = recorrer_arbol(der)
                temp_res = nuevo_temp()
                generador_tripletas.agregar_tripleta('=', temp_res, f"{temp_izq} {op} {temp_der}")
                return temp_res
            elif node[0] == 'condicion':
                izq, op, der = node[1], node[2], node[3]
                temp_izq = recorrer_arbol(izq)
                temp_der = recorrer_arbol(der)
                temp_res = nuevo_temp()
                generador_tripletas.agregar_tripleta('=', temp_res, f"{temp_izq} {op} {temp_der}")
                return temp_res
            else:
                for child in node:
                    recorrer_arbol(child)
        elif isinstance(node, str):
            return node

    recorrer_arbol(node)
    return generador_tripletas.obtener_tripletas()

def exportar_triples_a_texto(triples):
    return "\n".join(f"{i}: {triple}" for i, triple in enumerate(triples))

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
parser = construir_analizador_sintactico()

# Realizar el análisis léxico y sintáctico
ast = parser.parse(test_code)

# Generar el código intermedio con tripletas
codigo_intermedio_triples = generar_codigo_intermedio_triples(ast)

# Exportar los triples de código intermedio a una cadena de texto formateada
codigo_intermedio_triples_texto = exportar_triples_a_texto(codigo_intermedio_triples)

# Imprimir el código intermedio formateado
print(codigo_intermedio_triples_texto)
