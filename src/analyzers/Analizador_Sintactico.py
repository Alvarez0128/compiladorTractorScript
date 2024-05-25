import ply.yacc as yacc
from Analizador_Lexico import construir_analizador_lexico, obtener_errores_lexico, reiniciar_analizador_lexico, tokens, find_column_lexico
from SymbolTable import Symbol, SymbolTable

tabla_errores=obtener_errores_lexico()
tabla_simbolos_global = SymbolTable()
para_scope = tabla_simbolos_global.enter_scope()

def agregar_error_sintactico(id,error_type,error_description, value, line, column):
    tabla_errores.append({
        'index':id,
        'type': error_type,
        'description': error_description,
        'value': str(value),
        'line': line,
        'column': column
    })

def obtener_errores_sintactico():
    return tabla_errores

# Función para encontrar la columna del token en la línea
def find_column(input, token,n):
    last_cr = input.rfind('\n', 0, token.lexpos(n))
    if last_cr < 0:
        last_cr = 0
    column = (token.lexpos(n) - last_cr)
    if column == 0:
        return 1 
    return column

def reiniciar_analizador_sintactico():
    global tabla_errores
    tabla_errores = []

# Función para procesar las declaraciones y agregar símbolos a la tabla de símbolos
def procesar_declaracion(declaracion, symbol_table):
    if declaracion[0] == 'declaracion':
        if len(declaracion) == 4:
            symbol = Symbol(name=declaracion[2], category='variable', symbol_type=declaracion[1], attributes={'value': declaracion[3]})
            symbol_table.add(symbol)
        else:
            # Pendiente para otros tipos de declaración
            pass

# Clase para representar el nodo PARA en el árbol sintáctico
class NodoPara:
    def __init__(self, tipo, identificador, inicio, condicion, incremento, bloque):
        self.tipo = tipo
        self.identificador = identificador
        self.inicio = inicio
        self.condicion = condicion
        self.incremento = incremento
        self.bloque = bloque

    def __str__(self):
        return f"PARA {self.tipo} {self.identificador} = {self.inicio}; {self.condicion}; {self.incremento} {{\n{self.bloque}\n}}"

# Evitar la impresión de advertencias sobre tokens no utilizados
yacc.errorlog = yacc.NullLogger()

# Programa principal
def p_programa(p):
    """
    programa : COMENZAR bloque_codigo TERMINAR
    """
    p[0] = ('programa', p[2])
    

# Bloque de código
def p_bloque_codigo(p):
    """
    bloque_codigo : LLAVE_IZQ lista_declaraciones LLAVE_DER
    """
    tabla_simbolos_local = tabla_simbolos_global.enter_scope()
    # Procesar las declaraciones en el ámbito local
    for declaracion in p[2]:
        procesar_declaracion(declaracion, tabla_simbolos_local)
    # Salir del ámbito local al cerrar el bloque de código
    tabla_simbolos_global.exit_scope()
    p[0] = ('bloque_codigo', p[2])
    
# Lista de declaraciones
def p_lista_declaraciones(p):
    """
    lista_declaraciones : lista_declaraciones declaracion 
                        | declaracion
                        | empty
    """
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

# | sonar_alarma
#                 | activar_freno
#                 | esperar
#                 | ajustar_velocidad
# | detener_motor
#                 | verificar_sensor_obstaculos
#                 | calcular_distancia_restante

# Declaración
def p_declaracion(p):
    """
    declaracion : tipo IDENTIFICADOR IGUAL expresion PUNTO_COMA
                | expresion PUNTO_COMA
                | si
                | para
                | mientras
                | mostrar_en_pantalla
                | obstaculo_detectado
                | activar_freno
                | esperar
                | ajustar_velocidad
                | detener_motor
                | sonar_alarma
                | verificar_sensor_obstaculos
                | calcular_distancia_restante
                | motor_encendido
                | velocidad
                | cambiar_direccion
                | verificar_freno
                | distancia_recorrida
                | frenos_activados
                | distancia_restante
                | acelerar
                | nueva_velocidad
                | distancia_objetivo
                | tiempo_transcurrido

                
                
    """
    if len(p) == 6:
        # symbol = Symbol(name=p[2], category='variable', symbol_type=p[1], attributes={'value': p[4]})
        # tabla_simbolos_global.add(symbol)
        p[0] = ('declaracion', p[1], p[2], p[4])
    else:
        p[0] = ('declaracion', p[1])

