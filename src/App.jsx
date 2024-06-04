import React, { useRef, useState } from 'react';
import { Layout, Card, ConfigProvider, Button, Tooltip, Tabs, Table, message, Dropdown, Space, Tree, Modal, Image, Checkbox } from 'antd';
import { DownOutlined } from '@ant-design/icons';
import Editor from '@monaco-editor/react';
import { writeFile, readTextFile } from '@tauri-apps/api/fs';
import { open, save } from '@tauri-apps/api/dialog';
import './App.css'

const { Header, Content, Footer } = Layout;

const columns = [
  {
    title: 'Token',
    dataIndex: 'type',
    key: 'type',
  },
  {
    title: 'Lexema',
    dataIndex: 'value',
    key: 'value',
    render: (text) => <a>{text}</a>,
  },
  {
    title: 'Linea',
    dataIndex: 'line',
    key: 'line',
  },
  {
    title: 'Columna',
    key: 'column',
    dataIndex: 'column',
  },
];

function App() {
  const [tokens, setTokens] = useState([]);
  const [errors, setErrors] = useState([]);
  const [compilationMessage, setCompilationMessage] = useState('');
  const [codigo, setCodigo] = useState('');
  const [arbol, setArbol] = useState([]);
  const [codigoIntermedio, setcodigoIntermedio] = useState('');
  const [codigoOptimizado, setcodigoOptimizado] = useState('');
  const [codigoObjeto, setcodigoObjeto] = useState('');
  const [modalVisible, setModalVisible] = useState(false);
  const [modalImageSrc, setModalImageSrc] = useState('');
  const [openMenuVer, setOpenMenuVer] = useState(false);
  const [verPanDer, setverPanDer] = useState(true);
  const [verSalida, setverSalida] = useState(true);

  const imageMap = {
    1: '../public/Bloque_CodigoAF.png',
    2: '../public/expresionAF.png',
    3: '../public/DeclaracionAF.png',
    4: '../public/listaAF.png',
    5: '../public/menor_tipoAF.png',
    6: '../public/valores_listaAF.png',
    7: '../public/siAF.png',
    8: '../public/paraAF.png',
    9: '../public/mientrasAF.png',
    10: '../public/mostrar_en_pantallaAF.png',
    11: '../public/ProgramaAF.png',
    12: '../public/IdentificadorError.png',
    13: '../public/SinoAF(Nuevo).png',
    14: '../public/ESPERAR_AF.png',
    15: '../public/error_asignacion.png',
    16: '../public/error_motor.png',
    17: '../public/error_duplicatedvar.png',
    18: '../public/error_inexistsvar.png'
  };

  let lexTable = <ConfigProvider theme={{
    components: {
      Table: {
        colorBgContainer: '#303030',
        algorithm: true,
        borderColor: '#282828',
        colorText: '#dcdcdc',
        rowHoverBg: '#353535',
        colorTextHeading: '#fff',
        stickyScrollBarBg: '#365d34',
      }
    }
  }}>
    <Table pagination={false} columns={columns} dataSource={tokens} id='tabla' />
  </ConfigProvider>

  let sintactTree = <div className='font-mono font-bold rounded-lg p-5 text-lg overflow-auto' id='baseInteriorTabs'>
    <pre className='font-mono font-bold text-lg p-2'>
      Gramatica generada:<br />
      <ConfigProvider theme={{
        components: {
          Tree: {
            colorBgContainer: '#404040',
            algorithm: true,
            colorText: '#dcdcdc',
            nodeSelectedBg: '#606060',
            nodeHoverBg: '#505050'
          }
        }
      }}
      >
        <Tree
          showLine
          switcherIcon={<DownOutlined />}
          defaultExpandedKeys={['0-0-0']}
          // onSelect={onSelect}
          treeData={arbol}
          style={{ overflow: "auto", padding: "10px" }}
        />
      </ConfigProvider>
    </pre>
  </div>

  let intermediateCode = <div className='font-mono font-bold rounded-lg p-5 text-lg overflow-auto' id='baseInteriorTabs'>
    <pre className='font-mono font-bold text-base p-2'>{!codigoIntermedio ? "Código intermedio no generado" : codigoIntermedio}</pre>
  </div>
  let optimizedCode = <div className='font-mono font-bold rounded-lg p-5 text-lg overflow-auto' id='baseInteriorTabs'>
    <pre className='font-mono font-bold text-base p-2'>{!codigoOptimizado ? "Código optimizado no generado" : codigoOptimizado}</pre>
  </div>
  let objectCode = <div className='font-mono font-bold rounded-lg p-5 text-lg overflow-auto' id='baseInteriorTabs'>
    <pre className='font-mono font-bold text-base p-2'>{!codigoObjeto ? "Código Arduino no generado" : codigoObjeto}</pre>
  </div>

  const itemsTabs = [
    {
      key: '1',
      label: 'Componentes Léxicos',
      children: lexTable,
    },
    {
      key: '2',
      label: 'Análisis Sintáctico',
      children: sintactTree,
    },
    {
      key: '4',
      label: 'Codigo Intermedio',
      children: intermediateCode,
    },
    {
      key: '5',
      label: 'Codigo Optimizado',
      children: optimizedCode,
    },
    {
      key: '6',
      label: 'Codigo Objeto',
      children: objectCode,
    },
  ];

  const editorRef = useRef(null);

  function handleEditorDidMount(editor, monaco) {
    editorRef.current = editor;

    // Aquí defines el lenguaje y el tema personalizados
    monaco.languages.register({ id: 'TractorScript' });
    monaco.languages.setMonarchTokensProvider('TractorScript', {
      tokenizer: {
        root: [
          [/\b(COMENZAR|TERMINAR|PARA|MIENTRAS|SI|SINO|INTENTAR|CAPTURAR|EXCEPCION|FUNCION|CODIGO|RETORNA)\b/, 'keyword'],
          [/\b(A_CADENA|MOSTRAR_EN_PANTALLA|DETENER_MOTOR|MOTOR_ENCENDIDO|VELOCIDAD|CAMBIAR_DIRECCION|VERIFICAR_FRENO|DISTANCIA_RECORRIDA|ACTIVAR_FRENO|FRENOS_ACTIVADOS|CALCULAR_DISTANCIA_RESTANTE|DISTANCIA_RESTANTE|ACELERAR|AJUSTAR_VELOCIDAD|NUEVA_VELOCIDAD|SONAR_ALARMA|ESPERAR|VERIFICAR_SENSOR_OBSTACULOS|TIEMPO_TRANSCURRIDO)\b/, 'functions'],
          [/\b(ENTERO|DECIMAL|BOOL|LISTA|DICCIONARIO)\b/, 'datatypes'],
          [/\b(COMENZAR|TERMINAR)\b/, 'keyword'],
          [/\b\d+\.\d+\b/, 'number.decimal'],
          [/\d+(\.\d*){2,}|\d+\.\d+(\.\d+)+|\.\d+(\.\d*)*|(\d?\.\.\d+)|\d+\.(?!\d)/, 'number.decimal.invalid'],
          [/\b\d+\b/, 'number'],
          [/[+-]{2,}\d+/, 'number.invalid'],
          [/\/\/.*/, 'comment'],
          [/\/\*.*\*\//, 'comment'],
          [/"([^"\\]|\\.)*$/, 'string.invalid'],
          [/"/, { token: 'string.quote', bracket: '@open', next: '@string' }],
          [/'[^\\']'/, 'string'],
          [/'/, 'string.invalid'],
          [/[<>]=?|==/, 'operator.logical'],
          [/\b[<>]=?|==|(Falso|Verdadero|falso|verdadero|o|O|NO|No|nO|no|y|Y)\b/, 'operator.logical.words'],
          [/[+\-*/]|=/, 'operator.arit'],
          [/\b[a-zA-Z_ñÑ][a-zA-Z0-9_ñÑ]*\b/, 'identifier'],
          [/\b\d+[a-zA-Z_ñÑ][a-zA-Z0-9_ñÑ]*\b/, 'identifier.error']
        ],
        string: [
          [/[^\\"]+/, 'string'],
          [/\\./, 'string.escape.invalid'],
          [/"/, { token: 'string.quote', bracket: '@close', next: '@pop' }]
        ]
      }
    });

    monaco.languages.setLanguageConfiguration('TractorScript', {
      comments: {
        lineComment: '//',
        blockComment: ['/*', '*/']
      },
      brackets: [
        ['{', '}'],
        ['[', ']'],
        ['(', ')']
      ],
      autoClosingPairs: [
        { open: '{', close: '}' },
        { open: '[', close: ']' },
        { open: '(', close: ')' },
        { open: '"', close: '"' },
        { open: "'", close: "'" }
      ]
    });

    monaco.editor.defineTheme('myCustomTheme', {
      base: 'vs-dark',
      inherit: true,
      rules: [
        { token: 'keyword', foreground: '44bd54', fontStyle: 'bold' },
        { token: 'functions', foreground: '71b3ff' },
        { token: 'datatypes', foreground: 'ff4dd8', fontStyle: 'bold' },
        { token: 'identifier', foreground: 'ffd374' },
        { token: 'identifier.error', foreground: 'FF0000', fontStyle: 'bold' },
        { token: 'number', foreground: 'd66835', fontStyle: 'bold' },
        { token: 'number.invalid', foreground: 'FF0000', fontStyle: 'bold' },
        { token: 'number.decimal.invalid', foreground: 'FF0000', fontStyle: 'bold' },
        { token: 'comment', foreground: 'b8b8b8' },
        { token: 'string', foreground: 'CE9178' },
        { token: 'string.invalid', foreground: 'FF0000', fontStyle: 'bold' },
        { token: 'operator.arit', foreground: 'a371ff' },
        { token: 'operator.logical', foreground: 'ff70cf' }
      ],
      colors: {
        'editor.foreground': '#F8F8F8',
        'editor.background': '#1E1E1E',
        'editorCursor.foreground': '#A7A7A7',
        'editor.lineHighlightBackground': '#333333',
        'editorLineNumber.foreground': '#858585',
        'editor.selectionBackground': '#264F78',
        'editor.inactiveSelectionBackground': '#3A3D41'
      }
    });

    monaco.editor.setTheme('myCustomTheme');
  }


  const goToLineAndColumn = (line, column, text) => {
    if (editorRef.current) {
      const model = editorRef.current.getModel();
      const position = { lineNumber: line, column: column };
      const startOffset = model.getOffsetAt(position);
      const textLength = text.length;
      let endOffset = startOffset + textLength;
      let endPosition = model.getPositionAt(endOffset);

      // Check if the text exists at the position
      const currentText = model.getValueInRange({
        startLineNumber: line,
        startColumn: column,
        endLineNumber: endPosition.lineNumber,
        endColumn: endPosition.column,
      });

      if (currentText !== text) {
        // If text not found, select only one character
        endOffset = startOffset + 1;
        endPosition = model.getPositionAt(endOffset);
      }

      editorRef.current.revealPositionInCenter(position);
      editorRef.current.setPosition(position);
      editorRef.current.setSelection({
        startLineNumber: line,
        startColumn: column,
        endLineNumber: endPosition.lineNumber,
        endColumn: endPosition.column,
      });
      editorRef.current.focus();
    }
  };

  const compileCode = () => {
    fetch('http://localhost:5000/compile', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ code: editorRef.current.getValue() }),
    })
      .then(response => response.json())
      .then(data => {
        //console.log(data[0].errors);
        if (data[0].tokens) {
          setTokens(data[0].tokens);
          setArbol([data[1]])
          setErrors([]);
        }
        if (data[0].errors) {
          setErrors(data[0].errors);
          setCompilationMessage('Compilación exitosa');
          setcodigoIntermedio(data[2]);
          setcodigoOptimizado(data[3]);
          setcodigoObjeto(data[4]);
        }
        editorRef.current.setPosition({ lineNumber: 1, column: 1 });

      })
      .catch(error => console.error('Error:', error));
  };

  const guardarArchivo = async () => {
    const codigo = editorRef.current.getValue();
    try {
      const result = await save({
        defaultPath: 'code.tsp',
        filters: [{
          name: 'TractorScript',
          extensions: ['tsp']
        }]
      });
      if (result) {
        await writeFile(result, codigo);
        message.success('Archivo guardado correctamente');
      } else {
        message.info('Guardado cancelado por el usuario');
      }
    } catch (error) {
      console.error('Error al guardar el archivo:', error);
      message.error('Error al guardar el archivo');
    }
  };

  const nuevoArchivo = () => {
    setCodigo('');
  }
  const abrirArchivo = async () => {
    try {
      const result = await open({

        filters: [{
          name: 'TractorScript',
          extensions: ['tsp']
        }]
      });
      if (result) {
        const codigo = await readTextFile(result);
        setCodigo(codigo);
        message.success('Abierto');
      } else {
        message.info('No abierto');
      }
    } catch (error) {
      console.error('Error al abrir el archivo:', error);
      message.error('Error al abrir el archivo');
    }
  };
  const handleMenuClick = (e) => {
    if (e.key === 'pander' || e.key === 'salida') {
      setOpenMenuVer(true);
    }
  };

  // Función para mostrar el modal
  function showModalInfoErrores(id) {
    const imageSrc = imageMap[id];
    if (imageSrc) {
      setModalImageSrc(imageSrc);
      setModalVisible(true);
    }
  }


  // Función para ocultar el modal
  const handleCancel = () => {
    setModalVisible(false);
  };

  const itemsArchivo = [
    {
      label: 'Nuevo archivo',
      key: 'nuevo',
      onClick: () => {
        nuevoArchivo();
      },
    },
    {
      label: 'Abrir',
      key: 'abrir',
      onClick: () => {
        abrirArchivo();
      },
    },
    {
      label: 'Guardar',
      key: 'guardarc',
      onClick: () => {
        guardarArchivo();
      },
    },
  ];

  const itemsEditar = [
    {
      label: 'Copiar',
      key: 'copiar',
    },
    {
      label: 'Cortar',
      key: 'cortar',
    },
    {
      label: 'Pegar',
      key: 'pegar',
    },
  ];

  const onChangePD = (e) => {
    setverPanDer(e.target.checked)
  };
  const onChangeS = (e) => {
    setverSalida(e.target.checked)
  };
  const alturaSalida = verSalida ? {} : { height: '100vh' };
  const itemsVer = [
    {
      label: (<Checkbox defaultChecked={verPanDer} onChange={onChangePD}>Panel derecho</Checkbox>),
      key: 'pander',
    },
    {
      label: (<Checkbox defaultChecked={verSalida} onChange={onChangeS}>Salida</Checkbox>),
      key: 'salida',
    },
  ];

  const itemsAyuda = [
    {
      label: 'Documentación',
      key: 'documentacion',
    },
    {
      label: 'Soporte',
      key: 'soporte',
    },
  ];

  const handleOpenChangeMenuVer = (nextOpen, info) => {
    if (info.source === 'trigger' || nextOpen) {
      setOpenMenuVer(nextOpen);
    }
  };

  const MenuDropdown = ({ label, items, onClick, onOpenChange, open }) => (
    <Dropdown menu={{ items, onClick }} trigger={['click']} onOpenChange={onOpenChange} open={open}>
      <a onClick={(e) => e.preventDefault()} className="cursor-default">
        <Space className=' text-white hover:bg-green-600 px-3 py-0.5 hover:text-white'>
          {label}
        </Space>
      </a>
    </Dropdown>
  );

  return (
    <Layout>
      <Header className='bg-zinc-900 text-sm text-white h-fit pl-0'>
        <ConfigProvider theme={{
          components: {
            Dropdown: {
              colorBgElevated: '#C9FFB6',
              borderRadiusLG: 2,
              colorText: '#000'
            }
          }
        }}>
          <MenuDropdown label="Archivo" items={itemsArchivo} />
          <MenuDropdown label="Editar" items={itemsEditar} />
          <MenuDropdown label="Ver" items={itemsVer} onClick={handleMenuClick} onOpenChange={handleOpenChangeMenuVer} open={openMenuVer} />
          <MenuDropdown label="Ayuda" items={itemsAyuda} />
        </ConfigProvider>

        <ConfigProvider theme={{
          components: {
            Button: {
              textHoverBg: 'rgba(22, 163, 74, 0)',
              colorText: '#fff',
              colorBgTextActive: 'rgba(22, 163, 74, 0.28)'
            }
          }
        }}>
          <Tooltip title="Compilar">
            <Button type='text' onClick={compileCode}>▶</Button>
          </Tooltip>
        </ConfigProvider>

      </Header>
      
      <Content id='content' className='border border-green-900 grid grid-cols-2' style={alturaSalida}>
        <div>
          <Editor
            theme='vs-dark'
            height='100%'
            width={verPanDer ? '100%' : '100vw'}
            defaultLanguage="TractorScript"
            options={{
              fontSize: 15,
              fontFamily: 'Cascadia Mono' ?? 'Arial',
            }}
            value={`${codigo}` ?? ""}
            onChange={(value) => setCodigo(value)}
            onMount={handleEditorDidMount}
            className='border-e border-green-900 pt-3 relative'
          />
        </div>
        {verPanDer &&
          <div className='px-6 '>
            <ConfigProvider
              theme={{
                components: {
                  Tabs: {
                    itemSelectedColor: '#43BC4C',
                    algorithm: true,
                    inkBarColor: '#43BC4C',
                    itemColor: '#fff',
                    itemHoverColor: '#47AB4E',
                    colorText: '#fff',
                    colorBorderSecondary: '#8b8b8b',
                    colorBgContainer: '#282828'
                  }
                }
              }}
            >
              <Tabs defaultActiveKey="1" items={itemsTabs} />
            </ConfigProvider>
          </div>
        }
      </Content>

      <Footer className='bg-slate-800 h-60 m-0 p-0'>
        <ConfigProvider theme={{
          components: {
            Card: {
              headerHeight: 0,
              colorText: '#CCCCCC',
              colorBorderSecondary: '#14532D',
              paddingLG: 10,
              algorithm: true
            },
            Modal: {
              titleFontSize: 20
            }
          }
        }}>
          <Card
            title="Salida ↴"
            bordered={false}
            style={{
              width: '100%',
              height: '35vh',
              borderRadius: 0,
              overflow: 'auto',
              backgroundColor: '#2e2e2e',
            }}
          >
            <div className='px-5 '>
              {errors.length === 0 && <p>{compilationMessage}</p>}
              {errors.map((error, index) => (
                <li key={index} onClick={() => showModalInfoErrores(error.index)} className='hover:text-green-600 cursor-pointer transition'>
                  Error {error.type} - {error.description} en la <a onClick={(e) => { e.stopPropagation(); goToLineAndColumn(error.line, error.column, error.value); }} className="font-bold hover:underline"> línea {error.line}, columna {error.column}</a> lexema: {error.value}
                </li>
              ))}


              <Modal
                title="Validación para el error"
                open={modalVisible}
                onCancel={handleCancel}
                footer={null}
              >
                <h1>Imagen:</h1>
                <Image
                  width="100%"
                  src={modalImageSrc}
                />
              </Modal>
            </div>
          </Card>
        </ConfigProvider>
      </Footer>
    </Layout>
  );
}

export default App;
