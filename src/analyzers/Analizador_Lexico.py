import ply.lex as lex

tabla_errores = []

# Función para reiniciar la lista de errores y los contadores del analizador
def reiniciar_analizador_lexico(lexer):
    global tabla_errores
    tabla_errores = []
    lexer.lineno = 1
    lexer.lexpos = 0

# Función para obtener los errores
def obtener_errores_lexico():
    global tabla_errores
    return tabla_errores

def agregar_error_lexico(error_index, error_type, error_description, value, line, column):
    tabla_errores.append({
        'index': error_index,
        'type': error_type,
        'description': error_description,
        'value': value,
        'line': line,
        'column': column
    })

# Función para encontrar la columna del token en la línea
def find_column_lexico(input, token):
    last_cr = input.rfind('\n', 0, token.lexpos)
    if last_cr < 0:
        last_cr = 0
    column = (token.lexpos - last_cr)
    if column == 0:
        return 1 
    return column

# Manejo de errores para identificadores mal formados
def t_error_IDENTIFICADOR(t):
    r'\d+[a-zA-Z_ñÑ][a-zA-Z0-9_ñÑ]*'
    agregar_error_lexico(12, 'Léxico', 'Identificador inválido', t.value, t.lineno, find_column_lexico(t.lexer.lexdata, t))

def t_error_PUNTO(t):
    r'\.'
    agregar_error_lexico(13, 'Léxico', 'No se esperaba ese carácter en esa posición', t.value, t.lineno, find_column_lexico(t.lexer.lexdata, t))

# Manejo de errores para números enteros inválidos
def t_error_NUMERO_ENTERO(t):
    r'[+-]{2,}\d+'
    agregar_error_lexico(13, 'Léxico', 'Formato de número entero inválido', t.value, t.lineno, find_column_lexico(t.lexer.lexdata, t))

# Manejo de errores para números decimales inválidos
def t_error_NUMERO_DECIMAL(t):
    r'\d+([\.]{2,}\d+[\.|\d]*)+ | \d+\.\d+(\.+\d+)+ | \.+\d+(\.|\d)* | (\d?\.\.\d)+ | \d+\.(?!\d)'
    agregar_error_lexico(13, 'Léxico', 'Formato de número decimal inválido', t.value, t.lineno, find_column_lexico(t.lexer.lexdata, t))

# Manejo de errores para cualquier carácter no reconocido
def t_error(t):
    agregar_error_lexico(13, 'Léxico', 'Carácter no reconocido', t.value[0], t.lineno, find_column_lexico(t.lexer.lexdata, t))
    t.lexer.skip(1)

# Definición de tokens
tokens = [
    'COMENZAR',
    'TERMINAR',
    'MIENTRAS',
    'ENTERO',
    'NUMENTERO',
    'DECIMAL',
    'NUMDECIMAL',
    'BOOL',
    'IDENTIFICADOR',
    'IGUAL',
    'MENOR',
    'MAYOR',
    'MAS',
    'MENOS',
    'POR',
    'DIVIDIDO',
    'PARENTESIS_IZQ',
    'PARENTESIS_DER',
    'LLAVE_IZQ',
    'LLAVE_DER',
    'COMA',
    'PUNTO_COMA',
    'ESPERAR',
    'SONAR_ALERTA',
    'DETENER_MOTOR',
    'ACTIVAR_FRENO',
    'VERIFICAR_SENSOR_OBSTACULOS',
    'AJUSTAR_VELOCIDAD',
    'CALCULAR_DISTANCIA_RESTANTE',
    'SI',
    'SINO',
    'OBSTACULO_DETECTADO',
    'ASIGNACION'
]

# Expresiones regulares para tokens simples
t_IGUAL = r'='
t_MAS = r'\+'
t_MENOS = r'-'
t_POR = r'\*'
t_DIVIDIDO = r'/'
t_MENOR = r'<'
t_MAYOR = r'>'
t_PARENTESIS_IZQ = r'\('
t_PARENTESIS_DER = r'\)'
t_LLAVE_IZQ = r'\{'
t_LLAVE_DER = r'\}'
t_COMA = r','
t_PUNTO_COMA = r';'
t_ASIGNACION = r':='