# Tipos de datos
def p_tipo(p):
    """
    tipo : ENTERO
         | DECIMAL
         | BOOL
         | LISTA
         | DICCIONARIO
    """
    p[0] = p[1]

# Expresiones
def p_expresion(p):
    """
    expresion : expresion operador expresion
              | PARENTESIS_IZQ expresion PARENTESIS_DER
              | IDENTIFICADOR
              | NUMENTERO
              | NUMDECIMAL
              | BOOL
              | CADENA
              | lista
    """
    if len(p) == 4:
        if p[1] == '(':
            p[0] = ('grupo', p[2])
        else:
            p[0] = ('expresion', p[1], p[2], p[3])
    else:
        p[0] = p[1]

# Operadores
def p_operador(p):
    """
    operador : MAS
             | MENOS
             | POR
             | DIVIDIDO
             | IGUAL
             | DIFERENTE
             | MENOR
             | MAYOR
             | MENOR_IGUAL
             | MAYOR_IGUAL
             | Y
             | O
             | NO
    """
    p[0] = p[1]

# Lista
def p_lista(p):
    """
    lista : menor_tipo LLAVE_IZQ valores_lista LLAVE_DER
    """
    p[0] = ('lista', p[1], p[3])

def p_menor_tipo(p):
    """
    menor_tipo : MENOR tipo MAYOR
    """
    p[0] = p[2]

def p_valores_lista(p):
    """
    valores_lista : valores_lista COMA valor_lista
                  | valor_lista
    """
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]

def p_valor_lista(p):
    """
    valor_lista : NUMENTERO
                | NUMDECIMAL
                | BOOL
    """
    p[0] = p[1]

# Estructuras de Control de Flujo
def p_si(p):
    """
    si : SI PARENTESIS_IZQ expresion PARENTESIS_DER bloque_codigo
        | SI PARENTESIS_IZQ expresion Y expresion PARENTESIS_DER bloque_codigo
        | SI PARENTESIS_IZQ expresion O expresion PARENTESIS_DER bloque_codigo
        | SI PARENTESIS_IZQ NO expresion PARENTESIS_DER bloque_codigo
    """
    if len(p) == 6:
        p[0] = ('si', p[3], p[5])
    elif p[4] == 'Y':
        p[0] = ('si_y', p[3], p[5], p[7])
    elif p[4] == 'O':
        p[0] = ('si_o', p[3], p[5], p[7])
    else:
        p[0] = ('si_no', p[4], p[5])

# Estructura de control de flujo PARA
def p_para(p):
    """
    para : PARA PARENTESIS_IZQ tipo IDENTIFICADOR IGUAL expresion PUNTO_COMA expresion PUNTO_COMA expresion PARENTESIS_DER bloque_codigo
    """
    symbol = Symbol(name=p[4], category='variable', symbol_type=p[3], attributes={'value': p[6]},scope='local')
    para_scope.add(symbol)
    p[0] = NodoPara(p[3], p[4], p[6], p[8], p[10], p[12])
    tabla_simbolos_global = para_scope.exit_scope()

# Estructura de control de flujo MIENTRAS
def p_mientras(p):
    """
    mientras : MIENTRAS PARENTESIS_IZQ expresion PARENTESIS_DER bloque_codigo
    """
    p[0] = ('mientras', p[3], p[5])

# Estructura expresion MOSTRAR_EN_PANTALLA
def p_mostrar_en_pantalla(p):
    """
    mostrar_en_pantalla : MOSTRAR_EN_PANTALLA PARENTESIS_IZQ expresion PARENTESIS_DER PUNTO_COMA
    """
    p[0] = ('mostrar_en_pantalla', p[3])

# Estructura expresion OBSTACULO_DETECTADO   
def p_obstaculo_detectado(p):
    """
    obstaculo_detectado : OBSTACULO_DETECTADO PARENTESIS_IZQ PARENTESIS_DER PUNTO_COMA
                        | OBSTACULO_DETECTADO PARENTESIS_IZQ PARENTESIS_DER 
    """
    p[0] = ('obstaculo_detectado',p[1])

# Estructura expresion DETENER_MOTOR
def p_detener_motor(p):
    """
    detener_motor : DETENER_MOTOR PARENTESIS_IZQ PARENTESIS_DER PUNTO_COMA
                    | DETENER_MOTOR PARENTESIS_IZQ PARENTESIS_DER 
    """
    p[0] = ('detener_motor',p[1])

