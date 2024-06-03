COMENZAR{
    BOOL obstaculo_detectado = Falso;
    DECIMAL distancia_objetivo = 500.0;
    DECIMAL distancia_recorrida = 0.0; // Declarar distancia_recorrida
    DECIMAL velocidad = 0.0; // Declarar velocidad
    DECIMAL tiempo_transcurrido = 1.0; // Asumir un tiempo transcurrido constante para la simulación

    MOTOR_ENCENDIDO();  // Se enciende el motor al inicio
    AJUSTAR_VELOCIDAD(50);  // Se ajusta la velocidad inicial
    ACELERAR(); // Iniciar el avance del vehículo

    MIENTRAS(distancia_recorrida < distancia_objetivo){
        SI(obstaculo_detectado){
            SI(CALCULAR_DISTANCIA_RESTANTE(distancia_objetivo) < 100){
                AJUSTAR_VELOCIDAD(0); // Reducir la velocidad a 0 antes de detener el motor
                DETENER_MOTOR(); // Detener el motor después de ajustar la velocidad a 0
                SONAR_ALARMA();
                ACTIVAR_FRENO(); // Activar freno inmediatamente después de detener el motor
                ESPERAR(5); // Esperar 5 segundos con los frenos activados
                obstaculo_detectado = Falso; // Reiniciar la detección de obstáculos
                MOTOR_ENCENDIDO(); // Encender el motor de nuevo
                AJUSTAR_VELOCIDAD(50); // Volver a la velocidad inicial
                ACELERAR(); // Reanudar el avance del vehículo
            } SINO {
                AJUSTAR_VELOCIDAD(20); // Reducir la velocidad para evitar el obstáculo
            }
        } SINO {
            SI(VERIFICAR_SENSOR_OBSTACULOS()){
                obstaculo_detectado = V; // Detectar obstáculo
            } SINO {
                AJUSTAR_VELOCIDAD(50); // Mantener velocidad constante
            }
        }
        distancia_recorrida = distancia_recorrida + (velocidad * tiempo_transcurrido);
    }

    AJUSTAR_VELOCIDAD(0); // Reducir la velocidad a 0 antes de detener el motor
    DETENER_MOTOR(); // Detener el motor al final del recorrido
}TERMINAR