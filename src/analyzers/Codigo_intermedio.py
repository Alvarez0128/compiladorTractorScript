class IntermediateCodeGenerator:
    def __init__(self):
        self.instructions = []
        self.temp_counter = 0
        self.label_counter = 0
        self.labels = {}

    def get_temp(self):
        temp = f"t{self.temp_counter}"
        self.temp_counter += 1
        return temp

    def get_label(self):
        label = f"L{self.label_counter}"
        self.label_counter += 1
        return label

    def add_instruction(self, op, arg1=None, arg2=None, result=None):
        self.instructions.append((op, arg1, arg2, result))

    def parse_line(self, line):
        line = line.strip()
        if line.startswith("ENTERO"):
            parts = line.split()
            if len(parts) == 2:
                _, var = parts
                self.add_instruction('=', 0, None, var)
        elif line.startswith("temperatura = MEDIR_TEMPERATURA()"):
            self.add_instruction('MEDIR_TEMPERATURA', None, None, 'temperatura')
        elif line.startswith("MOTOR_ENCENDIDO()"):
            self.add_instruction('MOTOR_ENCENDIDO', None, None, None)
        elif line.startswith("SI"):
            condition = line[3:-1]  # Extrae la condición entre paréntesis
            self.handle_condition(condition)
        elif line.startswith("SINO"):
            self.add_instruction('GOTO', None, None, self.get_label())
        elif line.startswith("ESPERAR"):
            time = line[8:-1]  # Extrae el tiempo entre paréntesis
            self.add_instruction('ESPERAR', time, None, None)
        elif line.startswith("MOVER_IMPLEMENTO"):
            angle = line[17:-1]  # Extrae el ángulo entre paréntesis
            self.add_instruction('MOVER_IMPLEMENTO', angle, None, None)
        elif line.startswith("RETROCEDER()"):
            self.add_instruction('RETROCEDER', None, None, None)
        elif line.startswith("DETENER_MOTOR()"):
            self.add_instruction('DETENER_MOTOR', None, None, None)
        elif line.startswith("OBSTACULO_DETECTADO"):
            angle = line[19:-1]  # Extrae el ángulo entre paréntesis
            self.add_instruction('OBSTACULO_DETECTADO', angle, None, None)
        elif line.startswith("CALCULAR_DISTANCIA_RESTANTE()"):
            var = line.split('=')[0].strip()
            self.add_instruction('CALCULAR_DISTANCIA_RESTANTE', None, None, var)
        elif line.startswith("MOSTRAR_EN_PANTALLA"):
            message = line[19:-1]  # Extrae el mensaje entre paréntesis
            self.add_instruction('MOSTRAR_EN_PANTALLA', message, None, None)
        elif line.startswith("GIRAR_IZQUIERDA()"):
            self.add_instruction('GIRAR_IZQUIERDA', None, None, None)
        elif line.startswith("GIRAR_DERECHA()"):
            self.add_instruction('GIRAR_DERECHA', None, None, None)
        elif line.startswith("ACELERAR"):
            speed = line[9:-1]  # Extrae la velocidad entre paréntesis
            self.add_instruction('ACELERAR', speed, None, None)
        elif line.startswith("SONAR_ALARMA()"):
            self.add_instruction('SONAR_ALARMA', None, None, None)

    def handle_condition(self, condition):
        parts = condition.split()
        
        if len(condition.split())==1:
            op = parts[0]
            label=self.get_label()
            self.add_instruction(op, label)
        elif len(condition.split())==2:
            op = parts[0]
            arg1 = parts[1]
            label=self.get_label()
            self.add_instruction(op,arg1, label)
        else:
            op = parts[0]
            arg1 = parts[1]
            arg2 = parts[2]
            label=self.get_label()
            self.add_instruction(op,arg1,arg2, label)

    def generate(self, code):
        lines = code.split('\n')
        for line in lines:
            self.parse_line(line)
        return self.instructions

# Código de entrada TractorScript
# tractor_code = """
# COMENZAR{
#         ENTERO obstaculo_izquierda = 0;
#         ENTERO obstaculo_derecha = 0;
#         ENTERO temperatura = 0;
#         ENTERO distancia = 10;

#         temperatura = MEDIR_TEMPERATURA();
#         MOTOR_ENCENDIDO();

#         SI(temperatura<=75){
#             MOVER_IMPLEMENTO(160);
#             ESPERAR(600);

#             SI(distancia <= 8){
#                 SI(distancia !=0){
#                     RETROCEDER();
#                     ESPERAR(400);
#                     distancia=15;
#                 }
#             }
#             SI(distancia<= 20){
#                 SI(distancia !=0){
#                     DETENER_MOTOR();
#                     OBSTACULO_DETECTADO(40);
#                     ESPERAR(600);
#                     obstaculo_derecha = CALCULAR_DISTANCIA_RESTANTE();

#                     OBSTACULO_DETECTADO(140);
#                     ESPERAR(600);
#                     obstaculo_izquierda = CALCULAR_DISTANCIA_RESTANTE();

#                     //miramos de frente
#                     OBSTACULO_DETECTADO(90);
#                     ESPERAR(600);
#                 }
#                 SI(obstaculo_izquierda > obstaculo_derecha){
#                     MOSTRAR_EN_PANTALLA("Giro izquierda");
#                     GIRAR_IZQUIERDA();
#                 }
#                 SI(obstaculo_derecha >= obstaculo_izquierda){
#                     MOSTRAR_EN_PANTALLA("Giro derecha");
#                     GIRAR_DERECHA();
#                 }
#             }
#             SI(distancia > 20){
#                 MOSTRAR_EN_PANTALLA("RECTO");
#                 ACELERAR(80);
#             }
#             SINO{
#                 SONAR_ALARMA();
#             }
#         }
#     }TERMINAR
# """

# generator = IntermediateCodeGenerator()
# intermediate_code = generator.generate(tractor_code)

# for index, instr in enumerate(intermediate_code, start=1):
#     op, arg1, arg2, result = instr
#     print(f"{index}. [{op}, {arg1}, {arg2}, {result}]")