# Estructura expresion MOTOR_ENCENDIDO
def p_motor_encendido(p):
    """
    motor_encendido : MOTOR_ENCENDIDO PARENTESIS_IZQ PARENTESIS_DER PUNTO_COMA
                    | MOTOR_ENCENDIDO PARENTESIS_IZQ PARENTESIS_DER 
    """
    p[0] = ('motor_encendido',p[1])

# Estructura expresion VELOCIDAD
def p_velocidad(p):
    """
    velocidad : VELOCIDAD PARENTESIS_IZQ  PARENTESIS_DER PUNTO_COMA
              | VELOCIDAD PARENTESIS_IZQ  PARENTESIS_DER 
    """
    p[0] = ('velocidad',p[1])

# Estructura expresion CAMBIAR_DIRECCION
def p_cambiar_direccion(p):
    """
    cambiar_direccion : CAMBIAR_DIRECCION PARENTESIS_IZQ PARENTESIS_DER PUNTO_COMA
                      | CAMBIAR_DIRECCION  PARENTESIS_IZQ PARENTESIS_DER 
    """
    p[0] = ('cambiar_direccion',p[1])

# Estructura expresion VERIFICAR_FRENO
def p_verificar_freno(p):
    """
    verificar_freno : VERIFICAR_FRENO PARENTESIS_IZQ PARENTESIS_DER PUNTO_COMA
                    | VERIFICAR_FRENO PARENTESIS_IZQ PARENTESIS_DER 
    """
    p[0] = ('verificar_freno',p[1])

# Estructura expresion DISTANCIA_RECORRIDA
def p_distancia_recorrida(p):
    """
    distancia_recorrida : DISTANCIA_RECORRIDA PARENTESIS_IZQ PARENTESIS_DER PUNTO_COMA
                        | DISTANCIA_RECORRIDA PARENTESIS_IZQ PARENTESIS_DER
                        | DISTANCIA_RECORRIDA  
    """
    p[0] = ('distancia_recorrida',p[1])

# Estructura expresion FRENOS_ACTIVADOS
def p_frenos_activados(p):
    """
    frenos_activados : FRENOS_ACTIVADOS PARENTESIS_IZQ PARENTESIS_DER PUNTO_COMA
                     | FRENOS_ACTIVADOS PARENTESIS_IZQ PARENTESIS_DER 
    """
    p[0] = ('frenos_activados',p[1])

# Estructura expresion CALCULAR_DISTANCIA_RESTANTE
def p_calcular_distancia_restante(p):
    """
    calcular_distancia_restante : CALCULAR_DISTANCIA_RESTANTE PARENTESIS_IZQ PARENTESIS_DER PUNTO_COMA
                                | CALCULAR_DISTANCIA_RESTANTE PARENTESIS_IZQ PARENTESIS_DER 
    """
    p[0] = ('calcular_distancia_restante',p[1])

# Estructura expresion DISTANCIA_RESTANTE
def p_distancia_restante(p):
    """
    distancia_restante : DISTANCIA_RESTANTE PARENTESIS_IZQ PARENTESIS_DER PUNTO_COMA
                       | DISTANCIA_RESTANTE PARENTESIS_IZQ PARENTESIS_DER 
    """
    p[0] = ('distancia_restante',p[1])

# Estructura expresion ACELERAR
def p_acelerar(p):
    """
    acelerar : ACELERAR PARENTESIS_IZQ PARENTESIS_DER PUNTO_COMA
             | ACELERAR PARENTESIS_IZQ PARENTESIS_DER 
    """
    p[0] = ('acelerar',p[1])

# Estructura expresion AJUSTAR_VELOCIDAD
def p_ajustar_velocidad(p):
    """
    ajustar_velocidad : AJUSTAR_VELOCIDAD PARENTESIS_IZQ PARENTESIS_DER PUNTO_COMA
                      | AJUSTAR_VELOCIDAD PARENTESIS_IZQ PARENTESIS_DER 
    """
    p[0] = ('ajustar_velocidad',p[1])

# Estructura expresion NUEVA_VELOCIDAD
def p_nueva_velocidad(p):
    """
    nueva_velocidad : NUEVA_VELOCIDAD PARENTESIS_IZQ PARENTESIS_DER PUNTO_COMA
                    | NUEVA_VELOCIDAD PARENTESIS_IZQ PARENTESIS_DER 
    """
    p[0] = ('nueva_velocidad',p[1])

