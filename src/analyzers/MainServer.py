from flask import Flask, request, jsonify
from flask_cors import CORS
from Analizador_Lexico import construir_analizador_lexico, reiniciar_analizador_lexico, obtener_errores_lexico
# from Analizador_Sintactico import construir_analizador_sintactico, obtener_errores_sintactico, tree_to_json, tree_to_string

app = Flask(__name__)
CORS(app)

lexer = construir_analizador_lexico()
# parser = construir_analizador_sintactico()

@app.route('/compile', methods=['POST'])
def compile_code():
    # Reiniciamos la lista de errores en cada solicitud
    reiniciar_analizador_lexico(lexer)

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

    # arbol = tree_to_json(parser.parse(code))
    
    # Obtener errores después de analizar el código
    errores_lexico = obtener_errores_lexico()

    errores = errores_lexico 
    
    # Devolver los resultados y errores
    return jsonify({'tokens': tokens, 'errors': errores},[]) 


if __name__ == '__main__':
    app.run(debug=True)
