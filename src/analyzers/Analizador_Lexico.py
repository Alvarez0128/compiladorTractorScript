import ply.lex as lex

# Función para reiniciar la lista de errores y los contadores del analizador
def reiniciar_analizador_lexico(lexer):
    # global errors
    # errors = []
    lexer.lineno = 1
    lexer.lexpos = 0
    
# Función para encontrar la columna del token en la línea
def find_column(input, token):
    last_cr = input.rfind('\n', 0, token.lexpos)
    if last_cr < 0:
        last_cr = 0
    column = (token.lexpos - last_cr)
    if column == 0:
        return 1 
    return column

# Lista de errores
errors = []

# USO DE AUTOMATAS FINITOS PARA EL MANEJO DE ERRORES

# Manejo de errores para identificadores mal formados
def t_error_IDENTIFICADOR(t):
    r'\d+[a-zA-Z_ñÑ][a-zA-Z0-9_ñÑ]*'
    errors.append({
        'type': 'Error: Identificador inválido',
        'value': t.value,
        'line': t.lineno,
        'column': find_column(t.lexer.lexdata, t)
    })
    # t.lexer.skip(1)

# Manejo de errores para números enteros invalidos
def t_error_NUMERO_ENTERO(t):
    r'[+-]{2,}\d+'
    errors.append({
        'type': 'Error: Formato de número entero inválido',
        'value': t.value,
        'line': t.lineno,
        'column': find_column(t.lexer.lexdata, t)
    })
    # t.lexer.skip(1)

# Manejo de errores para números decimales invalidos
def t_error_NUMERO_DECIMAL(t):
    r'\d+([\.]{2,}[a-zA-Z0-9_ñÑ]+[\.|[a-zA-Z0-9_ñÑ]]*)+ | \d+\.[a-zA-Z0-9_ñÑ]+(\.+[a-zA-Z0-9_ñÑ]+)+ | \.+[a-zA-Z0-9_ñÑ]+(\.|[a-zA-Z0-9_ñÑ])* '
    errors.append({
        'type': 'Error: Formato de número decimal inválido',
        'value': t.value,
        'line': t.lineno,
        'column': find_column(t.lexer.lexdata, t)
    })

# Manejo de errores para símbolos no reconocidos
def t_error(t):
    errors.append({
        'type': 'Error: Símbolo no reconocido',
        'value': t.value[0],
        'line': t.lineno,
        'column': find_column(t.lexer.lexdata, t)
    })
    t.lexer.skip(1)


# Definición de tokens
tokens = [
    'COMENZAR',
    'TERMINAR',
    'PARA',
    'MIENTRAS',
    'ENTERO',
    'DECIMAL',
    'BOOL',
    'IDENTIFICADOR',
    'LISTA',
    'DICCIONARIO',
    'A_CADENA',
    'MOSTRAR_EN_PANTALLA',
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
    'CORCHETE_IZQ',
    'CORCHETE_DER',
    'COMA',
    'DOS_PUNTOS',
    'PUNTO_COMA',
    'COMENTARIO',
    'NUEVA_LINEA',
    'INTENTAR',
    'CAPTURAR',
    'EXCEPCION',
    'FUNCION',
    'CODIGO',
    'RETORNA',
    'ASIGNAR',
    'DIFERENTE',
    'MENOR_IGUAL',
    'MAYOR_IGUAL',
    'Y',
    'O',
    'NO',
    'CADENA',
    'SI',
    'SINO'
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
t_CORCHETE_IZQ = r'\['
t_CORCHETE_DER = r'\]'
t_COMA = r','
t_DOS_PUNTOS = r':'
t_PUNTO_COMA = r';'

# expresiones regulares para operadores de comparación y lógicos
t_ASIGNAR = r'=='
t_DIFERENTE = r'!='
t_MENOR_IGUAL = r'<='
t_MAYOR_IGUAL = r'>='
t_Y = r'[Yy]'
t_O = r'[Oo]'
t_NO = r'[Nn][Oo]'

# Expresión regular para números decimales
def t_DECIMAL(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

# Expresión regular para números enteros
def t_ENTERO(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Expresión regular para booleanos
def t_BOOL(t):
    r'[Vv]alor|[Ff]also'
    t.value = True if t.value.lower() == 'valor' else False
    return t

# Expresión regular para identificadores (nombres de variables, funciones, etc.)
def t_IDENTIFICADOR(t):
    r'[a-zA-Z_ñÑ][a-zA-Z0-9_ñÑ]*'
    keywords = {
        'COMENZAR': 'COMENZAR',
        'TERMINAR': 'TERMINAR',
        'PARA': 'PARA',
        'MIENTRAS': 'MIENTRAS',
        'SI': 'SI',
        'SINO': 'SINO',
        'ENTERO': 'ENTERO',
        'DECIMAL': 'DECIMAL',
        'BOOL': 'BOOL',
        'LISTA': 'LISTA',
        'DICCIONARIO': 'DICCIONARIO',
        'A_CADENA': 'A_CADENA',
        'MOSTRAR_EN_PANTALLA': 'MOSTRAR_EN_PANTALLA',
        'INTENTAR': 'INTENTAR',
        'CAPTURAR': 'CAPTURAR',
        'EXCEPCION': 'EXCEPCION',
        'FUNCION': 'FUNCION',
        'CODIGO': 'CODIGO',
        'RETORNA': 'RETORNA'
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
    errors.append({
        'type': 'Error: Cadena no cerrada',
        'value': t.value,
        'line': t.lineno,
        'column': find_column(t.lexer.lexdata, t)
    })
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
lexer = lex.lex()
# Construcción del analizador léxico
def construir_analizador_lexico():
    return lex.lex()

# Función para obtener los errores y limpiar la lista de errores
def obtener_errores_lexico():
    global errors
    errores = list(errors)
    errors.clear()
    return errores