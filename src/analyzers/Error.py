class Error:
    def __init__(self, error_type,error_description, value, line, column):
        self.error_type = error_type
        self.error_description = error_description
        self.value = value
        self.line = line
        self.column = column

    def __eq__(self, other):
        return (
            self.error_type == other.error_type and
            self.error_description == other.error_description and
            self.value == other.value and
            self.line == other.line and
            self.column == other.column
        )
    def __str__(self):
        return f"Error: {self.error_type} - {self.error_description} en la linea {self.line}, columna {self.column} - Cadena: {self.value}"