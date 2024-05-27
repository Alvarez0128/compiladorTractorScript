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