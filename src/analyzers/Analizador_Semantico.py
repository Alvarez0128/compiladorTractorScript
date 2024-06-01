from SymbolTable import SymbolTable
import Analizador_Sintactico
import Analizador_Lexico

# Definición de excepciones personalizadas para diferentes tipos de errores semánticos.
class SemanticError(Exception):
    def __init__(self, message, line_number):
        super().__init__(f"{message} (Línea {line_number})")

class UndeclaredVariableError(SemanticError):
    pass

class ConstantModificationError(SemanticError):
    pass

class TypeError(SemanticError):
    pass

class FunctionCallError(SemanticError):
    pass

class ScopeError(SemanticError):
    pass

def check_assignment(symbol_table, identifier, value, line_number):
    """
    Verifica la validez de una asignación asegurando que la variable está declarada y que el tipo de valor asignado es compatible.
    Args:
        symbol_table (SymbolTable): La tabla de símbolos en uso.
        identifier (str): El identificador de la variable a la cual se asigna el valor.
        value (any): El valor que se asigna.
        line_number (int): Línea en el código fuente donde ocurre la asignación.
    Raises:
        UndeclaredVariableError: Si la variable no está declarada.
        ConstantModificationError: Si se intenta modificar una constante.
        TypeError: Si el tipo de valor no es compatible.
    """
    symbol = symbol_table.get(identifier)
    if not symbol:
        raise UndeclaredVariableError(f"Variable '{identifier}' no declarada", line_number)
    if symbol.attributes.get('constant', False):
        raise ConstantModificationError(f"Intento de modificar la constante '{identifier}'", line_number)
    if type(value).__name__ != symbol.type:
        raise TypeError(f"Asignación de un valor de tipo {type(value).__name__} a una variable de tipo {symbol.type}", line_number)
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
        TypeError: Si los tipos dentro de la expresión son incompatibles.
        UndeclaredVariableError: Si una variable no está declarada.
        SemanticError: Si se encuentra un operador no reconocido.
    """
    if isinstance(expr, tuple):
        left, operator, right = expr
        left_type = check_expression(symbol_table, left)
        right_type = check_expression(symbol_table, right)
        # Verificación de tipos según el operador
        if operator in ['+', '-', '*', '/']:
            # Operadores aritméticos
            if left_type not in ['int', 'float'] or right_type not in ['int', 'float']:
                raise TypeError(f"Operación aritmética entre tipos incompatibles {left_type} y {right_type}", -1)  # Línea no especificada
            return 'float' if 'float' in [left_type, right_type] else 'int'
        elif operator in ['==', '!=', '<', '>', '<=', '>=']:
            # Operadores de comparación
            if left_type != right_type:
                raise TypeError(f"Comparación entre tipos incompatibles {left_type} y {right_type}", -1)  # Línea no especificada
            return 'bool'
        elif operator in ['and', 'or', 'not']:
            # Operadores lógicos
            if left_type != 'bool' or (operator != 'not' and right_type != 'bool'):
                raise TypeError(f"Operación lógica entre tipos incompatibles {left_type} y {right_type}", -1)  # Línea no especificada
            return 'bool'
        else:
            raise SemanticError(f"Operador '{operator}' no reconocido", -1)  # Línea no especificada
    elif isinstance(expr, str):
        symbol = symbol_table.get(expr)
        if not symbol:
            raise UndeclaredVariableError(f"Variable '{expr}' no declarada", -1)  # Línea no especificada
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
        UndeclaredVariableError: Si el identificador no está declarado.
    """
    if not symbol_table.exists(identifier):
        raise UndeclaredVariableError(f"Uso no declarado de '{identifier}'", line_number)

def check_function_call(symbol_table, function_name, args, line_number):
    """
    Verifica que una llamada a función sea correcta en términos del número y tipo de argumentos.
    Args:
        symbol_table (SymbolTable): La tabla de símbolos en uso.
        function_name (str): El nombre de la función.
        args (list): Argumentos proporcionados en la llamada.
        line_number (int): Línea en el código fuente donde ocurre la llamada.
    Raises:
        FunctionCallError: Si la función no está declarada o si los tipos de argumentos no coinciden.
        TypeError: Si el tipo de algún argumento no coincide con el tipo esperado.
    """
    functions = symbol_table.get(function_name, category='function')
    if not functions:
        raise FunctionCallError(f"Función '{function_name}' no declarada", line_number)
    for function in functions:
        if len(function.parameters) == len(args):
            for param, arg in zip(function.parameters, args):
                arg_type = check_expression(symbol_table, arg)
                if param['type'] != arg_type:
                    raise TypeError(f"Se esperaba un argumento de tipo {param['type']} pero se recibió tipo {arg_type}", line_number)
            return
    raise FunctionCallError(f"Ninguna sobrecarga de la función '{function_name}' coincide con los argumentos dados", line_number)

def check_control_structure(symbol_table, condition, line_number):
    """
    Verifica que las condiciones en estructuras de control como if, while sean booleanas.
    Args:
        symbol_table (SymbolTable): La tabla de símbolos en uso.
        condition: Condición para evaluar.
        line_number (int): Línea en el código fuente donde se evalúa la condición.
    Raises:
        TypeError: Si la condición evaluada no es de tipo booleano.
    """
    condition_type = check_expression(symbol_table, condition)
    if condition_type != 'bool':
        raise TypeError(f"La condición en una estructura de control debe ser booleana, pero se recibió {condition_type}", line_number)

def check_scope_exit(symbol_table, scope_level, line_number):
    """
    Verifica que la salida de un ámbito sea coherente con el ámbito actual.
    Args:
        symbol_table (SymbolTable): La tabla de símbolos en uso.
        scope_level: Nivel de ámbito que se pretende salir.
        line_number (int): Línea en el código fuente donde ocurre la salida de ámbito.
    Raises:
        ScopeError: Si el ámbito actual no coincide con el ámbito que se intenta salir.
    """
    if symbol_table.current_scope() != scope_level:
        raise ScopeError(f"Desajuste de ámbito al intentar salir del bloque de código.", line_number)
    symbol_table.exit_scope()

def check_constant_modification(symbol_table, identifier, line_number):
    """
    Verifica que no se modifiquen constantes.
    Args:
        symbol_table (SymbolTable): La tabla de símbolos en uso.
        identifier (str): Identificador de la constante.
        line_number (int): Línea en el código fuente donde se intenta la modificación.
    Raises:
        ConstantModificationError: Si se intenta modificar una constante.
    """
    symbol = symbol_table.get(identifier)
    if symbol and symbol.attributes.get('constant', False):
        raise ConstantModificationError(f"Intento de modificar la constante '{identifier}'", line_number)

def main():
    # Punto de entrada principal del programa.
    # Aquí se inicializa la tabla de símbolos y se pueden añadir símbolos para verificar con las funciones anteriores.
    symbol_table = SymbolTable()
    # Añadir símbolos y luego verificar algo con las funciones aquí arriba

if __name__ == "__main__":
    main()