# Estructura expresion DISTANCIA_OBJETIVO
def p_distancia_objetivo(p):
    """
    distancia_objetivo : DISTANCIA_OBJETIVO PARENTESIS_IZQ PARENTESIS_DER PUNTO_COMA
                       | DISTANCIA_OBJETIVO PARENTESIS_IZQ PARENTESIS_DER 
    """
    p[0] = ('distancia_objetivo',p[1])

# Estructura expresion SONAR_ALARMA
def p_sonar_alarma(p):
    """
    sonar_alarma : SONAR_ALARMA PARENTESIS_IZQ PARENTESIS_DER PUNTO_COMA
                 | SONAR_ALARMA PARENTESIS_IZQ PARENTESIS_DER 
    """
    p[0] = ('sonar_alarma',p[1])

# Estructura expresion ESPERAR
def p_esperar(p):
    """
    esperar : ESPERAR PARENTESIS_IZQ PARENTESIS_DER PUNTO_COMA
            | ESPERAR PARENTESIS_IZQ PARENTESIS_DER 
    """
    p[0] = ('esperar',p[1])

# Estructura expresion VERIFICAR_SENSOR_OBSTACULO
def p_verificar_sensor_obstaculos(p):
    """
    verificar_sensor_obstaculos : VERIFICAR_SENSOR_OBSTACULOS PARENTESIS_IZQ PARENTESIS_DER PUNTO_COMA
                                | VERIFICAR_SENSOR_OBSTACULOS PARENTESIS_IZQ PARENTESIS_DER 
    """
    p[0] = ('verificar_sensor_obstaculos',p[1])

# Estructura expresion TIEMPO_TRANSCURRIDO
def p_tiempo_transcurrido(p):
    """
    tiempo_transcurrido : TIEMPO_TRANSCURRIDO PARENTESIS_IZQ PARENTESIS_DER PUNTO_COMA
                        | TIEMPO_TRANSCURRIDO PARENTESIS_IZQ PARENTESIS_DER 
    """
    p[0] = ('tiempo_transcurrido',p[1])

# Estructura expresion ACTIVAR_FRENO
def p_activar_freno(p):
    """
    activar_freno : ACTIVAR_FRENO PARENTESIS_IZQ PARENTESIS_DER PUNTO_COMA
                  | ACTIVAR_FRENO PARENTESIS_IZQ PARENTESIS_DER 
    """
    p[0] = ('activar_freno',p[1])

def p_empty(p):
    'empty :'
    p[0] = 'VACÍO'


# Manejo de Errores
def p_programa_error(p):
    """
    programa : COMENZAR TERMINAR
    """
    agregar_error_sintactico(11,'Sintactico','Inicio de programa inválido. No se declaró un bloque de código',p[1],p.lineno(1),find_column(p.lexer.lexdata,p,1))
    p[0] = 'Error en programa'
def p_programa_error_2(p):
    """
    programa : COMENZAR lista_declaraciones TERMINAR
    """
    agregar_error_sintactico(11,'Sintactico','Inicio de programa inválido. No se declaró un bloque de código',p[1],p.lineno(1),find_column(p.lexer.lexdata,p,1))
    p[0] = 'Error en programa'
def p_programa_error_3(p):
    """
    programa : lista_declaraciones
    """
    agregar_error_sintactico(11,'Sintactico','Inicio de programa inválido','',1,1)
    p[0] = 'Error en programa'

#>>>>>>>>>>>>>>>>>>>>>> BLOQUE_CODIGO
def p_error_bloque_codigo(p): 
    """
    bloque_codigo : error lista_declaraciones LLAVE_DER
    """
    agregar_error_sintactico(1,'Sintactico','Falta la llave de apertura {',p[1],p.lineno(1),find_column(p.lexer.lexdata,p,1))
    p[0] = 'Error en bloque_codigo'

def p_error_bloque_codigo_2(p):
    """
    bloque_codigo : LLAVE_IZQ lista_declaraciones error
    """
    agregar_error_sintactico(1,'Sintactico','Falta la llave de cierre }',p[3],p.lineno(3),find_column(p.lexer.lexdata,p,3))
    p[0] = 'Error en bloque_codigo'
def p_error_bloque_codigo_3(p):
    """
    bloque_codigo : LLAVE_IZQ error LLAVE_DER
    """
    agregar_error_sintactico(1,'Sintactico','Error en el cuerpo del bloque de codigo',p[2],p.lineno(2),find_column(p.lexer.lexdata,p,2))
    p[0] = 'Error en bloque_codigo'
