from flask import Flask, request, jsonify
from flask_cors import CORS
from Analizador_Lexico import construir_analizador_lexico, reiniciar_analizador_lexico, obtener_errores_lexico
from Analizador_Sintactico import construir_analizador_sintactico, obtener_errores_sintactico, reiniciar_analizador_sintactico, tree_to_json
from Codigo_objeto import ArduinoCodeGenerator
from Codigo_intermedio import IntermediateCodeGenerator
# from Codigo_optimizado import generar_codigo_optimizado


app = Flask(__name__)
CORS(app)

parser = construir_analizador_sintactico()
lexer = construir_analizador_lexico()

@app.route('/compile', methods=['POST'])
def compile_code():
    reiniciar_analizador_lexico(lexer)
    reiniciar_analizador_sintactico()
    # Obtener el código fuente de la solicitud POST
    code = request.json['code']
    code = code.replace('\r\n', '\n')
    # Pasar el código al analizador léxico
    lexer.input(code)
    
    tokens = []
    for tok in lexer:
        tokens.append({
            'type': tok.type,
            'value': tok.value,
            'line': tok.lineno,
            'column': tok.lexpos - code.rfind('\n', 0, tok.lexpos)
        })
    errores_lexico = obtener_errores_lexico()
    reiniciar_analizador_lexico(lexer)
    reiniciar_analizador_sintactico()
    
    arbol = parser.parse(code)
    
    arbolJSON = tree_to_json(arbol)
    
    # Obtener errores después de analizar el código
    errores_sintactico = obtener_errores_sintactico()
    errores = errores_lexico + errores_sintactico
    
    intermediate_code_generator = IntermediateCodeGenerator()
    codigo_intermedio = intermediate_code_generator.generate(code)

    codigo_intermedio_texto = "\n".join([str(instr) for instr in codigo_intermedio])

    codigo_optimizado_texto = codigo_intermedio_texto
    arduino_generator = ArduinoCodeGenerator()
    arduino_code = arduino_generator.generate(arbol)

    initValues ="""#include <Servo.h>
#include <math.h>
Servo myservo;
Servo myservo2;
// Definición de pines del driver L298N
int ENA = 5; 
int IN1 = 12;
int IN2 = 13;
int ENB = 6;
int IN3 = 10;
int IN4 = 11;

// Definición de pines para lectura de temperatura
int TERMISTOR = A0;
int val;
int temp;

// Definición de pines para buzzer de alarma
int BUZZER_PIN = 7;

// Definición pines sensor distancia y variables para el cálculo de la distancia
int echoPin = 8; 
int trigPin = 9; 
long duration; 
int distance; 
int delayVal;

// Variable control posición servo y observaciones
int servoPos = 0;
int servoReadLeft = 0;
int servoReadRight = 0;

void setup() {
  // Definimos pines de servomotores
  myservo.attach(4);
  myservo2.attach(3);

  // Definimos pines de motores
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  pinMode(ENA, OUTPUT);
  pinMode(ENB, OUTPUT);

  // Definimos pin del termistor
  pinMode(TERMISTOR,INPUT);

  // Definimos pin del buzzer
  pinMode(BUZZER_PIN, OUTPUT);
  
  // Establecemos modo de los pines del sensor de ultrasonidos
  pinMode(trigPin, OUTPUT); 
  pinMode(echoPin, INPUT); 

  //Velocidad de los motores
  analogWrite(ENA, 90); 
  analogWrite(ENB, 85); 
  myservo.write(90); 
  Serial.begin(9600);
}

"""

    functions = """
    
  void left() {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  analogWrite(ENA, 150); 
  analogWrite(ENB, 140); 
  delay(450);
}

void right() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
  analogWrite(ENA, 150); 
  analogWrite(ENB, 140); 
  delay(450);
}

int forward(int x) {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  analogWrite(ENA, x); 
  analogWrite(ENB, x); 
}

void backward() {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
  analogWrite(ENA, 120); 
  analogWrite(ENB, 110); 
}

void stop() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
}

double Thermister(int RawADC) {
  double Temp;
  Temp = log(((10240000/RawADC) - 10000));
  Temp = 1 / (0.001129148 + (0.000234125 + (0.0000000876741 * Temp * Temp ))* Temp );
  Temp = Temp - 273.15;
  return Temp;
}

void alarm() {
  // Hace sonar el buzzer durante un segundo
  tone(BUZZER_PIN, 1000); // 1000 Hz
  delay(1000); // Duración del sonido en milisegundos
  noTone(BUZZER_PIN); // Detiene el sonido del buzzer
  delay(500); // Pausa entre repeticiones de la alarma
}

int medirDistancia(){
  // Lanzamos pulso de sonido
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(20);
  digitalWrite(trigPin, LOW);
  
  // Leemos lo que tarda el pulso en llegar al sensor y calculamos distancia
  duration = pulseIn(echoPin, HIGH);
  distance = duration * 0.034 / 2;

  // Devolver distancia calculada
  return distance;    
}
""" 
    codigo_arduino_texto=f"{initValues} {arduino_code}{functions}"
    
    # # Generar el código Arduino
    # if codigo_optimizado:
    #     codigo_arduino = generar_codigo_arduino(codigo_optimizado)
    #     # Exportar el código Arduino a una cadena de texto formateada
    #     codigo_arduino_texto = exportar_codigo_a_texto(codigo_arduino)
    # else:
    #     codigo_arduino_texto = "Código Arduino no generado"

    # Devolver los resultados y errores
    return jsonify({'tokens': tokens, 'errors': errores},arbolJSON,codigo_intermedio_texto,codigo_optimizado_texto,codigo_arduino_texto) 


if __name__ == '__main__':
    app.run(debug=True)
