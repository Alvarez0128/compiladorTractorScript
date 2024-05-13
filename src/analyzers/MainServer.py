from flask import Flask, request, jsonify
from flask_cors import CORS
from Analizador_Lexico import construir_analizador_lexico, reiniciar_analizador_lexico, obtener_errores_lexico
from Analizador_Sintactico import construir_analizador_sintactico, obtener_errores_sintactico, tree_to_string

app = Flask(__name__)
CORS(app)

lexer = construir_analizador_lexico()
parser = construir_analizador_sintactico()

@app.route('/compile', methods=['POST'])
def compile_code():
    # Reiniciamos la lista de errores en cada solicitud
    reiniciar_analizador_lexico(lexer)

    # Obtener el código fuente de la solicitud POST
    code = request.json['code']
    # Reemplazar los saltos de línea por '\n' explícitamente
    code = code.replace('\r\n', '\n')
    # Pasar el código al analizador léxico
    lexer.input(code)
    
    tokens = []
    for tok in lexer:
        tokens.append({
            'type': tok.type,
            'value': tok.value,
            'line': tok.lineno,
            'column': tok.lexpos - code.rfind('\n', 0, tok.lexpos)
        })

    result = tree_to_string(parser.parse(code))
    
    # Obtener errores después de analizar el código
    errores_lexico = obtener_errores_lexico()
    errores_sintactico = obtener_errores_sintactico()

    # Fusionar las listas de errores en una sola lista
    errores = errores_lexico + errores_sintactico
    all_errors = remove_duplicates(errores)
    
    # Devolver los resultados y errores
    return jsonify({'tokens': tokens, 'errors': all_errors, 'tree':result})

def remove_duplicates(error_list):
    
    unique_errors = []
    for error in error_list:
        if error not in unique_errors:
            unique_errors.append(error)
    return unique_errors


if __name__ == '__main__':
    app.run(debug=True)
