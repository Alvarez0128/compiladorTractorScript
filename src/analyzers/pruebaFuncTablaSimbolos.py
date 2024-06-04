# Crear la tabla de símbolos global
from SymbolTable import Symbol, SymbolTable


global_symbol_table = SymbolTable()

# Simular la entrada a una función
function_scope = global_symbol_table.enter_scope()

# Añadir símbolos a la tabla del ámbito de la función
function_scope.add(Symbol(name="x", category="variable", symbol_type="int", scope="local"))
function_scope.add(Symbol(name="y", category="variable", symbol_type="int", scope="local"))

# Imprimir el estado actual de la tabla de símbolos
print("Después de entrar al ámbito de la función:")
global_symbol_table.print_table()

# Simular la entrada a un bloque if dentro de la función
if_scope = function_scope.enter_scope()

# Añadir símbolos al ámbito del bloque if
if_scope.add(Symbol(name="z", category="variable", symbol_type="int", scope="local"))

# Imprimir el estado actual de la tabla de símbolos
print("Después de entrar al ámbito del bloque if:")
global_symbol_table.print_table()

# Salir del ámbito del bloque if
function_scope = if_scope.exit_scope()

# Imprimir el estado actual de la tabla de símbolos
print("Después de salir del ámbito del bloque if:")
global_symbol_table.print_table()

# Salir del ámbito de la función
global_symbol_table = function_scope.exit_scope()

# Imprimir el estado final de la tabla de símbolos
print("Después de salir del ámbito de la función:")
global_symbol_table.print_table()
