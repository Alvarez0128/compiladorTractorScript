from flask import Flask, request, jsonify
from flask_cors import CORS
from Analizador_Lexico import construir_analizador_lexico, reiniciar_analizador_lexico, obtener_errores_lexico
from Analizador_Sintactico import construir_analizador_sintactico, obtener_errores_sintactico, reiniciar_analizador_sintactico, tree_to_json
from Codigo_intermedio import GeneradorCodigoIntermedio
# from Codigo_optimizado import generar_codigo_optimizado
# from Codigo_objeto import generar_codigo_arduino


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
    
    arbol = parser.parse(code)
    
    arbolJSON = tree_to_json(arbol)
    
    # Obtener errores después de analizar el código
    errores_sintactico = obtener_errores_sintactico()
    errores = errores_lexico + errores_sintactico
    
    # Generar el código intermedio
    generador = GeneradorCodigoIntermedio()
    generador.analizar(arbol)
    tripletas = generador.tripletas
    
    # Formatear las tripletas como texto
    codigo_intermedio_texto = "\n".join([f"{i+1}. {tripleta}" for i, tripleta in enumerate(tripletas)])
    
    # # Optimizar el código intermedio
    # codigo_optimizado = generar_codigo_optimizado(codigo_intermedio)
    # # Exportar el código optimizado a una cadena de texto formateada
    # codigo_optimizado_texto = exportar_codigo_a_texto(codigo_optimizado)    
    
    # # Generar el código Arduino
    # if codigo_optimizado:
    #     codigo_arduino = generar_codigo_arduino(codigo_optimizado)
    #     # Exportar el código Arduino a una cadena de texto formateada
    #     codigo_arduino_texto = exportar_codigo_a_texto(codigo_arduino)
    # else:
    #     codigo_arduino_texto = "Código Arduino no generado"

    # Devolver los resultados y errores
    return jsonify({'tokens': tokens, 'errors': errores},arbolJSON,codigo_intermedio_texto,'codigo_optimizado_texto','codigo_arduino_texto') 


if __name__ == '__main__':
    app.run(debug=True)
