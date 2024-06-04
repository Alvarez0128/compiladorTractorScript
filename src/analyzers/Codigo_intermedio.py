from Analizador_Lexico import reiniciar_analizador_lexico, construir_analizador_lexico
from Analizador_Sintactico import construir_analizador_sintactico, obtener_errores_sintactico, reiniciar_analizador_sintactico
from SymbolTable import SymbolTable, Symbol

class GeneradorCodigoIntermedio:
    def __init__(self):
        self.tripletas = []
        self.temporales = 0
        self.etiquetas = 0

    def nueva_temporal(self):
        temporal = f"t{self.temporales}"
        self.temporales += 1
        return temporal

    def nueva_etiqueta(self):
        etiqueta = f"L{self.etiquetas}"
        self.etiquetas += 1
        return etiqueta

    def generar_tripleta(self, operador, operando1=None, operando2=None, resultado=None):
        if not resultado:
            resultado = self.nueva_temporal()
        tripleta = (operador, operando1, operando2, resultado)
        self.tripletas.append(tripleta)
        return resultado

    def imprimir_tripletas(self):
        for i, tripleta in enumerate(self.tripletas):
            print(f"({i+1}) {tripleta}")

    def analizar(self, codigo):
        lexer = construir_analizador_lexico()
        parser = construir_analizador_sintactico()
        reiniciar_analizador_lexico(lexer)
        reiniciar_analizador_sintactico()
        arbol = parser.parse(codigo, lexer=lexer)
        self.recorrer_arbol(arbol)

    def recorrer_arbol(self, nodo):
        if isinstance(nodo, list):
            for subnodo in nodo:
                self.recorrer_arbol(subnodo)
        elif isinstance(nodo, tuple):
            nodo_tipo = nodo[0]
            if nodo_tipo == 'programa':
                self.recorrer_arbol(nodo[1])
            elif nodo_tipo == 'bloque_codigo':
                self.recorrer_arbol(nodo[1])
            elif nodo_tipo == 'declaracion':
                self.recorrer_arbol(nodo[0])
            elif nodo_tipo == 'declaracion_variable':
                identificador = nodo[1]
                valor = self.recorrer_arbol(nodo[2])
                self.generar_tripleta('=', valor, None, identificador)
            elif nodo_tipo == 'asignacion':
                identificador = nodo[1]
                valor = self.recorrer_arbol(nodo[2])
                self.generar_tripleta('=', valor, None, identificador)
            elif nodo_tipo == 'instruccion':
                self.recorrer_arbol(nodo[1])
            elif nodo_tipo == 'llamada_funcion':
                nombre_funcion = nodo[1]
                argumentos = [self.recorrer_arbol(arg) for arg in nodo[2]]
                self.generar_tripleta(nombre_funcion, *argumentos)
            elif nodo_tipo == 'if':
                condicion = self.recorrer_arbol(nodo[1])
                etiqueta_else = self.nueva_etiqueta()
                etiqueta_fin = self.nueva_etiqueta()
                self.generar_tripleta('if', condicion, None, etiqueta_else)
                self.recorrer_arbol(nodo[2])
                self.generar_tripleta('goto', None, None, etiqueta_fin)
                self.generar_tripleta('label', None, None, etiqueta_else)
                if len(nodo) > 3:
                    self.recorrer_arbol(nodo[3])
                self.generar_tripleta('label', None, None, etiqueta_fin)
            elif nodo_tipo == 'while':
                etiqueta_inicio = self.nueva_etiqueta()
                etiqueta_fin = self.nueva_etiqueta()
                self.generar_tripleta('label', None, None, etiqueta_inicio)
                condicion = self.recorrer_arbol(nodo[1])
                self.generar_tripleta('if', condicion, None, etiqueta_fin)
                self.recorrer_arbol(nodo[2])
                self.generar_tripleta('goto', None, None, etiqueta_inicio)
                self.generar_tripleta('label', None, None, etiqueta_fin)
            elif nodo_tipo == 'binario':
                operador = nodo[1]
                operando1 = self.recorrer_arbol(nodo[0])
                operando2 = self.recorrer_arbol(nodo[2])
                return self.generar_tripleta(operador, operando1, operando2)
            elif nodo_tipo == 'numero':
                return nodo[1]
            elif nodo_tipo == 'identificador':
                return nodo[1]
            else:
                print(f"Error: Nodo tipo {nodo_tipo} no reconocido")

if __name__ == "__main__":
    codigo_prueba = """
    COMENZAR{
        BOOL obstaculo_detectado = Falso;
        DECIMAL distancia_objetivo = 500.0;
        DECIMAL distancia_recorrida = 0.0;
        DECIMAL velocidad = 0.0;
        DECIMAL tiempo_transcurrido = 1.0;

        MOTOR_ENCENDIDO();
        AJUSTAR_VELOCIDAD(50);
        ACELERAR();

        MIENTRAS(distancia_recorrida < distancia_objetivo){
            SI(obstaculo_detectado){
                SI(CALCULAR_DISTANCIA_RESTANTE(distancia_objetivo) < 100){
                    AJUSTAR_VELOCIDAD(0);
                    DETENER_MOTOR();
                    SONAR_ALARMA();
                    ACTIVAR_FRENO();
                    ESPERAR(5);
                    obstaculo_detectado = Falso;
                    MOTOR_ENCENDIDO();
                    AJUSTAR_VELOCIDAD(50);
                    ACELERAR();
                } SINO {
                    AJUSTAR_VELOCIDAD(20);
                }
            } SINO {
                SI(VERIFICAR_SENSOR_OBSTACULOS()){
                    obstaculo_detectado = verdadero;
                } SINO {
                    AJUSTAR_VELOCIDAD(50);
                }
            }
            distancia_recorrida = distancia_recorrida + (velocidad * tiempo_transcurrido);
        }

        AJUSTAR_VELOCIDAD(0);
        DETENER_MOTOR();
    }TERMINAR
    """
    generador = GeneradorCodigoIntermedio()
    generador.analizar(codigo_prueba)
    generador.imprimir_tripletas()
