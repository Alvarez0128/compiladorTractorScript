# optimizado_Codigo_Intermedio.py

from SymbolTable import Symbol, SymbolTable
from Analizador_Sintactico import construir_analizador_sintactico, NodoPara
from Analizador_Lexico import construir_analizador_lexico
from tripletas import GeneradorTripletas

generador_tripletas = GeneradorTripletas()

def nuevo_temp():
    return generador_tripletas.nueva_temporal()

def agregar_tripleta(*args):
    generador_tripletas.agregar_tripleta(*args)

def generar_codigo_intermedio_triples(node):
    def recorrer_arbol(node):
        if isinstance(node, tuple):
            tipo_nodo = node[0]
            if tipo_nodo == 'programa':
                recorrer_arbol(node[1])
            elif tipo_nodo == 'bloque_codigo':
                for decl in node[1]:
                    recorrer_arbol(decl)
            elif tipo_nodo == 'declaracion':
                if len(node) == 4:
                    _, ident, valor = node[1], node[2], node[3]
                    agregar_tripleta('=', ident, valor)
                else:
                    recorrer_arbol(node[1])
            elif tipo_nodo == 'si':
                manejar_condicional(node[1], node[2])
            elif tipo_nodo == 'si_no':
                manejar_condicional_con_sino(node[1], node[2], node[3])
            elif tipo_nodo == 'mientras':
                manejar_bucle_mientras(node[1], node[2])
            elif tipo_nodo == 'operacion':
                return manejar_operacion(node[1], node[2], node[3])
            else:
                for child in node:
                    recorrer_arbol(child)
        elif isinstance(node, str):
            return node

    def manejar_condicional(condicion, bloque_si):
        temp_cond = recorrer_arbol(condicion)
        label_si = f"L{len(generador_tripletas.obtener_tripletas())+2}"
        label_end = f"L{len(generador_tripletas.obtener_tripletas())+3}"
        agregar_tripleta('IF', temp_cond, label_si)
        agregar_tripleta('GOTO', label_end, '')
        agregar_tripleta('LABEL', label_si, '')
        recorrer_arbol(bloque_si)
        agregar_tripleta('LABEL', label_end, '')

    def manejar_condicional_con_sino(condicion, bloque_si, bloque_no):
        temp_cond = recorrer_arbol(condicion)
        label_si = f"L{len(generador_tripletas.obtener_tripletas())+2}"
        label_no = f"L{len(generador_tripletas.obtener_tripletas())+3}"
        label_end = f"L{len(generador_tripletas.obtener_tripletas())+4}"
        agregar_tripleta('IF', temp_cond, label_si)
        agregar_tripleta('GOTO', label_no, '')
        agregar_tripleta('LABEL', label_si, '')
        recorrer_arbol(bloque_si)
        agregar_tripleta('GOTO', label_end, '')
        agregar_tripleta('LABEL', label_no, '')
        recorrer_arbol(bloque_no)
        agregar_tripleta('LABEL', label_end, '')

    def manejar_bucle_mientras(condicion, bloque):
        label_start = f"L{len(generador_tripletas.obtener_tripletas())+1}"
        label_end = f"L{len(generador_tripletas.obtener_tripletas())+2}"
        agregar_tripleta('LABEL', label_start, '')
        temp_cond = recorrer_arbol(condicion)
        agregar_tripleta('IF', temp_cond, label_end)
        recorrer_arbol(bloque)
        agregar_tripleta('GOTO', label_start, '')
        agregar_tripleta('LABEL', label_end, '')

    def manejar_operacion(izq, op, der):
        temp_izq = recorrer_arbol(izq)
        temp_der = recorrer_arbol(der)
        temp_res = nuevo_temp()
        agregar_tripleta('=', temp_res, f"{temp_izq} {op} {temp_der}")
        return temp_res

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
lexer = construir_analizador_lexico()
# Construir los analizadores
parser = construir_analizador_sintactico()

# Realizar el análisis léxico y sintáctico
ast = parser.parse(test_code)

# Generar el código intermedio con tripletas
codigo_optimizado_triples = generar_codigo_intermedio_triples(ast)

# Exportar los triples de código intermedio a una cadena de texto formateada
codigo_optimizado_triples_texto = exportar_triples_a_texto(codigo_optimizado_triples)

# Imprimir el código intermedio formateado
print(codigo_optimizado_triples_texto)
