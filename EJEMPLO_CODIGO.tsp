COMENZAR {
        ENTERO obstaculo_izquierda = 0;
        ENTERO obstaculo_derecha = 0;
        ENTERO temperatura = 0;
        ENTERO distancia = 10;

        temperatura = MEDIR_TEMPERATURA();
        MOTOR_ENCENDIDO();

        SI(temperatura<=75){
            MOVER_IMPLEMENTO(160);
            ESPERAR(600);

            SI(distancia <= 8){
                SI(distancia !=0){
                    RETROCEDER();
                    ESPERAR(400);
                    distancia=15;
                }
            }
            SI(distancia<= 20){
                SI(distancia !=0){
                    DETENER_MOTOR();
                    OBSTACULO_DETECTADO(40);
                    ESPERAR(600);
                    obstaculo_derecha = CALCULAR_DISTANCIA_RESTANTE();

                    OBSTACULO_DETECTADO(140);
                    ESPERAR(600);
                    obstaculo_izquierda = CALCULAR_DISTANCIA_RESTANTE();

                    //miramos de frente
                    OBSTACULO_DETECTADO(90);
                    ESPERAR(600);
                }
                SI(obstaculo_izquierda > obstaculo_derecha){
                    MOSTRAR_EN_PANTALLA("Giro izquierda");
                    GIRAR_IZQUIERDA();
                }
                SI(obstaculo_derecha >= obstaculo_izquierda){
                    MOSTRAR_EN_PANTALLA("Giro derecha");
                    GIRAR_DERECHA();
                }
            }
            SI(distancia > 20){
                MOSTRAR_EN_PANTALLA("RECTO");
                ACELERAR(80);
            }
            SINO{
                SONAR_ALARMA();
            }
        }
    } TERMINAR