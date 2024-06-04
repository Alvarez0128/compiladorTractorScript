from Analizador_Lexico import reiniciar_analizador_lexico, construir_analizador_lexico
from Analizador_Sintactico import construir_analizador_sintactico, reiniciar_analizador_sintactico
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
                if len(nodo) == 4:
                    identificador = nodo[2]
                    valor = self.recorrer_arbol(nodo[3])
                    self.generar_tripleta('=', valor, None, identificador)
                else:
                    identificador = nodo[1]
                    valor = self.recorrer_arbol(nodo[2])
                    self.generar_tripleta('=', valor, None, identificador)
            elif nodo_tipo == 'declaracion_estructura':
                self.recorrer_arbol(nodo[1])
            elif nodo_tipo == 'declaracion_funcion_interna':
                self.recorrer_arbol(nodo[1])
            elif nodo_tipo == 'si':
                condicion = self.recorrer_arbol(nodo[1])
                etiqueta_else = self.nueva_etiqueta()
                etiqueta_fin = self.nueva_etiqueta()
                self.generar_tripleta('if', condicion, None, etiqueta_else)
                self.recorrer_arbol(nodo[2])
                self.generar_tripleta('goto', None, None, etiqueta_fin)
                self.generar_tripleta('label', None, None, etiqueta_else)
                self.generar_tripleta('label', None, None, etiqueta_fin)
            elif nodo_tipo == 'sino':
                self.recorrer_arbol(nodo[1])
                self.recorrer_arbol(nodo[2])
            elif nodo_tipo == 'para':
                self.recorrer_arbol(nodo[1])
                self.recorrer_arbol(nodo[2])
                self.recorrer_arbol(nodo[3])
                self.recorrer_arbol(nodo[4])
                self.recorrer_arbol(nodo[5])
            elif nodo_tipo == 'mientras':
                etiqueta_inicio = self.nueva_etiqueta()
                etiqueta_fin = self.nueva_etiqueta()
                self.generar_tripleta('label', None, None, etiqueta_inicio)
                condicion = self.recorrer_arbol(nodo[1])
                self.generar_tripleta('if', condicion, None, etiqueta_fin)
                self.recorrer_arbol(nodo[2])
                self.generar_tripleta('goto', None, None, etiqueta_inicio)
                self.generar_tripleta('label', None, None, etiqueta_fin)
            elif nodo_tipo == 'mostrar_en_pantalla':
                self.generar_tripleta('mostrar_en_pantalla', self.recorrer_arbol(nodo[1]))
            elif nodo_tipo == 'detener_motor':
                self.generar_tripleta('detener_motor')
            elif nodo_tipo == 'motor_encendido':
                self.generar_tripleta('motor_encendido')
            elif nodo_tipo == 'velocidad':
                self.generar_tripleta('velocidad')
            elif nodo_tipo == 'cambiar_direccion':
                self.generar_tripleta('cambiar_direccion')
            elif nodo_tipo == 'verificar_freno':
                self.generar_tripleta('verificar_freno')
            elif nodo_tipo == 'distancia_recorrida':
                self.generar_tripleta('distancia_recorrida')
            elif nodo_tipo == 'frenos_activados':
                self.generar_tripleta('frenos_activados')
            elif nodo_tipo == 'calcular_distancia_restante':
                self.generar_tripleta('calcular_distancia_restante', nodo[2])
            elif nodo_tipo == 'distancia_restante':
                self.generar_tripleta('distancia_restante')
            elif nodo_tipo == 'acelerar':
                self.generar_tripleta('acelerar')
            elif nodo_tipo == 'ajustar_velocidad':
                self.generar_tripleta('ajustar_velocidad', nodo[1])
            elif nodo_tipo == 'nueva_velocidad':
                self.generar_tripleta('nueva_velocidad', nodo[1])
            elif nodo_tipo == 'sonar_alarma':
                self.generar_tripleta('sonar_alarma')
            elif nodo_tipo == 'esperar':
                self.generar_tripleta('esperar', nodo[1])
            elif nodo_tipo == 'verificar_sensor_obstaculos':
                self.generar_tripleta('verificar_sensor_obstaculos')
            elif nodo_tipo == 'tiempo_transcurrido':
                self.generar_tripleta('tiempo_transcurrido')
            elif nodo_tipo == 'activar_freno':
                self.generar_tripleta('activar_freno')
            elif nodo_tipo == 'expresion':
                operador = nodo[1]
                operando1 = self.recorrer_arbol(nodo[0])
                operando2 = self.recorrer_arbol(nodo[2])
                return self.generar_tripleta(operador, operando1, operando2)
            elif nodo_tipo == 'grupo':
                return self.recorrer_arbol(nodo[1])
            elif nodo_tipo == 'identificador':
                return nodo[1]
            elif nodo_tipo == 'numero':
                return nodo[1]
            elif nodo_tipo == 'bool':
                return nodo[1]
            elif nodo_tipo == 'cadena':
                return nodo[1]
            elif nodo_tipo == 'lista':
                return self.recorrer_arbol(nodo[2])
            elif nodo_tipo == 'llamada_funcion_motor':
                self.recorrer_arbol(nodo[1])
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