def p_error_bloque_codigo_4(p):
    """
    bloque_codigo : LLAVE_IZQ error 
    """
    agregar_error_sintactico(1,'Sintactico','Falta la llave de cierre }',p[2],p.lineno(2),find_column(p.lexer.lexdata,p,2))
    p[0] = 'Error en bloque_codigo'
def p_error_bloque_codigo_5(p):
    """
    bloque_codigo : error LLAVE_DER 
    """
    agregar_error_sintactico(1,'Sintactico','Falta la llave de apertura {',p[2],p.lineno(2),find_column(p.lexer.lexdata,p,2))
    p[0] = 'Error en bloque_codigo'

#>>>>>>>>>>>>>>>>>>>>>> EXPRESION
def p_error_expresion(p): #expresion operador expresion
    """
    expresion : error operador expresion
              | expresion error expresion
              | expresion operador error
              | error expresion PARENTESIS_DER
              | PARENTESIS_IZQ error PARENTESIS_DER
              | PARENTESIS_IZQ expresion error
    """
    agregar_error_sintactico(2,'Sintactico','Expresión inválida',p[2],p.lineno(2),p.lexpos(2))
    p[0] = 'Error en expresion'

#>>>>>>>>>>>>>>>>>>>>> DECLARACION
def p_error_declaracion(p):
    """
    declaracion : error IDENTIFICADOR IGUAL expresion PUNTO_COMA
    """
    agregar_error_sintactico(3,'Sintactico','No se indicó el tipo de dato antes de',p[1],p.lineno(1),find_column(p.lexer.lexdata,p,1))
    p[0] = 'Error en declaracion'
def p_error_declaracion_2(p):
    """
    declaracion : tipo error IGUAL expresion PUNTO_COMA
    """
    agregar_error_sintactico(3,'Sintactico','Se esperaba un identificador',p[2],p.lineno(2),find_column(p.lexer.lexdata,p,2))
    p[0] = 'Error en declaracion'
def p_error_declaracion_3(p):
    """
    declaracion : error PUNTO_COMA
                | error expresion PUNTO_COMA
                | NUMENTERO PUNTO_COMA
                | NUMDECIMAL PUNTO_COMA
                | BOOL PUNTO_COMA
                | IDENTIFICADOR PUNTO_COMA
                | CADENA PUNTO_COMA
                | lista PUNTO_COMA
                | NUMENTERO
                | NUMDECIMAL
                | BOOL
                | IDENTIFICADOR
                | CADENA
                | lista
    """
    agregar_error_sintactico(3,'Sintactico','Declaración inválida',p[1],p.lineno(1),find_column(p.lexer.lexdata,p,1))
    p[0] = 'Error en declaracion'
def p_error_declaracion_4(p):
    """
    declaracion : tipo IDENTIFICADOR error expresion PUNTO_COMA
    """
    agregar_error_sintactico(3,'Sintactico','Se esperaba un signo (=) para la declaración',p[4],p.lineno(3),find_column(p.lexer.lexdata,p,3))
    p[0] = 'Error en declaracion'
def p_error_declaracion_5(p):
    """
    declaracion : tipo IDENTIFICADOR IGUAL expresion error
    """
    agregar_error_sintactico(3,'Sintactico','Se esperaba un ;',p[4],p.lineno(3),find_column(p.lexer.lexdata,p,3))
    p[0] = 'Error en declaracion'
def p_error_declaracion_6(p):
    """
    declaracion : tipo expresion PUNTO_COMA
    """
    agregar_error_sintactico(3,'Sintactico','Declaración inválida. No se incializó correctamente la variable',p[2],p.lineno(3),find_column(p.lexer.lexdata,p,3))
    p[0] = 'Error en declaracion'
def p_error_declaracion_7(p):
    """
    declaracion : tipo expresion error
    """
    agregar_error_sintactico(3,'Sintactico','Declaracion inválida',p[2],p.lineno(3)-1,find_column(p.lexer.lexdata,p,3))
    p[0] = 'Error en declaracion'
def p_error_declaracion_8(p):
    """
    declaracion : tipo IDENTIFICADOR IGUAL error
    """
    agregar_error_sintactico(3,'Sintactico','Declaración inválida',p[3],p.lineno(3),find_column(p.lexer.lexdata,p,3))
    p[0] = 'Error en declaracion'
