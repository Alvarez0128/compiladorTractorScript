from flask import Flask, request, jsonify
from flask_cors import CORS
from Analizador_Lexico import construir_analizador_lexico, reiniciar_analizador_lexico, obtener_errores_lexico
from Analizador_Sintactico import construir_analizador_sintactico, obtener_errores_sintactico, reiniciar_analizador_sintactico, tree_to_json
app = Flask(__name__)
CORS(app)

parser = construir_analizador_sintactico()
lexer = construir_analizador_lexico()

@app.route('/compile', methods=['POST'])
def compile_code():
    reiniciar_analizador_lexico(lexer)
    reiniciar_analizador_sintactico()
    # Obtener el código fuente de la solicitud POST
    code = request.json['code']
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
    errores_lexico = obtener_errores_lexico()
    reiniciar_analizador_lexico(lexer)
    reiniciar_analizador_sintactico()
    
    arbol = tree_to_json(parser.parse(code))
    
    # Obtener errores después de analizar el código
    errores_sintactico = obtener_errores_sintactico()
    errores = errores_lexico + errores_sintactico
    
    # Devolver los resultados y errores
    return jsonify({'tokens': tokens, 'errors': errores},arbol) 


if __name__ == '__main__':
    app.run(debug=True)