# Expresión regular para palabras clave específicas
def t_COMENZAR(t):
    r'COMENZAR'
    return t

def t_TERMINAR(t):
    r'TERMINAR'
    return t

def t_MIENTRAS(t):
    r'MIENTRAS'
    return t

def t_SI(t):
    r'SI'
    return t

def t_SINO(t):
    r'SINO'
    return t

def t_OBSTACULO_DETECTADO(t):
    r'obstaculo_detectado'
    return t

def t_ESPERAR(t):
    r'ESPERAR'
    return t

def t_SONAR_ALERTA(t):
    r'SONAR_ALERTA'
    return t

def t_DETENER_MOTOR(t):
    r'detener_motor'
    return t

def t_ACTIVAR_FRENO(t):
    r'activar_freno'
    return t

def t_VERIFICAR_SENSOR_OBSTACULOS(t):
    r'verificar_sensor_obstaculos'
    return t

def t_AJUSTAR_VELOCIDAD(t):
    r'ajustar_velocidad'
    return t

def t_CALCULAR_DISTANCIA_RESTANTE(t):
    r'calcular_distancia_restante'
    return t

# Expresión regular para números decimales
def t_NUMDECIMAL(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

# Expresión regular para números enteros
def t_NUMENTERO(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Expresión regular para booleanos
def t_BOOL(t):
    r'[Vv]|[Ff]'
    t.value = True if t.value.lower() == 'v' else False
    return t

# Expresión regular para identificadores (nombres de variables, funciones, etc.)
def t_IDENTIFICADOR(t):
    r'[a-zA-Z_ñÑ][a-zA-Z0-9_ñÑ]*'
    keywords = {
        'COMENZAR': 'COMENZAR',
        'TERMINAR': 'TERMINAR',
        'MIENTRAS': 'MIENTRAS',
        'SI': 'SI',
        'SINO': 'SINO',
        'ESPERAR': 'ESPERAR',
        'SONAR_ALERTA': 'SONAR_ALERTA',
        'DETENER_MOTOR': 'DETENER_MOTOR',
        'ACTIVAR_FRENO': 'ACTIVAR_FRENO',
        'VERIFICAR_SENSOR_OBSTACULOS': 'VERIFICAR_SENSOR_OBSTACULOS',
        'AJUSTAR_VELOCIDAD': 'AJUSTAR_VELOCIDAD',
        'CALCULAR_DISTANCIA_RESTANTE': 'CALCULAR_DISTANCIA_RESTANTE'
    }
    t.type = keywords.get(t.value, 'IDENTIFICADOR')
    return t

# Expresión regular para cadenas entre comillas dobles
def t_CADENA(t):
    r'"([^"\n]|(\\"))*"'
    return t

# Manejo de errores para cadenas no cerradas
def t_error_CADENA(t):
    r'"(?:\\.|[^\n\"])*[^"]?'
    agregar_error_lexico(13, 'Léxico', 'Cadena no cerrada', t.value, t.lineno, find_column_lexico(t.lexer.lexdata, t))
    t.lexer.skip(1)

# Expresión regular para comentarios
def t_COMENTARIO(t):
    r'\/\/.*'
    pass  # Ignora los comentarios

# Expresión regular para nueva línea
def t_NUEVA_LINEA(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')
    pass  

# Ignorar espacios en blanco y tabulaciones
t_ignore = ' \t'

# Construcción del analizador léxico
def construir_analizador_lexico():
    return lex.lex()

# Ejemplo de uso
if __name__ == "__main__":
    # Prueba del analizador léxico
    data = '''
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
    '''

    # Construcción del analizador léxico
    lexer = construir_analizador_lexico()
    reiniciar_analizador_lexico(lexer)
    lexer.input(data)

    # Análisis de tokens
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)

    # Mostrar errores léxicos
    errores = obtener_errores_lexico()
    for error in errores:
        print(f"Error en línea {error['line']}, columna {error['column']}: {error['description']} ('{error['value']}')")