def p_error_declaracion_9(p):
    """
    declaracion : tipo IDENTIFICADOR error
    """
    agregar_error_sintactico(3,'Sintactico','Declaración inválida. Verifique la sintaxis',p[2],p.lineno(2),find_column(p.lexer.lexdata,p,2))
    p[0] = 'Error en declaracion'
def p_error_declaracion_10(p):
    """
    declaracion : tipo error
    """
    agregar_error_sintactico(3,'Sintactico','Declaración inválida. Verifique la ',p[1],p.lineno(2),find_column(p.lexer.lexdata,p,1))
    p[0] = 'Error en declaracion'

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>LISTA
def p_error_lista(p): #LISTA menor_tipo LLAVE_IZQ valores_lista LLAVE_DER
    """
    lista : error menor_tipo LLAVE_IZQ valores_lista LLAVE_DER
          | LISTA error LLAVE_IZQ valores_lista LLAVE_DER
          | LISTA menor_tipo error valores_lista LLAVE_DER
          | LISTA menor_tipo LLAVE_IZQ error LLAVE_DER
          | LISTA menor_tipo LLAVE_IZQ valores_lista error
    """
    agregar_error_sintactico(4,'Sintactico','Declaración inválida. Verifique que la sintaxis de la lista sea correcta',p[2],p.lineno(2),find_column(p.lexer.lexdata,p,2))
    p[0] = 'Error en lista'
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> LISTA ->> <IDENTIFICADOR>
def p_error_menor_tipo(p): #MENOR IDENTIFICADOR MAYOR
    """
    menor_tipo : MENOR error MAYOR
    """
    agregar_error_sintactico(5,'Sintactico','Declaración inválida',p[2],p.lineno(2),find_column(p.lexer.lexdata,p,2))
    p[0] = 'Error en identificador_lista'
def p_error_menor_tipo_2(p): #MENOR IDENTIFICADOR MAYOR
    """
    menor_tipo : MENOR IDENTIFICADOR error
    """
    agregar_error_sintactico(5,'Sintactico','Falta el signo de cierre >',p[2],p.lineno(2),find_column(p.lexer.lexdata,p,2))
    p[0] = 'Error en identificador_lista'
def p_error_menor_tipo_3(p): #MENOR IDENTIFICADOR MAYOR
    """
    menor_tipo : error IDENTIFICADOR MAYOR
    """
    agregar_error_sintactico(5,'Sintactico','Falta el signo de apertura <',p[2],p.lineno(2),find_column(p.lexer.lexdata,p,2))
    p[0] = 'Error en identificador_lista'
#>>>>>>>>>>>>>>>>>>>>>>>> VALORES LISTA
def p_error_valores_lista(p):
    """
    valores_lista : error COMA valor_lista
    """
    agregar_error_sintactico(6,'Sintactico','Valor inválido',p[1],p.lineno(1),find_column(p.lexer.lexdata,p,1))
    p[0] = 'Error en valores_lista'
def p_error_valores_lista_2(p):
    """
    valores_lista : valores_lista COMA error
    """
    agregar_error_sintactico(6,'Sintactico','Valor inválido',p[3],p.lineno(3),find_column(p.lexer.lexdata,p,3))
    p[0] = 'Error en valores_lista'
