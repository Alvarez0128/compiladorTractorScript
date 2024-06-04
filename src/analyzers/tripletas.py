# tripletas.py

class Tripleta:
    def __init__(self, operador, operando1, operando2):
        self.operador = operador
        self.operando1 = operando1
        self.operando2 = operando2
    
    def __repr__(self):
        return f"({self.operador}, {self.operando1}, {self.operando2})"

class GeneradorTripletas:
    def __init__(self):
        self.tripletas = []
        self.temporal_counter = 0

    def nueva_temporal(self):
        temporal = f"t{self.temporal_counter}"
        self.temporal_counter += 1
        return temporal

    def agregar_tripleta(self, operador, operando1, operando2):
        tripleta = Tripleta(operador, operando1, operando2)
        self.tripletas.append(tripleta)
        return tripleta

    def obtener_tripletas(self):
        return self.tripletas
