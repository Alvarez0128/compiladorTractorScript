class GeneradorTripletas:
    def __init__(self):
        self.tripletas = []
        self.temporales = 0

    def nueva_temporal(self):
        temp = f"T{self.temporales}"
        self.temporales += 1
        return temp

    def agregar_tripleta(self, operacion, arg1, arg2='', resultado=''):
        tripleta = (operacion, arg1, arg2, resultado)
        self.tripletas.append(tripleta)

    def obtener_tripletas(self):
        return self.tripletas

    def reiniciar(self):
        self.tripletas = []
        self.temporales = 0