def p_error_valores_lista_3(p):
    """
    valores_lista : valores_lista error valor_lista
    """
    agregar_error_sintactico(6,'Sintactico','Se esperaba una ","',p[3],p.lineno(3),find_column(p.lexer.lexdata,p,3))
    p[0] = 'Error en valores_lista'

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> CONDICIONAL SI
def p_error_si(p): #SI PARENTESIS_IZQ expresion PARENTESIS_DER bloque_codigo
    """
    si : error PARENTESIS_IZQ expresion PARENTESIS_DER bloque_codigo
                  | SI error expresion PARENTESIS_DER bloque_codigo
                  | SI PARENTESIS_IZQ error PARENTESIS_DER bloque_codigo
                  | SI PARENTESIS_IZQ expresion error bloque_codigo
                  | SI PARENTESIS_IZQ expresion PARENTESIS_DER error
                  | SI PARENTESIS_IZQ expresion error expresion PARENTESIS_DER bloque_codigo
                  | SI PARENTESIS_IZQ error expresion PARENTESIS_DER bloque_codigo
    """
    agregar_error_sintactico(7,'Sintactico','Verifique que la sintaxis de la estructura condicional SI sea correcta',p[1],p.lineno(1),find_column(p.lexer.lexdata,p,1))
    p[0] = 'Error en estructura SI'

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> CICLO PARA
def p_error_para(p): #PARA PARENTESIS_IZQ tipo IDENTIFICADOR IGUAL expresion PUNTO_COMA expresion PUNTO_COMA expresion PARENTESIS_DER bloque_codigo
    """
    para : error PARENTESIS_IZQ tipo IDENTIFICADOR IGUAL expresion PUNTO_COMA expresion PUNTO_COMA expresion PARENTESIS_DER bloque_codigo
         | PARA error tipo IDENTIFICADOR IGUAL expresion PUNTO_COMA expresion PUNTO_COMA expresion PARENTESIS_DER bloque_codigo
         | PARA PARENTESIS_IZQ error IDENTIFICADOR IGUAL expresion PUNTO_COMA expresion PUNTO_COMA expresion PARENTESIS_DER bloque_codigo
         | PARA PARENTESIS_IZQ tipo error IGUAL expresion PUNTO_COMA expresion PUNTO_COMA expresion PARENTESIS_DER bloque_codigo
         | PARA PARENTESIS_IZQ tipo IDENTIFICADOR error expresion PUNTO_COMA expresion PUNTO_COMA expresion PARENTESIS_DER bloque_codigo
         | PARA PARENTESIS_IZQ tipo IDENTIFICADOR IGUAL error PUNTO_COMA expresion PUNTO_COMA expresion PARENTESIS_DER bloque_codigo
         | PARA PARENTESIS_IZQ tipo IDENTIFICADOR IGUAL expresion error expresion PUNTO_COMA expresion PARENTESIS_DER bloque_codigo
         | PARA PARENTESIS_IZQ tipo IDENTIFICADOR IGUAL expresion PUNTO_COMA error PUNTO_COMA expresion PARENTESIS_DER bloque_codigo
         | PARA PARENTESIS_IZQ tipo IDENTIFICADOR IGUAL expresion PUNTO_COMA expresion error expresion PARENTESIS_DER bloque_codigo
         | PARA PARENTESIS_IZQ tipo IDENTIFICADOR IGUAL expresion PUNTO_COMA expresion PUNTO_COMA error PARENTESIS_DER bloque_codigo
         | PARA PARENTESIS_IZQ tipo IDENTIFICADOR IGUAL expresion PUNTO_COMA expresion PUNTO_COMA expresion error bloque_codigo
         | PARA PARENTESIS_IZQ tipo IDENTIFICADOR IGUAL expresion PUNTO_COMA expresion PUNTO_COMA expresion PARENTESIS_DER error
    """
    agregar_error_sintactico(8,'Sintactico','Verifique que la sintaxis de la estructura PARA sea correcta',p[1],p.lineno(1),find_column(p.lexer.lexdata,p,1))
    p[0] = 'Error en ciclo PARA'

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> CICLO MIENTRAS
def p_error_mientras(p): #MIENTRAS PARENTESIS_IZQ expresion PARENTESIS_DER bloque_codigo
    """
    mientras : error PARENTESIS_IZQ expresion PARENTESIS_DER bloque_codigo
             | MIENTRAS error expresion PARENTESIS_DER bloque_codigo
             | MIENTRAS PARENTESIS_IZQ error PARENTESIS_DER bloque_codigo
             | MIENTRAS PARENTESIS_IZQ expresion error bloque_codigo
             | MIENTRAS PARENTESIS_IZQ expresion PARENTESIS_DER error
    """
    agregar_error_sintactico(9,'Sintactico','Verifique que la sintaxis de la estructura MIENTRAS sea correcta',p[1],p.lineno(1),find_column(p.lexer.lexdata,p,1))
    p[0] = 'Error en ciclo MIENTRAS'

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> FUNCION MOSTRAR_EN_PANTALLA
def p_error_mostrar_en_pantalla(p): #MOSTRAR_EN_PANTALLA PARENTESIS_IZQ expresion PARENTESIS_DER PUNTO_COMA
    """
    mostrar_en_pantalla : MOSTRAR_EN_PANTALLA error expresion PARENTESIS_DER PUNTO_COMA
    """
    agregar_error_sintactico(10,'Sintactico','Falta el paréntesis de apertura (',p[2],p.lineno(2),find_column(p.lexer.lexdata,p,2))
    p[0] = 'Error en mostrar_en_pantalla'

