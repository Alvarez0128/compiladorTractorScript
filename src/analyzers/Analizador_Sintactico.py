from flask import jsonify
import ply.yacc as yacc
from Analizador_Lexico import tokens, find_column # Importa tokens desde tu archivo léxico


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
    p[0] = ('bloque_codigo', p[2])

# Lista de declaraciones
def p_lista_declaraciones(p):
    """
    lista_declaraciones : lista_declaraciones declaracion 
                        | declaracion
    """
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

# Declaración
def p_declaracion(p):
    """
    declaracion : tipo IDENTIFICADOR IGUAL expresion PUNTO_COMA
                | expresion PUNTO_COMA
                | si
                | para
                | mientras
                | mostrar_en_pantalla
    """
    if len(p) == 6:
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
              | ENTERO
              | DECIMAL
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
    lista : LISTA menor_tipo LLAVE_IZQ valores_lista LLAVE_DER
    """
    p[0] = ('lista', p[2], p[4])

def p_menor_tipo(p):
    """
    menor_tipo : MENOR IDENTIFICADOR MAYOR
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
    valor_lista : ENTERO
                | DECIMAL
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
    p[0] = NodoPara(p[3], p[4], p[6], p[8], p[10], p[12])

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
    
# Manejo de Errores

errors=[]
def p_error(p):
    global errors
    if p:
        errors.append({
            'type': 'Error de sintaxis en ',
            'value': p.value,
            'line': p.lineno,
            'column': find_column(p.lexer.lexdata, p)
        })
        #print(f"Error de sintaxis en '{p.value}', línea {p.lineno}")
    # else:
    #     errors.append({
    #         'type': 'Error de sintaxis: expresión incompleta',
    #         'value': '',
    #         'line': '',
    #         'column': ''
    #     })

# Construir el analizador
# parser = yacc.yacc()
def construir_analizador_sintactico():
    return yacc.yacc()

# Función para obtener los errores y limpiar la lista de errores
def obtener_errores_sintactico():
    global errors
    errores = list(errors)
    errors.clear()
    return errores

def tree_to_string(node, depth=0):
    result = ""
    if isinstance(node, tuple):
        result += "  " * depth + node[0] + "\n"
        for child in node[1:]:
            result += tree_to_string(child, depth + 1)
    elif isinstance(node, NodoPara):
        result += "  " * depth + f"PARA {node.tipo} {node.identificador} = {node.inicio}; {node.condicion}; {node.incremento}\n"
        result += tree_to_string(node.bloque, depth + 1)  # Imprimir el bloque de código del nodo
    elif isinstance(node, list):
        for item in node:
            result += tree_to_string(item, depth)
    else:
        result += "  " * depth + str(node) + "\n"
    return result

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

def tree_to_json_string(node):
    return jsonify(tree_to_json(node))



######################################################
# Función de prueba
# def test_parser(input_string):
#     result = parser.parse(input_string)
#     #print_tree(result)

# Función para imprimir el árbol sintáctico
# def print_tree(node, depth=0):
#     if isinstance(node, tuple):
#         print("  " * depth + node[0])
#         for child in node[1:]:
#             print_tree(child, depth + 1)
#     elif isinstance(node, NodoPara):
#         print("  " * depth + f"PARA {node.tipo} {node.identificador} = {node.inicio}; {node.condicion}; {node.incremento}")
#         print_tree(node.bloque, depth + 1)  # Imprimir el bloque de código del nodo
#     elif isinstance(node, list):
#         for item in node:
#             print_tree(item, depth)
#     else:
#         print("  " * depth + str(node))


# # Código de prueba
# test_code = """
# COMENZAR{
#     ENTERO contador = 0;
#     ENTERO s = 0;
# PARA(ENTERO contador = 0; contador < 10; contador = contador + 1){
#     MOSTRAR_EN_PANTALLA(contador);
#     ENTERO s = 0;
# }

# }
# TERMINAR
# """

# test_parser(test_code)
