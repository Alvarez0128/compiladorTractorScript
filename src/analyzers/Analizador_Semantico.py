from SymbolTable import SymbolTable
import Analizador_Sintactico
import Analizador_Lexico

def check_assignment(symbol_table, identifier, value, line_number):
    """
    Verifica la validez de una asignación asegurando que la variable está declarada y que el tipo de valor asignado es compatible.
    Args:
        symbol_table (SymbolTable): La tabla de símbolos en uso.
        identifier (str): El identificador de la variable a la cual se asigna el valor.
        value (any): El valor que se asigna.
        line_number (int): Línea en el código fuente donde ocurre la asignación.
    Raises:
        Exception: Si la variable no está declarada, si el tipo de valor no es compatible o si se intenta modificar una constante.
    """
    symbol = symbol_table.get(identifier)
    if not symbol:
        raise Exception(f"Error: Variable '{identifier}' no declarada en la línea {line_number}")
    if symbol.attributes.get('constant', False):
        raise Exception(f"Error semántico: Intento de modificar la constante '{identifier}' en la línea {line_number}")
    if type(value).__name__ != symbol.type:
        raise Exception(f"Error de tipo: Asignación de un valor de tipo {type(value).__name__} a una variable de tipo {symbol.type} en la línea {line_number}")
    symbol.attributes['value'] = value

def check_expression(symbol_table, expr):
    """
    Evalúa y verifica el tipo de una expresión, asegurando la compatibilidad entre operaciones.
    Args:
        symbol_table (SymbolTable): La tabla de símbolos en uso.
        expr (tuple|str): Expresión para evaluar.
    Returns:
        str: Tipo de la expresión evaluada.
    Raises:
        Exception: Si los tipos dentro de la expresión son incompatibles o si una variable no está declarada.
    """
    if isinstance(expr, tuple):
        left, operator, right = expr
        left_type = check_expression(symbol_table, left)
        right_type = check_expression(symbol_table, right)
        # Realizar verificación de tipos según el operador
        if operator in ['+', '-', '*', '/']:
            # Operadores aritméticos
            if left_type not in ['int', 'float'] or right_type not in ['int', 'float']:
                raise Exception(f"Error de tipo: Operación aritmética entre tipos incompatibles {left_type} y {right_type}")
            # El resultado de la operación será el tipo más amplio entre los operandos
            return 'float' if 'float' in [left_type, right_type] else 'int'
        elif operator in ['==', '!=', '<', '>', '<=', '>=']:
            # Operadores de comparación
            if left_type != right_type:
                raise Exception(f"Error de tipo: Comparación entre tipos incompatibles {left_type} y {right_type}")
            return 'bool'
        elif operator in ['and', 'or', 'not']:
            # Operadores lógicos
            if left_type != 'bool' or (operator != 'not' and right_type != 'bool'):
                raise Exception(f"Error de tipo: Operación lógica entre tipos incompatibles {left_type} y {right_type}")
            return 'bool'
        else:
            raise Exception(f"Error: Operador '{operator}' no reconocido")
    elif isinstance(expr, str):
        symbol = symbol_table.get(expr)
        if not symbol:
            raise Exception(f"Error: Variable '{expr}' no declarada")
        return symbol.type
    else:
        # Si la expresión es un valor constante, devolvemos su tipo
        return type(expr).__name__



def check_scope_and_declaration(symbol_table, identifier, line_number):
    """
    Verifica que un identificador esté declarado y sea accesible en el ámbito actual.
    Args:
        symbol_table (SymbolTable): La tabla de símbolos en uso.
        identifier (str): El identificador a verificar.
        line_number (int): Línea en el código fuente donde se verifica el identificador.
    Raises:
        Exception: Si el identificador no está declarado o no es accesible.
    """
    if not symbol_table.exists(identifier):
        raise Exception(f"Error: Uso no declarado de '{identifier}' en la línea {line_number}")

def check_function_call(symbol_table, function_name, args, line_number):
    """
    Verifica que una llamada a función sea correcta en términos del número y tipo de argumentos.
    Args:
        symbol_table (SymbolTable): La tabla de símbolos en uso.
        function_name (str): El nombre de la función.
        args (list): Argumentos proporcionados en la llamada.
        line_number (int): Línea en el código fuente donde ocurre la llamada.
    Raises:
        Exception: Si la función no está declarada o si los tipos de argumentos no coinciden.
    """
    functions = symbol_table.get(function_name, category='function')
    if not functions:
        raise Exception(f"Error: Función '{function_name}' no declarada en la línea {line_number}")
    for function in functions:
        if len(function.parameters) == len(args):
            for param, arg in zip(function.parameters, args):
                arg_type = check_expression(symbol_table, arg)
                if param['type'] != arg_type:
                    raise Exception(f"Error de tipo: Se esperaba un argumento de tipo {param['type']} pero se recibió tipo {arg_type} en la línea {line_number}")
            return
    raise Exception(f"Error: Ninguna sobrecarga de la función '{function_name}' coincide con los argumentos dados en la línea {line_number}")


def check_control_structure(symbol_table, condition, line_number):
    """
    Verifica que las condiciones en estructuras de control como if, while sean booleanas.
    Args:
        symbol_table (SymbolTable): La tabla de símbolos en uso.
        condition: Condición para evaluar.
        line_number (int): Línea en el código fuente donde se evalúa la condición.
    Raises:
        Exception: Si la condición evaluada no es de tipo booleano.
    """
    if isinstance(condition, tuple):
        left, operator, right = condition
        check_expression(symbol_table, left)
        check_expression(symbol_table, right)
    else:
        check_expression(symbol_table, condition)

def check_scope_exit(symbol_table, scope_level):
    """
    Verifica que la salida de un ámbito sea coherente con el ámbito actual.
    Args:
        symbol_table (SymbolTable): La tabla de símbolos en uso.
        scope_level: Nivel de ámbito que se pretende salir.
    Raises:
        Exception: Si el ámbito actual no coincide con el ámbito que se intenta salir.
    """
    if symbol_table.current_scope() != scope_level:
        raise Exception("Error semántico: Desajuste de ámbito al intentar salir del bloque de código.")
    symbol_table.exit_scope()

def check_constant_modification(symbol_table, identifier, line_number):
    """
    Verifica que no se modifiquen constantes.
    Args:
        symbol_table (SymbolTable): La tabla de símbolos en uso.
        identifier (str): Identificador de la constante.
        line_number (int): Línea en el código fuente donde se intenta la modificación.
    Raises:
        Exception: Si se intenta modificar una constante.
    """
    symbol = symbol_table.get(identifier)
    if symbol and symbol.attributes.get('constant', False):
        raise Exception(f"Error semántico: Intento de modificar la constante '{identifier}' en la línea {line_number}")

def main():
    # Suponemos que tenemos un symbol_table disponible
    symbol_table = SymbolTable()
    # Añadir simbolos y luego verificar algo con las funciones aquí arriba

if __name__ == "__main__":
    main()
