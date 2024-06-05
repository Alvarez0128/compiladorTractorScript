class ArduinoCodeGenerator:
    def __init__(self):
        self.arduino_code = []
        self.indent_level = 1

    def add_line(self, line):
        indent = '  ' * self.indent_level
        self.arduino_code.append(f"{indent}{line}")

    def generate(self, node):
        self.add_line("void loop() {")
        self.indent_level += 1
        self.traverse(node)
        self.indent_level -= 1
        self.add_line("}")
        return '\n'.join(self.arduino_code)

    def traverse(self, node):
        
        
        if isinstance(node, tuple):
            
            node_type = node[0]
            if node_type == 'programa':
                self.traverse(node[1])
                
            if node_type == 'bloque_codigo':
              self.traverse_list(node[1])
                    
            if node_type == 'lista_declaraciones':
              self.traverse_list(node[1])
            if node_type == 'declaracion':
                self.handle_declaracion(node)
            if node_type == 'declaracion_estructura':
                self.traverse(node[1])
            if node_type == 'declaracion_funcion_interna':
                self.traverse(node[1])
            if node_type == 'llamada_funcion_motor':
                self.traverse(node[1])
            if node_type == 'si':
                self.handle_si(node)
            if node_type == 'sino':
                self.handle_sino(node)
            if node_type == 'mientras':
                self.handle_mientras(node)
            if node_type == 'mostrar_en_pantalla':
                self.add_line(f'Serial.println({node[1]});')
            if node_type == 'detener_motor':
                self.add_line('stop();')
            if node_type == 'motor_encendido':
                self.add_line('// MOTOR_ENCENDIDO() no tiene equivalente directo')
            if node_type == 'acelerar':
                print(node[0])
                self.add_line(f'forward({node[1]});')
            if node_type == 'retroceder':
                self.add_line('backward();')
            if node_type == 'girar_derecha':
                self.add_line('right();')
            if node_type == 'girar_izquierda':
                self.add_line('left();')
            if node_type == 'mover_implemento':
                self.add_line(f'myservo2.write({node[1]});')
            if node_type == 'esperar':
                self.add_line(f'delay({node[1]});')
            if node_type == 'obstaculo_detectado':
                self.handle_obstaculo_detectado(node)
            if node_type == 'sonar_alarma':
                self.add_line('alarm();')
            if node_type == 'calcular_distancia_restante':
                print("si entra")
                self.add_line('medirDistancia();')

    def handle_declaracion(self, node):
        if len(node) == 4:
            tipo, identificador, valor = node[1], node[2], node[3]
            if tipo == 'ENTERO':
                self.add_line(f'int {identificador} = {valor};')
            if tipo == 'DECIMAL':
                self.add_line(f'float {identificador} = {valor};')
            if tipo == 'BOOL':
                self.add_line(f'bool {identificador} = {valor};')
            if tipo == 'CADENA':
                self.add_line(f'string {identificador} = {valor};')
        else:
            identificador, valor = node[1], node[2]
            self.add_line(f'{identificador} = {valor};')

    def handle_si(self, node):
        if len(node) == 3:
            condicion, bloque = node[1], node[2]
            self.add_line(f'if {self.translate_expr(condicion)} {{')
            self.indent_level += 1
            self.traverse(bloque)
            self.indent_level -= 1
            self.add_line('}')

    def traverse_list(self, node_list):
        for child in node_list:
            self.traverse(child)

    def handle_sino(self, node):
        self.handle_si(node[1])
        self.add_line('else {')
        self.indent_level += 1
        self.traverse(node[2])
        self.indent_level -= 1
        self.add_line('}')

    def handle_mientras(self, node):
        condicion, bloque = node[1], node[2]
        self.add_line(f'while ({self.translate_expr(condicion)}) {{')
        self.indent_level += 1
        self.traverse(bloque)
        self.indent_level -= 1
        self.add_line('}')

    def handle_obstaculo_detectado(self, node):
        if node[1] == '40':
            self.add_line('myservo.write(40);')
        if node[1] == '140':
            self.add_line('myservo.write(140);')
        if node[1] == '90':
            self.add_line('myservo.write(90);')
        self.add_line('delay(600);')

    def translate_expr(self, expr):
        if isinstance(expr, tuple):
            if expr[0] == 'expresion':
                left = self.translate_expr(expr[1])
                op = expr[2]
                right = self.translate_expr(expr[3])
                return f'({left} {op} {right})'
            if expr[0] == 'grupo':
                return f'({self.translate_expr(expr[1])})'
        return str(expr)

# # Ejemplo de uso
# if __name__ == "__main__":
#     from Analizador_Sintactico import construir_analizador_lexico, construir_analizador_sintactico, print_tree

#     codigo_fuente = """
    # COMENZAR {
    #     ENTERO obstaculo_izquierda = 0;
    #     ENTERO obstaculo_derecha = 0;
    #     ENTERO temperatura = 0;
    #     ENTERO distancia = 10;

    #     temperatura = MEDIR_TEMPERATURA();
    #     MOTOR_ENCENDIDO();

    #     SI(temperatura<=75){
    #         MOVER_IMPLEMENTO(160);
    #         ESPERAR(600);

    #         SI(distancia <= 8){
    #             SI(distancia !=0){
    #                 RETROCEDER();
    #                 ESPERAR(400);
    #                 distancia=15;
    #             }
    #         }
    #         SI(distancia<= 20){
    #             SI(distancia !=0){
    #                 DETENER_MOTOR();
    #                 OBSTACULO_DETECTADO(40);
    #                 ESPERAR(600);
    #                 obstaculo_derecha = CALCULAR_DISTANCIA_RESTANTE();

    #                 OBSTACULO_DETECTADO(140);
    #                 ESPERAR(600);
    #                 obstaculo_izquierda = CALCULAR_DISTANCIA_RESTANTE();

    #                 //miramos de frente
    #                 OBSTACULO_DETECTADO(90);
    #                 ESPERAR(600);
    #             }
    #             SI(obstaculo_izquierda > obstaculo_derecha){
    #                 MOSTRAR_EN_PANTALLA("Giro izquierda");
    #                 GIRAR_IZQUIERDA();
    #             }
    #             SI(obstaculo_derecha >= obstaculo_izquierda){
    #                 MOSTRAR_EN_PANTALLA("Giro derecha");
    #                 GIRAR_DERECHA();
    #             }
    #         }
    #         SI(distancia > 20){
    #             MOSTRAR_EN_PANTALLA("RECTO");
    #             ACELERAR(80);
    #         }
    #         SINO{
    #             SONAR_ALARMA();
    #         }
    #     }
    # } TERMINAR
#     """

#     analizador_lexico = construir_analizador_lexico()
#     analizador_sintactico = construir_analizador_sintactico()

#     parse_result = analizador_sintactico.parse(codigo_fuente)
#     #arduino_generator = ArduinoCodeGenerator()
#     print_tree(parse_result)
#     #arduino_code = arduino_generator.generate(parse_result)
    
#     #print(arduino_code)