def p_error_mostrar_en_pantalla_2(p):
    """
    mostrar_en_pantalla : MOSTRAR_EN_PANTALLA PARENTESIS_IZQ expresion error PUNTO_COMA
    """
    agregar_error_sintactico(10,'Sintactico','Falta el paréntesis de cierre )',p[4],p.lineno(4),find_column(p.lexer.lexdata,p,4))
    p[0] = 'Error en mostrar_en_pantalla'
def p_error_mostrar_en_pantalla_3(p):
    """
    mostrar_en_pantalla : MOSTRAR_EN_PANTALLA PARENTESIS_IZQ expresion PARENTESIS_DER error
    """
    agregar_error_sintactico(10,'Sintactico','Se esperaba el ; al final de la sentencia',p[4],p.lineno(4),find_column(p.lexer.lexdata,p,4))
    p[0] = 'Error en mostrar_en_pantalla'
def p_error_mostrar_en_pantalla_4(p):
    """
    mostrar_en_pantalla : MOSTRAR_EN_PANTALLA PARENTESIS_IZQ error PARENTESIS_DER PUNTO_COMA
    """
    agregar_error_sintactico(10,'Sintactico','Verifique que el argumento para MOSTRAR_EN_PANTALLA sea válido',p[2],p.lineno(2),find_column(p.lexer.lexdata,p,2))
    p[0] = 'Error en mostrar_en_pantalla'

def p_error(p):
    if p:
        # agregar_error_sintactico(1,'Sintactico','🔍',p.value,p.lineno,find_column_lexico(p.lexer.lexdata,p))
        pass
    else:
        agregar_error_sintactico(11,'Sintactico','Inicio de programa inválido. El programa debe iniciar con COMENZAR y finalizar con TERMINAR','','','')


# Construir el analizador

def construir_analizador_sintactico():
    return yacc.yacc()

def tree_to_json(node):
    if isinstance(node, tuple):
        result = {'title': node[0], 'children': []}
        for child in node[1:]:
            child_json = tree_to_json(child)
            if child_json.get('title'):  # Si el hijo tiene un título válido
                result['children'].append(child_json)
            else:  # Si no tiene título, añadir sus hijos directamente
                result['children'].extend(child_json.get('children', []))
        return result
    elif isinstance(node, NodoPara):
        result = {'title': f'PARA {node.tipo} {node.identificador} = {node.inicio}; {node.condicion}; {node.incremento}', 'children': []}
        result['children'].append(tree_to_json(node.bloque))
        return result
    elif isinstance(node, list):
        result = {'children': []}
        for item in node:
            result['children'].append(tree_to_json(item))
        return result
    else:
        return {'title': str(node)}



######################################################ZONA PARA PRUEBAS
# DESCOMENTA CON Ctrl+k+u TODAS LAS LINEAS DE ABAJO PARA PROBAR ESTE ARCHIVO DE MANERA AISLADA

parser = yacc.yacc()
lexer = construir_analizador_lexico()
tokens_analisis=[]
#Función de prueba
def test_parser(input_string):
    
   lexer.input(input_string)
    
   for token in lexer:
       tokens_analisis.append(token)
        
   reiniciar_analizador_lexico(lexer)
   for t in tokens_analisis:
        print(t)
   result = parser.parse(input_string)
   for error in tabla_errores:
       print(error)
   print_tree(result)

#Función para imprimir el árbol sintáctico
def print_tree(node, depth=0):
   if isinstance(node, tuple):
       print("  " * depth + node[0])
       for child in node[1:]:
           print_tree(child, depth + 1)
   elif isinstance(node, NodoPara):
       print("  " * depth + f"PARA {node.tipo} {node.identificador} = {node.inicio}; {node.condicion}; {node.incremento}")
       print_tree(node.bloque, depth + 1)  # Imprimir el bloque de código del nodo
   elif isinstance(node, list):
       for item in node:
           print_tree(item, depth)
   else:
       print("  " * depth + str(node))


# Código de prueba
test_code = """
COMENZAR{

BOOL obstaculo_detectado = F;
DECIMAL distancia_objetivo = 500.0;

MIENTRAS(distancia_recorrida < distancia_objetivo){
    SI(obstaculo_detectado){
        SI(calcular_distancia_restante(distancia_objetivo) < 100){
            DETENER_MOTOR();
            SONAR_ALARMA();
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

test_parser(test_code)
tabla_simbolos_global.print_table()

