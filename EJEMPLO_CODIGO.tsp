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