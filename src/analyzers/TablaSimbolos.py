# TablaSimbolos.py

class TablaSimbolos:
    def __init__(self):
        self.tabla = [{}]  # Pila de ámbitos

    def abrir_ambito(self):
        self.tabla.append({})

    def cerrar_ambito(self):
        if len(self.tabla) > 1:
            self.tabla.pop()
        else:
            raise Exception("Error: No se puede cerrar el ámbito global.")

    def declarar(self, nombre, tipo, valor=None):
        # Declarar variable solo en el ámbito actual
        ambito_actual = self.tabla[-1]
        if nombre in ambito_actual:
            raise Exception(f"Error: Variable '{nombre}' ya declarada en el ámbito actual.")
        ambito_actual[nombre] = {'tipo': tipo, 'valor': valor}

    def asignar(self, nombre, valor):
        for ambito in reversed(self.tabla):
            if nombre in ambito:
                ambito[nombre]['valor'] = valor
                return
        raise Exception(f"Error: Variable '{nombre}' no declarada.")

    def obtener(self, nombre):
        for ambito in reversed(self.tabla):
            if nombre in ambito:
                return ambito[nombre]
        raise Exception(f"Error: Variable '{nombre}' no declarada.")
