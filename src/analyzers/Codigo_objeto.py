import ply.yacc as yacc
from Analizador_Lexico import construir_analizador_lexico, obtener_errores_lexico, reiniciar_analizador_lexico, tokens
from SymbolTable import Symbol, SymbolTable
from Analizador_Sintactico import construir_analizador_sintactico, NodoPara
from Codigo_optimizado import optimizar_codigo_intermedio, generar_codigo_intermedio

# Función para generar el código objeto (Arduino) a partir del código intermedio
def generar_codigo_arduino(codigo_intermedio):
    codigo_arduino = []

    def traducir_linea(linea):
        # Traducción de declaraciones de variables
        if "BOOL" in linea:
            return linea.replace("BOOL", "bool").replace("F", "false").replace("V", "true")
        elif "DECIMAL" in linea:
            return linea.replace("DECIMAL", "float")
        elif "PRINT" in linea:
            return linea.replace("PRINT", "Serial.println")
        elif "IF" in linea:
            return linea.replace("IF", "if")
        elif "WHILE" in linea:
            return linea.replace("WHILE", "while")
        elif "OBSTACLE_DETECTED" in linea:
            return "// Código para detectar obstáculo"
        elif "FOR" in linea:
            return linea.replace("FOR", "for")

        return linea

    # Añadir el código de configuración inicial para Arduino
    codigo_arduino.append("#include <Arduino.h>")
    codigo_arduino.append("int ENA = 29;")
    codigo_arduino.append("int IN1 = 32;")
    codigo_arduino.append("int IN2 = 33;")
    codigo_arduino.append("int ENB = 31;")
    codigo_arduino.append("int IN3 = 36;")
    codigo_arduino.append("int IN4 = 37;")
    codigo_arduino.append("int TERMISTOR = 40;")
    codigo_arduino.append("int BUZZER_PIN = 7;")
    codigo_arduino.append("int echoPin = 8;")
    codigo_arduino.append("int trigPin = 9;")
    codigo_arduino.append("int SERVO_PIN = 4;")
    codigo_arduino.append("void setup() {")
    codigo_arduino.append("  Serial.begin(9600);")
    codigo_arduino.append("  pinMode(ENA, OUTPUT);")
    codigo_arduino.append("  pinMode(IN1, OUTPUT);")
    codigo_arduino.append("  pinMode(IN2, OUTPUT);")
    codigo_arduino.append("  pinMode(ENB, OUTPUT);")
    codigo_arduino.append("  pinMode(IN3, OUTPUT);")
    codigo_arduino.append("  pinMode(IN4, OUTPUT);")
    codigo_arduino.append("  pinMode(BUZZER_PIN, OUTPUT);")
    codigo_arduino.append("  pinMode(echoPin, INPUT);")
    codigo_arduino.append("  pinMode(trigPin, OUTPUT);")
    codigo_arduino.append("  pinMode(TERMISTOR, INPUT);")
    codigo_arduino.append("  servo.attach(SERVO_PIN);")
    codigo_arduino.append("}")
    codigo_arduino.append("void loop() {")

    for linea in codigo_intermedio:
        linea_traducida = traducir_linea(linea)
        if linea_traducida:
            codigo_arduino.append("  " + linea_traducida)

    # Añadir el cierre del bucle loop
    codigo_arduino.append("}")

    return codigo_arduino

# Probar el código de ejemplo
test_code = """
COMENZAR{

BOOL obstaculo_detectado = F;
DECIMAL distancia_objetivo = 500.0;

MIENTRAS(distancia_recorrida < distancia_objetivo){
    SI(obstaculo_detectado){
        SI(calcular_distancia_restante(distancia_objetivo) < 100){
            detener_motor();
            SONAR_ALERTA();
            ESPERAR(5); // Espera 5 segundos antes de reanudar
            activar_freno();
            ESPERAR(2); // Espera 2 segundos con los frenos activados
            obstaculo_detectado = F; // Reinicia la detección de obstáculos
        }SINO{
            ajustar_velocidad(20); // Reducir la velocidad para evitar el obstáculo
        }
    }SINO{
        SI(verificar_sensor_obstaculos()){
            obstaculo_detectado = V;
        }SINO{
            ajustar_velocidad(50); // Mantener velocidad constante
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

# Optimizar el código intermedio
codigo_optimizado = optimizar_codigo_intermedio(codigo_intermedio)

# Generar el código Arduino
codigo_arduino = generar_codigo_arduino(codigo_optimizado)

# Imprimir el código Arduino
for linea in codigo_arduino:
    print(linea)
