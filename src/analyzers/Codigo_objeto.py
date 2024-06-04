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
    codigo_arduino.append("#include <Servo.h>")
    codigo_arduino.append("Servo myservo;")
    codigo_arduino.append("Servo myservo2;")
    codigo_arduino.append("int ENA = 5;")
    codigo_arduino.append("int IN1 = 12;")
    codigo_arduino.append("int IN2 = 13;")
    codigo_arduino.append("int ENB = 6;")
    codigo_arduino.append("int IN3 = 10;")
    codigo_arduino.append("int IN4 = 11;")
    codigo_arduino.append("int TERMISTOR = A0;")
    codigo_arduino.append("int val;")
    codigo_arduino.append("int temp;")
    codigo_arduino.append("int BUZZER_PIN = 7;")
    codigo_arduino.append("int echoPin = 8;")
    codigo_arduino.append("int trigPin = 9;")
    codigo_arduino.append("long duration;")
    codigo_arduino.append("int distance;")
    codigo_arduino.append("int delayVal;")
    codigo_arduino.append("int servoPos = 0;")
    codigo_arduino.append("int servoReadLeft = 0;")
    codigo_arduino.append("int servoReadRight = 0;")
    codigo_arduino.append("void setup() {")
    codigo_arduino.append("  Serial.begin(9600);")
    codigo_arduino.append("  myservo.attach(4);")
    codigo_arduino.append("  myservo2.attach(3);")
    codigo_arduino.append("  pinMode(IN1, OUTPUT);")
    codigo_arduino.append("  pinMode(IN2, OUTPUT);")
    codigo_arduino.append("  pinMode(IN3, OUTPUT);")
    codigo_arduino.append("  pinMode(IN4, OUTPUT);")
    codigo_arduino.append("  pinMode(ENA, OUTPUT);")
    codigo_arduino.append("  pinMode(ENB, OUTPUT);")
    codigo_arduino.append("  pinMode(TERMISTOR, INPUT);")
    codigo_arduino.append("  pinMode(BUZZER_PIN, OUTPUT);")
    codigo_arduino.append("  pinMode(trigPin, OUTPUT);")
    codigo_arduino.append("  pinMode(echoPin, INPUT);")
    codigo_arduino.append("}")
    codigo_arduino.append("void loop() {")

    for linea in codigo_intermedio:
        linea_traducida = traducir_linea(linea)
        if linea_traducida:
            codigo_arduino.append("  " + linea_traducida)

    # Añadir el cierre del bucle loop
    codigo_arduino.append("}")

    return codigo_arduino

def exportar_codigo_a_texto(codigo):
    return "\n".join(codigo)


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

# # Generar el código Arduino
# codigo_arduino = generar_codigo_arduino(codigo_optimizado)

# # Exportar el código Arduino a una cadena de texto formateada
# codigo_arduino_texto = exportar_codigo_a_texto(codigo_arduino)

# # Imprimir el código Arduino formateado
# print(codigo_arduino_texto)
