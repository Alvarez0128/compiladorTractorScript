#include <Servo.h>
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

void loop() {
  //Subir el servomotor de carga
  //myservo2.write(160);
  //delay(600);
  //Bajar el servomotor de carga
  //myservo2.write(100);
  //delay(600);

  val=analogRead(TERMISTOR);
  temp=Thermister(val);
  
  if (temp <= 75){
    //Subir el servomotor de carga
    myservo2.write(160);
    delay(600);
    distance = medirDistancia();
    //Serial.println(distance);
    if (distance <= 8 && distance != 0){
      backward();
      delay(400);
      distance = 15;
    }
    if (distance <= 20 && distance != 0){
      stop();
      
      // Miramos a la derecha    
      myservo.write(40);  
      delay(600); 
      servoReadRight = medirDistancia();

      // Miramos a la izquierda                             
      myservo.write(140);  
      delay(600); 
      servoReadLeft = medirDistancia();

      // Miramos de frente 
      myservo.write(90);  
      delay(600); 

      if(servoReadLeft > servoReadRight){
        Serial.println("Giro izquierda");
        left();
      }

      if(servoReadRight >= servoReadLeft){
        Serial.println("Giro derecha");
        right(); 
      }
    }
    
    if(distance > 20){
      Serial.println("Recto");
      forward(80);
    }
  }else{
    alarm();
  }
}

// Función para girar hacia adelante
void left() {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  analogWrite(ENA, 150); 
  analogWrite(ENB, 140); 
  delay(450);
}

// Función para girar hacia atrás
void right() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
  analogWrite(ENA, 150); 
  analogWrite(ENB, 140); 
  delay(450);
}

// Función para girar a la izquierda
int forward(int x) {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  analogWrite(ENA, x); 
  analogWrite(ENB, x); 
}

// Función para girar a la derecha
void backward() {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
  analogWrite(ENA, 120); 
  analogWrite(ENB, 110); 
}

// Función para girar a la derecha
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