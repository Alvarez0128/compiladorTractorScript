class Symbol:
    def __init__(self, name, category, symbol_type, scope="global", attributes=None, parameters=None):
        self.name = name
        self.category = category  # 'variable', 'function'
        self.type = symbol_type  # 'int', 'bool', 'void' para funciones, etc.
        self.scope = scope
        self.attributes = attributes if attributes else {}  # Atributos adicionales, como valor para variables
        self.parameters = parameters if parameters else []  # Parámetros para funciones

    def __str__(self):
        return f"Symbol(name={self.name}, category={self.category}, type={self.type}, scope={self.scope}, attributes={self.attributes}, parameters={self.parameters})"

class SymbolTable:
    def __init__(self, parent=None):
        self.symbols = {}
        self.parent = parent
        self.children = []  # Mantener un registro de tablas de símbolos hijas para ámbitos anidados

    def add(self, symbol):
        if symbol.name in self.symbols:
            self.symbols[symbol.name].append(symbol)
        else:
            self.symbols[symbol.name] = [symbol]

    def get(self, name, category=None):
        # Buscar en la tabla actual
        symbol = self.symbols.get(name, None)
        if symbol and category == 'function':
            # Si se busca específicamente una función, se devuelve la lista de funciones sobrecargadas
            return symbol if isinstance(symbol, list) else None
        if symbol is None and self.parent is not None:
            # Si no se encuentra, buscar en la tabla del ámbito padre
            return self.parent.get(name, category)
        return symbol

    def exists(self, name, category=None):
        exists_in_current_scope = name in self.symbols
        if category == 'function':
            # Verificar si existe como función (considerando la sobrecarga)
            exists_in_current_scope = exists_in_current_scope and isinstance(self.symbols.get(name, None), list)
        return exists_in_current_scope or (self.parent and self.parent.exists(name, category))

    def lookup(self, name):
        # Buscar en la tabla de símbolos actual
        symbol = self.symbols.get(name, None)
        if symbol is not None:
            return symbol[0] if isinstance(symbol, list) else symbol
        # Si no se encuentra, buscar en el ámbito padre
        if self.parent is not None:
            return self.parent.lookup(name)
        return None

    def enter_scope(self):
        # Crea una nueva tabla de símbolos para el nuevo ámbito, con `self` como padre
        new_scope = SymbolTable(parent=self)
        self.children.append(new_scope)
        return new_scope

    def exit_scope(self):
        # Retorna a la tabla de símbolos del ámbito padre
        return self.parent

    def __str__(self):
        symbols_str = ', '.join([str(symbol) for symbol in self.symbols.values()])
        return f"SymbolTable(symbols=[{symbols_str}], parent={self.parent is not None}, children={len(self.children)})"

    def print_table(self, level=0):
        indent = "  " * level
        print(f"{indent}SymbolTable:")
        for name, symbol in self.symbols.items():
            if isinstance(symbol, list):
                for func in symbol:
                    print(f"{indent}  {func}")
            else:
                print(f"{indent}  {symbol}")
        for child in self.children:
            child.print_table(level + 1)
